import numpy as np
import pandas as pd
from typer.testing import CliRunner

from ww import cli
from ww.backtest.run import run_timing_overlay, verdict


def _fixture_repo(tmp_path):
    """A tiny self-contained repo: breadth_series + fund_proxy + a price df with QQQ/SPY/TQQQ/SQQQ."""
    bdir = tmp_path / "data" / "breadth"; bdir.mkdir(parents=True)
    idx = pd.date_range("2008-01-02", periods=600, freq="B")
    # GMI mostly 6 (bullish), but dips to 0 for a 40-day stretch in the middle
    s10h = np.full(600, 160.0); s10h[250:290] = 10.0
    nh = np.full(600, 150.0); nh[250:290] = 20.0
    bs = pd.DataFrame({"date": idx, "n_nyse":[1600]*600, "n_broad":[3200]*600, "t2108_nyse":[60.0]*600, "t2108_broad":[58.0]*600,
                       "pct_above_50dma_broad":[55.0]*600, "pct_above_200dma_broad":[60.0]*600,
                       "new_52w_highs":[300]*600, "new_52w_lows":[10]*600, "nasdaq_new_52w_highs":nh, "nasdaq_new_52w_lows":[5]*600,
                       "s10_total":[200.0]*600, "s10_higher":s10h, "coverage_note":[""]*600})
    bs.to_parquet(bdir / "breadth_series.parquet", index=False)
    pd.DataFrame({"date": idx, "fund_proxy": list(np.linspace(10, 25, 600))}).to_parquet(bdir / "fund_proxy.parquet", index=False)
    # prices: QQQ trends up but drops 25% during the GMI=0 stretch then recovers; SPY similar; TQQQ ~3x; SQQQ ~ -3x
    base = np.linspace(100, 220, 600)
    qqq = base.copy(); qqq[250:300] = base[250:300] * np.linspace(1.0, 0.75, 50); qqq[300:] = qqq[300:] - (base[300] - qqq[299])
    qqq = pd.Series(qqq, index=idx)
    ret = qqq.pct_change().fillna(0.0)
    tqqq = (1 + 3 * ret).cumprod() * 100
    sqqq = (1 - 3 * ret).cumprod() * 100
    prices = pd.DataFrame({"QQQ": qqq, "SPY": qqq * 0.9, "TQQQ": tqqq, "SQQQ": sqqq})
    (tmp_path / "raw").mkdir(exist_ok=True)
    pd.DataFrame({"date":[idx[10]], "gmi_value":[6], "qqq_day":[None],"qqq_dir":[None],"t2108":[None],"stance":[None],
                  "parse_confidence":["high"],"source_url":["u"],"stem":["x"],"gmi_state":[None],"gmi2_value":[None],"gmi_s":[None]}).to_parquet(tmp_path/"raw"/"timeline.parquet", index=False)
    return tmp_path, prices


def test_run_timing_overlay_produces_default_grid_and_verdict(tmp_path):
    root, prices = _fixture_repo(tmp_path)
    res = run_timing_overlay(root, prices=prices, start=None, end=None, cost_bps=5.0, quick=False)
    assert {"default", "benchmarks", "grid", "verdict", "equity"} <= set(res)
    assert "cagr" in res["default"] and "max_drawdown" in res["default"] and "sharpe" in res["default"]
    assert "buy_hold_qqq" in res["benchmarks"]
    assert isinstance(res["grid"], list) and len(res["grid"]) >= 5
    assert res["verdict"] in {"adds value", "marginal", "drag"} or res["verdict"].split(" —")[0] in {"adds value", "marginal", "drag"}
    # the strategy sat out the -25% QQQ stretch -> its max drawdown should be smaller than buy-and-hold's
    assert abs(res["default"]["max_drawdown"]) < abs(res["benchmarks"]["buy_hold_qqq"]["max_drawdown"])


def test_verdict_classification():
    # crafted metrics: strategy better Sharpe AND <=0.7x drawdown, grid stable -> "adds value"
    strat = {"sharpe": 1.2, "max_drawdown": -0.20, "cagr": 0.12}
    bench = {"sharpe": 1.0, "max_drawdown": -0.40, "cagr": 0.13}
    grid = [{"label": "5bps", "metrics": {"sharpe": 1.2, "max_drawdown": -0.20}},
            {"label": "20bps", "metrics": {"sharpe": 1.1, "max_drawdown": -0.22}}]
    v = verdict(strat, bench, grid)
    assert v.startswith("adds value")
    # underperforms Sharpe AND doesn't cut drawdown -> "drag"
    strat2 = {"sharpe": 0.7, "max_drawdown": -0.38, "cagr": 0.08}
    assert verdict(strat2, bench, grid).startswith("drag")
    # cuts drawdown but lower CAGR/Sharpe -> "marginal"
    strat3 = {"sharpe": 0.9, "max_drawdown": -0.18, "cagr": 0.09}
    assert verdict(strat3, bench, grid).startswith("marginal")


def test_ww_backtest_cli_offline(tmp_path, monkeypatch):
    root, prices = _fixture_repo(tmp_path)
    # mock the price loader so the CLI doesn't hit yfinance, and the litterbox upload
    monkeypatch.setattr("ww.cli._load_backtest_prices", lambda r, **kw: prices)
    monkeypatch.setattr("ww.cli._upload_plot", lambda path: "https://litter.catbox.moe/fixture.png")
    runner = CliRunner()
    r = runner.invoke(cli.app, ["backtest", "timing-overlay", "--root", str(root), "--quick", "--no-write-wiki"])
    assert r.exit_code == 0, r.output
    assert "verdict" in r.output.lower()
    assert "buy-and-hold" in r.output.lower() or "buy_hold" in r.output.lower()
    # with --write-wiki it produces the page
    r2 = runner.invoke(cli.app, ["backtest", "timing-overlay", "--root", str(root), "--quick"])
    assert r2.exit_code == 0
    assert (root / "wiki" / "methodology" / "backtest-timing-overlay.md").exists()
