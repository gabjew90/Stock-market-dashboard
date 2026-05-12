import json
from pathlib import Path

import httpx
from typer.testing import CliRunner

from ww import cli
from ww.corpus.index import PostRecord, write_posts_jsonl
from ww.scrape import ingest as ingest_mod

runner = CliRunner()


def _rec_cli(**over) -> PostRecord:
    base = dict(post_id=1, url="u", date="2020-01-01T00:00:00", slug="s", stem="2020-01-01-s",
                title="t", word_count=10, chart_count=0, chart_image_urls=[], kind_guess="unknown")
    base.update(over)
    return PostRecord(**base)


def test_stats_command_empty(tmp_path: Path):
    result = runner.invoke(cli.app, ["stats", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "total_posts: 0" in result.stdout


def test_scrape_command_uses_root_and_reports_count(fixtures_dir, tmp_path, monkeypatch):
    page1 = json.loads((fixtures_dir / "wp_api_page1.json").read_text())

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if page == 1:
            return httpx.Response(200, json=page1, headers={"X-WP-TotalPages": "1"})
        return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})

    real_scrape = ingest_mod.scrape_blog

    def patched(base_url="https://wishingwealthblog.com", **kw):
        kw.setdefault("client", httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test"))
        kw["delay"] = 0.0
        return real_scrape("https://example.test", **kw)

    monkeypatch.setattr(cli, "scrape_blog", patched)

    result = runner.invoke(cli.app, ["scrape", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "2 posts" in result.stdout
    assert (tmp_path / "raw" / "posts.jsonl").exists()

    # And `ww stats` then reads it back:
    result2 = runner.invoke(cli.app, ["stats", "--root", str(tmp_path)])
    assert result2.exit_code == 0
    assert "total_posts: 2" in result2.stdout


def test_ww_batch_lists_uningested_filtered_by_kind(tmp_path: Path):
    write_posts_jsonl(tmp_path / "raw" / "posts.jsonl", [
        _rec_cli(post_id=1, stem="2020-01-01-a", kind_guess="long_form", title="Strategy primer", word_count=900),
        _rec_cli(post_id=2, stem="2020-01-02-b", kind_guess="daily_update", title="GMI=6", word_count=40),
        _rec_cli(post_id=3, stem="2020-01-03-c", kind_guess="long_form", title="More strategy", word_count=700, ingested=True),
        _rec_cli(post_id=4, stem="2020-01-04-d", kind_guess="unknown", title="A trade", word_count=300),
    ])
    # default: only un-ingested, all kinds, newest first
    result = runner.invoke(cli.app, ["batch", "--root", str(tmp_path), "-n", "10"])
    assert result.exit_code == 0
    assert "2020-01-04-d" in result.stdout and "2020-01-01-a" in result.stdout
    assert "2020-01-03-c" not in result.stdout            # already ingested
    # filter to a single kind
    result2 = runner.invoke(cli.app, ["batch", "--root", str(tmp_path), "-n", "10", "--kind", "long_form"])
    assert result2.exit_code == 0
    assert "2020-01-01-a" in result2.stdout
    assert "2020-01-02-b" not in result2.stdout and "2020-01-04-d" not in result2.stdout
    # -n limits
    result3 = runner.invoke(cli.app, ["batch", "--root", str(tmp_path), "-n", "1"])
    assert result3.exit_code == 0
    assert result3.stdout.count("raw/posts/") == 1


def _write_monthly_csv(path, highs):
    import pandas as pd
    idx = pd.date_range("2015-01-31", periods=len(highs), freq="ME")
    pd.DataFrame({"open": highs, "high": highs, "low": [h * 0.9 for h in highs], "close": highs}, index=idx).to_csv(path, index_label="date")


def test_ww_compute_green_line_from_csv(tmp_path):
    csv = tmp_path / "m.csv"
    _write_monthly_csv(csv, [10, 20, 50, 40, 45, 30, 48, 49])   # current green line = 50, last close 49 -> no breakout
    result = runner.invoke(cli.app, ["compute", "green-line", "TEST", "--csv", str(csv)])
    assert result.exit_code == 0
    assert "50" in result.stdout
    assert "breakout" in result.stdout.lower()
    assert "no" in result.stdout.lower()  # not a breakout


def test_ww_compute_unknown_indicator_errors():
    result = runner.invoke(cli.app, ["compute", "not-an-indicator", "TEST"])
    assert result.exit_code != 0


def test_ww_compute_gmi_demo():
    result = runner.invoke(cli.app, ["compute", "gmi", "2014-08-01", "--demo"])
    assert result.exit_code == 0
    assert "GMI" in result.stdout
    assert "6" in result.stdout            # demo fixtures make all 6 components True
    assert "DEMO" in result.stdout.upper()


def test_ww_compute_t2108_without_demo_explains_unavailability():
    result = runner.invoke(cli.app, ["compute", "t2108", "2014-08-01"])
    # informative, not a crash — exit 0, points at the methodology page
    assert result.exit_code == 0
    assert "t2108" in result.stdout.lower()
    assert "methodology" in result.stdout.lower() or "breadth" in result.stdout.lower()


def test_ww_compute_t2108_demo_prints_value():
    result = runner.invoke(cli.app, ["compute", "t2108", "2014-08-01", "--demo"])
    assert result.exit_code == 0
    assert "66.67" in result.stdout or "66.6" in result.stdout
    assert "DEMO" in result.stdout.upper()


def test_ww_timeline_builds_parquet(tmp_path):
    import json
    (tmp_path / "raw" / "posts").mkdir(parents=True)
    rows = [{"post_id": 1, "url": "u", "date": "2014-01-28T00:00:00", "slug": "a", "stem": "2014-01-28-a",
             "title": "t", "word_count": 50, "chart_count": 0, "chart_image_urls": [], "kind_guess": "daily_update"}]
    (tmp_path / "raw" / "posts.jsonl").write_text(json.dumps(rows[0]) + "\n", encoding="utf-8")
    (tmp_path / "raw" / "posts" / "2014-01-28-a.md").write_text("---\nurl: u\n---\n\nDay 13 of $QQQ short term up-trend and GMI= 6.\n", encoding="utf-8")
    result = runner.invoke(cli.app, ["timeline", "--root", str(tmp_path)])
    assert result.exit_code == 0
    out = tmp_path / "raw" / "timeline.parquet"
    assert out.exists()
    import pandas as pd
    df = pd.read_parquet(out)
    assert len(df) == 1 and df.iloc[0]["gmi_value"] == 6 and df.iloc[0]["qqq_day"] == 13
    assert "1" in result.stdout  # reports row count


def _tiny_wiki(root):
    import json
    (root / "wiki" / "methodology").mkdir(parents=True)
    (root / "raw" / "posts").mkdir(parents=True)
    (root / "wiki" / "methodology" / "green-line-breakouts.md").write_text(
        "---\ntitle: GLB\n---\n\n# Green Line Breakouts\n\nA green line is an all-time-high level held three months; the breakout is a close above it.\n\n## Sources\n\n_None._\n", encoding="utf-8")
    (root / "raw" / "posts.jsonl").write_text(json.dumps({"post_id": 1, "url": "u", "date": "2012-07-23T00:00:00", "slug": "s", "stem": "2012-07-23-s", "title": "t", "word_count": 10, "chart_count": 0, "chart_image_urls": [], "kind_guess": "long_form"}) + "\n", encoding="utf-8")
    (root / "raw" / "posts" / "2012-07-23-s.md").write_text("---\nurl: u\n---\n\nI draw a green line on the monthly chart.\n", encoding="utf-8")


def test_ww_index_then_search(tmp_path):
    _tiny_wiki(tmp_path)
    r1 = runner.invoke(cli.app, ["index", "--root", str(tmp_path)])
    assert r1.exit_code == 0
    assert (tmp_path / "data" / "index" / "wiki.pkl").exists()
    assert "chunk" in r1.stdout.lower()
    r2 = runner.invoke(cli.app, ["search", "green line breakout", "--root", str(tmp_path)])
    assert r2.exit_code == 0
    assert "green" in r2.stdout.lower()
    assert "green-line-breakouts.md" in r2.stdout or "2012-07-23" in r2.stdout


def test_ww_search_without_index_tells_you_to_build_it(tmp_path):
    _tiny_wiki(tmp_path)
    r = runner.invoke(cli.app, ["search", "green line", "--root", str(tmp_path)])
    # graceful: non-zero or a clear "run ww index" message — accept either, but it must mention index
    assert "index" in r.stdout.lower()


def test_ww_breadth_build_and_show(tmp_path, monkeypatch):
    import numpy as np
    import pandas as pd
    from ww.breadth.series import build_fund_proxy as _real_proxy

    # lay down a tiny universe + panel by hand (skip the network parts)
    bdir = tmp_path / "data" / "breadth"
    (bdir / "panel").mkdir(parents=True)
    pd.DataFrame({"ticker": ["AAA", "BBB"], "name": ["A", "B"], "listing_exchange": ["N", "Q"], "in_nyse": [True, False]}).to_parquet(bdir / "universe.parquet")
    for t, lo, hi in (("AAA", 10, 80), ("BBB", 80, 10)):
        idx = pd.date_range("2020-01-01", periods=300, freq="B")
        c = list(np.linspace(lo, hi, 300))
        df = pd.DataFrame({"open": c, "high": [x + 1 for x in c], "low": [x - 1 for x in c], "close": [float(x) for x in c], "adj_close": [float(x) for x in c], "volume": [1] * 300}, index=idx)
        df.index.name = "date"; df.to_parquet(bdir / "panel" / f"{t}.parquet")

    # make `build` not hit yfinance for the fund proxy
    monkeypatch.setattr("ww.cli.build_fund_proxy", lambda **kw: pd.Series([100.0] * 60, index=pd.date_range("2024-01-01", periods=60, freq="B"), name="fund_proxy"))

    r1 = runner.invoke(cli.app, ["breadth", "build", "--root", str(tmp_path)])
    assert r1.exit_code == 0, r1.output
    assert (bdir / "breadth_series.parquet").exists()
    bs = pd.read_parquet(bdir / "breadth_series.parquet")
    assert {"date", "n_nyse", "n_broad", "t2108_nyse", "t2108_broad", "new_52w_highs", "s10_total", "s10_higher"} <= set(bs.columns)

    r2 = runner.invoke(cli.app, ["breadth", "show", "--root", str(tmp_path)])
    assert r2.exit_code == 0
    assert "t2108" in r2.output.lower()
    assert "2020" in r2.output  # the series date range


def test_ww_breadth_fetch_uses_mocked_downloads(tmp_path, monkeypatch):
    import pandas as pd
    # mock the symbol download + the panel download so `ww breadth fetch` runs offline
    sample = (Path(__file__).parent / "breadth" / "fixtures" / "nasdaqtraded_sample.txt").read_text(encoding="utf-8") if (Path(__file__).parent / "breadth" / "fixtures" / "nasdaqtraded_sample.txt").exists() else "Nasdaq Traded|Symbol|Security Name|Listing Exchange|Market Category|ETF|Round Lot Size|Test Issue|Financial Status|CQS Symbol|NASDAQ Symbol|NextShares\nY|AAPL|Apple Inc. - Common Stock|Q|Q|N|100|N|N||AAPL|N\n"

    def fake_download_symbol_files(dest, **kw):
        dest = Path(dest); dest.mkdir(parents=True, exist_ok=True)
        (dest / "nasdaqtraded.txt").write_text(sample, encoding="utf-8")

    def fake_fetch_panel(uni, panel_dir, **kw):
        panel_dir = Path(panel_dir); panel_dir.mkdir(parents=True, exist_ok=True)
        idx = pd.date_range("2020-01-01", periods=5, freq="B")
        for t in uni["ticker"]:
            df = pd.DataFrame({"open": [10.0] * 5, "high": [11.0] * 5, "low": [9.0] * 5, "close": [10.0] * 5, "adj_close": [10.0] * 5, "volume": [1] * 5}, index=idx)
            df.index.name = "date"; df.to_parquet(panel_dir / f"{t}.parquet")
        return len(uni)

    monkeypatch.setattr("ww.cli.download_symbol_files", fake_download_symbol_files)
    monkeypatch.setattr("ww.cli.fetch_panel", fake_fetch_panel)
    r = runner.invoke(cli.app, ["breadth", "fetch", "--root", str(tmp_path)])
    assert r.exit_code == 0, r.output
    assert (tmp_path / "data" / "breadth" / "universe.parquet").exists()
    assert (tmp_path / "data" / "breadth" / "panel" / "AAPL.parquet").exists()
