"""`ww breadth update` must never destroy stored data on a degraded fetch.

Three guards, each for a bug found in the 2026-09-02 review:
  - the tail merge is additive, not window-replacing (it used to delete stored dates
    the recompute did not produce);
  - a merge that would shrink the series is refused outright;
  - fund_proxy.parquet is not overwritten by an empty or truncated proxy, which would
    make GMI component 6 read False for every date and flip the gate RED.
"""
import pandas as pd
import pytest
from typer.testing import CliRunner

from ww import cli

runner = CliRunner()


def _bdir(root):
    d = root / "data" / "breadth"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _series(dates, n=3000):
    return pd.DataFrame({
        "date": pd.to_datetime(dates),
        "n_nyse": [1900] * len(dates), "n_broad": [n] * len(dates),
        "t2108_nyse": [50.0] * len(dates), "t2108_broad": [50.0] * len(dates),
        "pct_above_50dma_broad": [50.0] * len(dates), "pct_above_200dma_broad": [50.0] * len(dates),
        "new_52w_highs": [200] * len(dates), "new_52w_lows": [10] * len(dates),
        "nasdaq_new_52w_highs": [100] * len(dates), "nasdaq_new_52w_lows": [5] * len(dates),
        "s10_total": [200] * len(dates), "s10_higher": [150] * len(dates),
        "coverage_note": [""] * len(dates),
    })


@pytest.fixture
def stubbed(tmp_path, monkeypatch):
    """A repo root with a stored series + proxy, and update_panel/compute stubbed out."""
    bdir = _bdir(tmp_path)
    stored = _series(pd.bdate_range("2026-01-01", periods=200))
    stored.to_parquet(bdir / "breadth_series.parquet", index=False)
    proxy = pd.DataFrame({"date": pd.bdate_range("2020-01-01", periods=1000),
                          "fund_proxy": [10.0] * 1000})
    proxy.to_parquet(bdir / "fund_proxy.parquet", index=False)
    pd.DataFrame({"ticker": ["AAPL"], "in_nyse": [False]}).to_parquet(bdir / "universe.parquet", index=False)
    monkeypatch.setattr("ww.cli.update_panel", lambda uni, panel_dir, **kw: 1)
    return tmp_path, bdir, stored, proxy


def _run(root):
    r = runner.invoke(cli.app, ["breadth", "update", "--root", str(root)])
    assert r.exit_code == 0, r.output
    return r


def test_recompute_missing_a_stored_date_does_not_delete_it(stubbed, monkeypatch):
    root, bdir, stored, _ = stubbed
    # the recompute covers the tail but is missing one session the stored file already has
    recomputed = _series([d for d in stored["date"].iloc[-60:] if d != stored["date"].iloc[-5]])
    monkeypatch.setattr("ww.cli.compute_breadth_series", lambda *a, **k: recomputed)
    monkeypatch.setattr("ww.cli.build_fund_proxy", lambda **k: pd.Series(dtype=float))
    _run(root)
    after = pd.read_parquet(bdir / "breadth_series.parquet")
    assert len(after) == len(stored), "an additive merge must not drop a stored session"
    assert pd.Timestamp(stored["date"].iloc[-5]) in set(pd.to_datetime(after["date"]))


def test_a_shrinking_merge_is_refused(stubbed, monkeypatch):
    root, bdir, stored, _ = stubbed
    monkeypatch.setattr("ww.cli.compute_breadth_series", lambda *a, **k: _series(pd.bdate_range("2026-01-01", periods=5)))
    monkeypatch.setattr("ww.cli.build_fund_proxy", lambda **k: pd.Series(dtype=float))
    _run(root)
    after = pd.read_parquet(bdir / "breadth_series.parquet")
    assert len(after) == len(stored), "a 200-row series must not be replaced by a 5-row recompute"


def test_an_empty_fund_proxy_does_not_overwrite_a_good_one(stubbed, monkeypatch):
    root, bdir, stored, proxy = stubbed
    monkeypatch.setattr("ww.cli.compute_breadth_series", lambda *a, **k: stored)
    monkeypatch.setattr("ww.cli.build_fund_proxy", lambda **k: pd.Series(dtype=float))
    _run(root)
    after = pd.read_parquet(bdir / "fund_proxy.parquet")
    assert len(after) == len(proxy), "an empty proxy would zero GMI component 6 for every date"


def test_a_truncated_fund_proxy_does_not_overwrite_a_good_one(stubbed, monkeypatch):
    """The VUG fallback, or a fetch that only returns FFTY, is far shorter than the spliced
    series - short enough that keeping it would silently rewrite component 6's history."""
    root, bdir, stored, proxy = stubbed
    short = pd.Series([10.0] * 100, index=pd.bdate_range("2026-01-01", periods=100), name="fund_proxy")
    short.index.name = "date"
    monkeypatch.setattr("ww.cli.compute_breadth_series", lambda *a, **k: stored)
    monkeypatch.setattr("ww.cli.build_fund_proxy", lambda **k: short)
    _run(root)
    after = pd.read_parquet(bdir / "fund_proxy.parquet")
    assert len(after) == len(proxy)


def test_a_healthy_proxy_is_written(stubbed, monkeypatch):
    root, bdir, stored, proxy = stubbed
    grown = pd.Series([11.0] * 1010, index=pd.bdate_range("2020-01-01", periods=1010), name="fund_proxy")
    grown.index.name = "date"
    monkeypatch.setattr("ww.cli.compute_breadth_series", lambda *a, **k: stored)
    monkeypatch.setattr("ww.cli.build_fund_proxy", lambda **k: grown)
    _run(root)
    after = pd.read_parquet(bdir / "fund_proxy.parquet")
    assert len(after) == 1010, "a healthy proxy must still be written"
