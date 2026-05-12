import json
from pathlib import Path

import pandas as pd
import pytest

from ww.indicators.breadth_provider import BreadthProvider
from ww.indicators.gmi import gmi
from ww.indicators.provider import DataUnavailable


def _make_breadth_dir(root: Path):
    bdir = root / "data" / "breadth"
    bdir.mkdir(parents=True)
    dates = pd.date_range("2014-07-01", periods=20, freq="B")
    bs = pd.DataFrame({
        "date": dates,
        "n_nyse": [1000] * 20, "n_broad": [2000] * 20,
        "t2108_nyse": [61.0] * 20, "t2108_broad": [58.0] * 20,
        "pct_above_50dma_broad": [55.0] * 20, "pct_above_200dma_broad": [60.0] * 20,
        "new_52w_highs": [350] * 20, "new_52w_lows": [10] * 20,
        "nasdaq_new_52w_highs": [180] * 20, "nasdaq_new_52w_lows": [5] * 20,
        "s10_total": [200] * 20, "s10_higher": [160] * 20,
        "coverage_note": [""] * 20,
    })
    bs.to_parquet(bdir / "breadth_series.parquet", index=False)
    fp = pd.DataFrame({"date": pd.date_range("2014-01-01", periods=200, freq="B"), "fund_proxy": [10.0 + i * 0.1 for i in range(200)]})
    fp.to_parquet(bdir / "fund_proxy.parquet", index=False)
    (bdir / "validate.json").write_text(json.dumps({"chosen_flavor": "nyse", "t2108": {}, "gmi": {}}), encoding="utf-8")
    return bdir, dates


def _uptrend(n, lo, hi, freq):
    idx = pd.date_range("2010-01-01" if freq == "B" else "2010-01-03", periods=n, freq=freq)
    c = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    return pd.DataFrame({"open": c, "high": c, "low": c, "close": c, "adj_close": c, "volume": [1] * n}, index=idx)


def test_breadth_provider_pct_above_ma(tmp_path):
    _make_breadth_dir(tmp_path)
    bp = BreadthProvider(tmp_path)             # flavor="auto" -> reads validate.json -> "nyse"
    assert bp.pct_above_ma(("X",), 40, "2014-07-10") == 61.0
    bp_broad = BreadthProvider(tmp_path, flavor="broad")
    assert bp_broad.pct_above_ma(("X",), 40, "2014-07-10") == 58.0
    assert bp.pct_above_ma(("X",), 50, "2014-07-10") == 55.0
    assert bp.pct_above_ma(("X",), 200, "2014-07-10") == 60.0
    with pytest.raises(DataUnavailable):
        bp.pct_above_ma(("X",), 100, "2014-07-10")          # unsupported window
    with pytest.raises(DataUnavailable):
        bp.pct_above_ma(("X",), 40, "1999-01-01")           # date not in the series


def test_breadth_provider_other_methods(tmp_path):
    _make_breadth_dir(tmp_path)
    bp = BreadthProvider(tmp_path, nh_universe="nasdaq")
    nhl = bp.nasdaq_new_highs_lows("2014-07-01", "2014-07-10")
    assert "new_highs" in nhl.columns and "new_lows" in nhl.columns
    assert nhl.iloc[0]["new_highs"] == 180 and nhl.iloc[0]["new_lows"] == 5     # nasdaq-only columns
    bp_broad = BreadthProvider(tmp_path, nh_universe="broad")
    assert bp_broad.nasdaq_new_highs_lows("2014-07-01", "2014-07-10").iloc[0]["new_highs"] == 350
    assert bp.successful_10day_new_high("2014-07-10") == (160, 200)
    s = bp.ibd_mutual_fund_index("2014-01-01", "2014-12-31")
    assert len(s) > 0 and s.name == "fund_proxy"


def test_breadth_provider_prices_uses_cache_then_yfinance(tmp_path):
    _make_breadth_dir(tmp_path)
    qqq = _uptrend(400, 100, 300, "B")
    bp = BreadthProvider(tmp_path, prices_cache={("QQQ", "1d"): qqq})
    pd.testing.assert_frame_equal(bp.prices("QQQ", "1d"), qqq)   # served from cache, no network


def test_breadth_provider_missing_series_errors(tmp_path):
    (tmp_path / "data" / "breadth").mkdir(parents=True)          # exists but empty
    with pytest.raises(RuntimeError):
        BreadthProvider(tmp_path)


def test_gmi_with_breadth_provider_is_full_0_to_6(tmp_path):
    _make_breadth_dir(tmp_path)
    cache = {
        ("QQQ", "1d"): _uptrend(400, 100, 300, "B"),
        ("SPY", "1d"): _uptrend(400, 100, 300, "B"),
        ("QQQ", "1wk"): _uptrend(120, 100, 300, "W-SUN"),
    }
    bp = BreadthProvider(tmp_path, flavor="broad", prices_cache=cache)
    r = gmi(bp, "2014-07-10")
    assert r.unavailable == []                                   # all six components computable
    # fixture is fully bullish: t2108 high, lots of new highs, s10 80%, prices uptrending, fund proxy rising
    assert r.score == 6
