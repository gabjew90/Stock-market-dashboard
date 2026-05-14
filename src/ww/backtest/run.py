"""Orchestrate the timing-overlay backtest: default gate + benchmarks + variant grid + verdict + the wiki page."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from ww.backtest.engine import run_backtest
from ww.backtest.gate import _above_trailing_sma, _sma_rising, daily_gmi_series, green_state_machine, market_state_gate
from ww.backtest.metrics import compare, performance, rolling_excess_cagr

_DEFAULT = dict(gmi_threshold=4, confirm_in=2, confirm_out=2, require_stage2=False, require_st_up=False,
                gmi_source="reconstructed", red_etf=None, long_etf="QQQ", cost_bps=5.0)


def _qqq_30wk_filter(prices: pd.DataFrame, idx: pd.Index) -> pd.Series:
    qqq = prices["QQQ"].reindex(idx).ffill()
    wk = qqq.resample("W-FRI").last().dropna()
    sig_wk = _above_trailing_sma(wk, 30) & _sma_rising(wk, 30)
    return sig_wk.reindex(idx, method="ffill").fillna(False).astype(bool)


def _one_run(root, prices, *, start, end, cfg) -> dict:
    gmi = daily_gmi_series(root, prices, source=cfg["gmi_source"])
    sig = market_state_gate(gmi, prices, gmi_threshold=cfg["gmi_threshold"], confirm_in=cfg["confirm_in"],
                            confirm_out=cfg["confirm_out"], require_stage2=cfg["require_stage2"], require_st_up=cfg["require_st_up"])
    res = run_backtest(sig, prices, long_etf=cfg["long_etf"], red_etf=cfg["red_etf"], cost_bps_round_trip=cfg["cost_bps"],
                       start=start, end=end)
    m = performance(res.equity, signal=res.signal, trades=res.trades)
    cov = gmi.attrs.get("reported_coverage", None)
    return {"result": res, "metrics": m, "cfg": cfg, "reported_coverage": cov}


def verdict(default_m: dict, bench_m: dict, grid: list[dict]) -> str:
    """Apply the pre-stated criteria. 'adds value' iff Sharpe >= benchmark's AND |maxDD| <= 0.7*benchmark's AND
    not fragile across the grid middle. 'marginal' if it cuts drawdown but not Sharpe/CAGR. 'drag' if it
    underperforms Sharpe AND doesn't cut drawdown."""
    s, sb = default_m["sharpe"], bench_m["sharpe"]
    dd, ddb = abs(default_m["max_drawdown"]), abs(bench_m["max_drawdown"])
    cuts_dd = dd <= 0.7 * ddb if ddb > 0 else False
    beats_sharpe = s >= sb
    # fragility: in the grid (cost / lag / threshold variants), does the "beats_sharpe AND cuts_dd" survive most of them?
    survive = sum(1 for g in grid if g["metrics"]["sharpe"] >= sb and abs(g["metrics"]["max_drawdown"]) <= 0.7 * ddb) if ddb > 0 else 0
    robust = survive >= max(1, len(grid) // 2)
    if beats_sharpe and cuts_dd and robust:
        return f"adds value — Sharpe {s:.2f} >= {sb:.2f}, max-DD {dd:.0%} <= 0.7x{ddb:.0%}, robust across {survive}/{len(grid)} grid variants"
    if cuts_dd and not beats_sharpe:
        return f"marginal — cuts drawdown (max-DD {dd:.0%} vs {ddb:.0%}) but at a Sharpe/CAGR cost (Sharpe {s:.2f} vs {sb:.2f}); a stomach-vs-money trade"
    if (not beats_sharpe) and (not cuts_dd):
        return f"drag — underperforms on Sharpe ({s:.2f} vs {sb:.2f}) AND doesn't meaningfully cut drawdown ({dd:.0%} vs {ddb:.0%})"
    return f"mixed — Sharpe {s:.2f} vs {sb:.2f}, max-DD {dd:.0%} vs {ddb:.0%}, robust={robust}; read the grid"


def run_timing_overlay(root: Path, *, prices: pd.DataFrame, start: str | None, end: str | None,
                       cost_bps: float = 5.0, quick: bool = False) -> dict:
    root = Path(root)
    cfg = dict(_DEFAULT); cfg["cost_bps"] = cost_bps
    default = _one_run(root, prices, start=start, end=end, cfg=cfg)

    # benchmarks
    bh_qqq = run_backtest(pd.Series(True, index=prices.index), prices, long_etf="QQQ", cost_bps_round_trip=0.0, start=start, end=end)
    bh_spy = run_backtest(pd.Series(True, index=prices.index), prices, long_etf="SPY", cost_bps_round_trip=0.0, start=start, end=end)
    filt = run_backtest(_qqq_30wk_filter(prices, prices.index), prices, long_etf="QQQ", cost_bps_round_trip=cost_bps, start=start, end=end)
    benchmarks = {
        "buy_hold_qqq": performance(bh_qqq.equity),
        "buy_hold_spy": performance(bh_spy.equity),
        "qqq_30wk_filter": performance(filt.equity, signal=filt.signal, trades=filt.trades),
    }
    bench_m = benchmarks["buy_hold_qqq"]

    # variant grid (one dimension at a time vs the default)
    variants = []
    if not quick:
        for gt in (3, 6):
            variants.append((f"GMI>={gt}", {**cfg, "gmi_threshold": gt}))
        for ci, co in ((0, 0), (5, 5), (2, 1)):
            variants.append((f"confirm {ci}/{co}", {**cfg, "confirm_in": max(ci, 1), "confirm_out": max(co, 1)}))
        variants.append(("+Stage-2", {**cfg, "require_stage2": True}))
        variants.append(("+QQQ-short-term-up", {**cfg, "require_st_up": True}))
        variants.append(("+Stage-2 +ST-up", {**cfg, "require_stage2": True, "require_st_up": True}))
        variants.append(("reported GMI", {**cfg, "gmi_source": "reported"}))
        variants.append(("RED->SQQQ", {**cfg, "red_etf": "SQQQ"}))
        variants.append(("GREEN->TQQQ", {**cfg, "long_etf": "TQQQ"}))
        variants.append(("cost 20bps", {**cfg, "cost_bps": 20.0}))
        variants.append(("cost 0bps", {**cfg, "cost_bps": 0.0}))
    grid = []
    for label, vcfg in variants:
        try:
            run = _one_run(root, prices, start=start, end=end, cfg=vcfg)
            grid.append({"label": label, "metrics": run["metrics"]})
        except Exception as exc:  # noqa: BLE001 - a flaky variant shouldn't kill the report
            grid.append({"label": label, "metrics": {"error": str(exc), "sharpe": float("nan"), "max_drawdown": float("nan"), "cagr": float("nan")}})

    rex = rolling_excess_cagr(default["result"].equity, bh_qqq.equity, window_years=5)
    v = verdict(default["metrics"], bench_m, [g for g in grid if "error" not in g["metrics"]])
    equity = {"strategy": default["result"].equity, "buy_hold_qqq": bh_qqq.equity, "buy_hold_spy": bh_spy.equity}
    return {"default": default["metrics"], "default_signal": default["result"].signal, "benchmarks": benchmarks,
            "grid": grid, "verdict": v, "rolling_excess": rex, "equity": equity,
            "reported_coverage": default.get("reported_coverage")}


def _fmt(m: dict) -> str:
    return (f"CAGR {m.get('cagr',0):.1%} · maxDD {m.get('max_drawdown',0):.1%} · Sharpe {m.get('sharpe',0):.2f} · "
            f"Sortino {m.get('sortino',0):.2f} · Calmar {m.get('calmar',0):.2f}"
            + (f" · in-mkt {m['time_in_market']:.0%}" if 'time_in_market' in m else "")
            + (f" · {m['n_long_trades']} trades" if 'n_long_trades' in m else "")
            + (f" · win {m['win_rate']:.0%}" if 'win_rate' in m else ""))


def write_wiki_page(root: Path, results: dict, *, plot_url: str | None, period: tuple) -> Path:
    root = Path(root)
    d, b = results["default"], results["benchmarks"]["buy_hold_qqq"]
    rex = results["rolling_excess"]
    lines = []
    lines.append("---\ntitle: Backtest — the market-state timing overlay\ntype: methodology\nupdated: "
                 + pd.Timestamp.today().strftime("%Y-%m-%d") + "\nsources: []\n---\n")
    lines.append("# Backtest — does the GMI timing overlay beat buy-and-hold QQQ?\n")
    lines.append("**The rule (pre-stated, zero fitted parameters):** be long QQQ when the reconstructed [GMI](gmi.md) has been "
                 ">= 4 for two consecutive days; sit in cash when it has been <= 3 for two consecutive days. Signals on the close of "
                 "day D, executed at the next day's open (modelled as a 1-day lag, close-to-close). Cost: 5 bps per round trip; no "
                 "tax (an IRA). Period: " + f"{period[0]}-{period[1]}" + ". Benchmark: buy-and-hold QQQ. "
                 "**Verdict criteria, fixed in advance:** \"adds value\" iff the default beats B&H QQQ on Sharpe *and* has <= 0.7x its "
                 "max drawdown *and* the conclusion is robust across the variant grid; \"marginal\" if it cuts drawdown at a Sharpe/CAGR "
                 "cost; \"drag\" if it underperforms on Sharpe and doesn't cut drawdown. (Caveat: the reconstructed GMI reads optimistic "
                 "in declines -- ~78% GREEN/RED agreement with his reported GMI -- so this likely *understates* how defensive he actually was; "
                 "see the breadth-data design spec.)\n")
    lines.append(f"## Headline result\n\n- **Strategy:** {_fmt(d)}\n- **Buy-and-hold QQQ:** {_fmt(b)}\n- "
                 f"**Buy-and-hold SPY:** {_fmt(results['benchmarks']['buy_hold_spy'])}\n- "
                 f"**Plain 'QQQ > rising 30-week SMA' filter:** {_fmt(results['benchmarks']['qqq_30wk_filter'])}\n\n"
                 f"### Verdict: **{results['verdict']}**\n")
    # Reference the repo-stable copy of the chart (assets/backtest/equity_curve.png — committed; the
    # daily workflow stages it to the deployed site at the same relative path). The path is correct
    # relative to the *deployed* wiki.html (which is the only renderer of this page); raw-markdown
    # readers won't see the image render but the link is human-followable from the repo root.
    lines.append("\n![equity curve](assets/backtest/equity_curve.png)\n\n"
                 "*(Strategy vs buy-and-hold QQQ vs SPY, log scale, RED periods shaded"
                 + (f" — also at [{plot_url}]({plot_url}) for 72 h)" if plot_url else ")") + "*\n")
    lines.append("\n## Robustness grid\n\nEach row varies one dimension vs the default. **Picking the best-looking variant after the "
                 "fact would be data snooping** -- the headline is the default, full-period, no tuning.\n\n| variant | result |\n|---|---|\n"
                 + f"| **default (GMI>=4, 2/2 confirm, 5 bps)** | {_fmt(d)} |\n"
                 + "\n".join(f"| {g['label']} | {_fmt(g['metrics'])} |" for g in results["grid"]) + "\n")
    lines.append("\n## When did it help / hurt? (rolling 5-year strategy-CAGR minus QQQ-CAGR)\n\n"
                 + (("| 5y ending | excess CAGR |\n|---|---|\n" + "\n".join(
                     f"| {ts.date()} | {v:+.1%} |" for ts, v in rex.iloc[::126].items())) if len(rex) else "_(period too short for a 5-year window)_") + "\n")
    lines.append("\n## Limitations\n\n- The reconstructed GMI reads optimistic in declines (survivorship bias in the breadth universe) -- "
                 "so the strategy here is *less* defensive than Dr. Wish actually was; a faithful version would cut drawdown more (and "
                 "give back more on whipsaws). - 2007-start (the breadth reconstruction is thin before then). - 5-bps cost / no slippage "
                 "beyond that / no tax. - This is the *timing* layer only -- it does **not** test his GLB/WGB stock-selection signal (a "
                 "separate sub-project).\n\n## See also\n\n- [General Market Index (GMI)](gmi.md) · [Moving-average rules](moving-average-rules.md) · "
                 "[QQQ Short-Term Timing](qqq-short-term-timing.md) · [Trend-flip log](../history/trend-flip-log.md)\n\n## Sources\n\n_None -- "
                 "this page is a generated backtest report; the rules it tests are documented (and cited) on the linked methodology pages._\n")
    out = root / "wiki" / "methodology" / "backtest-timing-overlay.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
