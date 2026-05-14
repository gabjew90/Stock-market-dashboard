"""Build a self-contained single-day-deep-dive GMI playground HTML file.

Loads breadth + prices, recomputes GMI + components + gate state, fetches QQQ OHLC,
computes Day-N of QQQ short-term trend and Weinstein stage, and emits a single HTML
file with everything embedded as JSON.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from ww.backtest.gate import (
    _above_trailing_sma,
    daily_gmi_series,
    green_state_machine,
    _S10_FRAC,
    _NEW_HIGHS_MIN,
    _QQQ_DAILY_TREND_WINDOW,
    _QQQ_WEEKLY_TREND_WINDOW,
    _FUND_MA_WINDOW,
)


ROOT = Path(__file__).resolve().parents[1]
START = "2010-01-01"
QQQ_OHLC_CACHE = ROOT / "data" / "backtest" / "qqq_ohlc.parquet"
PRICES_CACHE = ROOT / "data" / "backtest" / "prices.parquet"


def _ensure_prices(tickers=("QQQ", "SPY", "TQQQ", "SQQQ")) -> pd.DataFrame:
    """Load `data/backtest/prices.parquet`; if missing or incomplete, fetch via yfinance."""
    if PRICES_CACHE.exists():
        df = pd.read_parquet(PRICES_CACHE)
        df.index = pd.to_datetime(df.index)
        if set(tickers) <= set(df.columns):
            return df
    import yfinance as yf
    print(f"prices cache miss — fetching {tickers} via yfinance…")
    raw = yf.download(list(tickers), interval="1d", period="max",
                      auto_adjust=False, group_by="ticker", progress=False, threads=True)
    out = {}
    for t in tickers:
        sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
        col = "Adj Close" if "Adj Close" in sub.columns else "Close"
        out[t] = sub[col].astype(float)
    df = pd.DataFrame(out).dropna(how="all")
    df.index = pd.to_datetime(df.index)
    PRICES_CACHE.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PRICES_CACHE)
    return df


def fetch_qqq_ohlc() -> pd.DataFrame:
    """Fetch QQQ OHLC from yfinance with split/dividend adjustment so all four series are on the same scale,
    cached. Returns a DataFrame indexed by date with open/high/low/close columns."""
    import yfinance as yf
    if QQQ_OHLC_CACHE.exists():
        cached = pd.read_parquet(QQQ_OHLC_CACHE)
        cached.index = pd.to_datetime(cached.index)
        if (pd.Timestamp.today().normalize() - cached.index.max()).days <= 3:
            return cached
    # auto_adjust=True → OHLC are all back-adjusted for dividends/splits, so the candle bodies and the MAs
    # (computed from prices.parquet's adj close) sit on the same scale.
    df = yf.download("QQQ", start="1999-01-01", auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0].lower() for c in df.columns]
    else:
        df.columns = [c.lower() for c in df.columns]
    df = df[["open", "high", "low", "close"]].dropna()
    df.index = pd.to_datetime(df.index)
    df.to_parquet(QQQ_OHLC_CACHE)
    return df


def _streak_and_state(daily_above: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Day count matching Dr. Wish's announcements: Day 1 is the trading day AFTER QQQ first crossed
    its 30-day SMA. He posts his blog after the close announcing "Day N" — the cross is detected on the
    prior session, the announcement (and Day 1) lands on the next session.

    Returns (day_count, side) where day_count = days since the most recent cross (inclusive of today,
    starting at 1 on the first trading day after the cross), side = 'up' / 'down'.
    """
    a = daily_above.fillna(False).astype(bool)
    # Effective regime today = yesterday's "above 30d" — i.e., today is Day N of the regime that was
    # established by yesterday's close.
    a_eff = a.shift(1, fill_value=False)
    side = a_eff.map(lambda v: "up" if v else "down")
    grp = (a_eff != a_eff.shift()).cumsum()
    day_count = a_eff.groupby(grp).cumcount() + 1
    return day_count, side


def _weinstein_stage(qqq: pd.Series, w10: pd.Series, w30: pd.Series, w30_slope_n: int = 4) -> pd.Series:
    """Stage 1/2/3/4 per Stan Weinstein, simplified to match Dr. Wish's actual usage:
      Stage 2 = price above rising 30wk          (advancing — only stage he buys long)
      Stage 4 = price below falling 30wk         (declining — defensive)
      Stage 3 = price above 30wk but 30wk flat / falling   (topping)
      Stage 1 = price below 30wk but 30wk flat / rising    (basing)
    The 10wk vs 30wk relationship is a separate confirmation he watches but isn't required
    for the stage call itself (see wiki/methodology/moving-average-rules.md).
    """
    above_30wk = (qqq > w30)
    slope_up = (w30 > w30.shift(w30_slope_n))
    stage = pd.Series(0, index=qqq.index, dtype=int)
    stage[above_30wk & slope_up] = 2
    stage[above_30wk & ~slope_up] = 3
    stage[~above_30wk & ~slope_up] = 4
    stage[~above_30wk & slope_up] = 1
    return stage


def build_payload() -> dict:
    bs = pd.read_parquet(ROOT / "data" / "breadth" / "breadth_series.parquet")
    bs["date"] = pd.to_datetime(bs["date"])
    bs = bs.set_index("date").sort_index()
    prices = _ensure_prices()
    if not isinstance(prices.index, pd.DatetimeIndex):
        prices = prices.set_index(pd.to_datetime(prices.index))
    prices = prices.sort_index()

    idx = bs.index
    qqq = prices["QQQ"].reindex(idx).ffill()
    spy = prices["SPY"].reindex(idx).ffill() if "SPY" in prices.columns else qqq
    fp = pd.read_parquet(ROOT / "data" / "breadth" / "fund_proxy.parquet")
    fp["date"] = pd.to_datetime(fp["date"])
    fund = fp.set_index("date")["fund_proxy"].reindex(idx).ffill()

    # QQQ OHLC for the chart (cached, auto-adjusted so all four series sit on the same scale as the MAs)
    print("fetching QQQ OHLC…")
    ohlc = fetch_qqq_ohlc().reindex(idx).ffill()
    qopen = ohlc["open"]
    qhigh = ohlc["high"]
    qlow = ohlc["low"]
    qclose_ohlc = ohlc["close"]  # used for the candle body so o/c are self-consistent

    c1 = (bs["s10_total"] > 0) & (bs["s10_higher"] >= _S10_FRAC * bs["s10_total"])
    c2 = bs["nasdaq_new_52w_highs"] >= _NEW_HIGHS_MIN
    c3 = _above_trailing_sma(qqq, _QQQ_DAILY_TREND_WINDOW)
    c4 = _above_trailing_sma(spy, _QQQ_DAILY_TREND_WINDOW)
    wk = qqq.resample("W-FRI").last().dropna()
    c5_wk = _above_trailing_sma(wk, _QQQ_WEEKLY_TREND_WINDOW)
    c5 = c5_wk.reindex(idx, method="ffill").fillna(False).astype(bool)
    c6 = _above_trailing_sma(fund, _FUND_MA_WINDOW)

    gmi = daily_gmi_series(ROOT, prices, source="reconstructed")
    state = green_state_machine(gmi)

    # MAs (Dr. Wish's canonical set)
    sma30 = qqq.rolling(30, min_periods=30).mean()
    wk_close = qqq.resample("W-FRI").last().dropna()
    wk10_s = wk_close.rolling(10, min_periods=10).mean()
    wk30_s = wk_close.rolling(30, min_periods=30).mean()
    sma_10wk = wk10_s.reindex(idx, method="ffill")
    sma_30wk = wk30_s.reindex(idx, method="ffill")

    # Day-N of QQQ short-term trend (QQQ vs 30d daily SMA — the 95%-fit proxy)
    daily_above_30d = (qqq > sma30)
    day_count, side = _streak_and_state(daily_above_30d)
    # The close on Day 1 of the current trend (i.e., (day_count - 1) bars back from this date)
    qq_vals = qqq.values
    day1_close_arr = np.empty(len(qq_vals))
    day1_date_arr = np.empty(len(qq_vals), dtype=object)
    for i, dn in enumerate(day_count.values):
        j = max(0, i - (int(dn) - 1))
        day1_close_arr[i] = qq_vals[j]
        day1_date_arr[i] = qqq.index[j].strftime("%Y-%m-%d")
    day1_close = pd.Series(day1_close_arr, index=qqq.index)
    day1_date = pd.Series(day1_date_arr, index=qqq.index)
    ret_since_day1 = (qqq / day1_close - 1.0) * 100

    # Weinstein stage
    stage = _weinstein_stage(qqq, sma_10wk, sma_30wk)

    # forward returns
    fwd1 = (qqq.shift(-1) / qqq - 1.0)
    fwd5 = (qqq.shift(-5) / qqq - 1.0)
    fwd10 = (qqq.shift(-10) / qqq - 1.0)
    fwd20 = (qqq.shift(-20) / qqq - 1.0)
    fwd60 = (qqq.shift(-60) / qqq - 1.0)

    df = pd.DataFrame({
        "gmi": gmi.astype(int, errors="ignore"),
        "c1": c1.astype(int), "c2": c2.astype(int), "c3": c3.astype(int),
        "c4": c4.astype(int), "c5": c5.astype(int), "c6": c6.astype(int),
        "state": state.astype(int),
        "qqq": qqq.round(2),
        "oo": qopen.round(2), "hh": qhigh.round(2), "ll": qlow.round(2), "cc": qclose_ohlc.round(2),
        "sma30": sma30.round(2),
        "wk10": sma_10wk.round(2),
        "wk30": sma_30wk.round(2),
        "day": day_count.astype(int),
        "side": side,
        "stage": stage.astype(int),
        "d1c": day1_close.round(2),
        "d1d": day1_date,
        "rd1": ret_since_day1.round(2),
        "s10_total": bs["s10_total"].astype(int),
        "s10_higher": bs["s10_higher"].astype(int),
        "new_highs": bs["nasdaq_new_52w_highs"].astype(int),
        "fwd1": (fwd1 * 100).round(2),
        "fwd5": (fwd5 * 100).round(2),
        "fwd10": (fwd10 * 100).round(2),
        "fwd20": (fwd20 * 100).round(2),
        "fwd60": (fwd60 * 100).round(2),
    })
    df = df.loc[START:].copy()

    # Stage-entry buttons: the FIRST day each calendar year that the market entered Stage 2 (advancing)
    # and the FIRST day it entered Stage 4 (declining). Lets the user jump to each major regime turn.
    stage_aligned = stage.loc[df.index]
    transitions = stage_aligned[stage_aligned != stage_aligned.shift(1)]
    seen_year_stage: set[tuple] = set()
    stage_flips: list[dict] = []
    for d, s in transitions.items():
        s = int(s)
        if s not in (2, 4):
            continue
        year = d.year
        key = (year, s)
        if key in seen_year_stage:
            continue
        seen_year_stage.add(key)
        stage_flips.append({"stage": s, "year": year, "d": d.strftime("%Y-%m-%d")})
    stage_flips.sort(key=lambda f: f["d"])  # chronological
    # Keep only the most recent 5 years to stay compact
    recent_years = sorted({f["year"] for f in stage_flips}, reverse=True)[:5]
    stage_flips = [f for f in stage_flips if f["year"] in recent_years]

    # Weekly OHLC bars (W-FRI: last completed week ends on Friday). Used by the weekly chart view.
    wk_o = qopen.resample("W-FRI").first()
    wk_h = qhigh.resample("W-FRI").max()
    wk_l = qlow.resample("W-FRI").min()
    wk_c = qclose_ohlc.resample("W-FRI").last()
    wk_df = pd.DataFrame({"o": wk_o, "h": wk_h, "l": wk_l, "c": wk_c}).dropna()
    wk_df = wk_df.loc[(wk_df.index >= pd.Timestamp(START))].copy()
    wk_df["m10"] = wk10_s.reindex(wk_df.index)
    wk_df["m30"] = wk30_s.reindex(wk_df.index)
    # Gate state on the last trading day of each week (used for red shading in weekly view)
    wk_df["s"] = state.resample("W-FRI").last().reindex(wk_df.index).ffill()
    weekly_rows = []
    for wd, wr in wk_df.iterrows():
        weekly_rows.append({
            "d": wd.strftime("%Y-%m-%d"),
            "o": None if pd.isna(wr["o"]) else round(float(wr["o"]), 2),
            "h": None if pd.isna(wr["h"]) else round(float(wr["h"]), 2),
            "l": None if pd.isna(wr["l"]) else round(float(wr["l"]), 2),
            "c": None if pd.isna(wr["c"]) else round(float(wr["c"]), 2),
            "m10": None if pd.isna(wr["m10"]) else round(float(wr["m10"]), 2),
            "m30": None if pd.isna(wr["m30"]) else round(float(wr["m30"]), 2),
            "s": int(wr["s"]) if not pd.isna(wr["s"]) else 1,
        })

    # For each daily row, the index of the weekly bar it belongs to (the next-Friday-or-later weekly bar).
    wk_index_array = wk_df.index
    wk_pos: dict[pd.Timestamp, int] = {wd: i for i, wd in enumerate(wk_index_array)}

    df.index = df.index.strftime("%Y-%m-%d")

    rows = []
    for d, r in df.iterrows():
        # Find weekly bar this daily date belongs to (next Friday ≥ this date).
        dt = pd.Timestamp(d)
        after = wk_index_array[wk_index_array >= dt]
        if len(after):
            wi = wk_pos[after[0]]
        elif len(wk_index_array):
            wi = len(wk_index_array) - 1
        else:
            wi = 0
        rows.append({
            "d": d, "wi": wi,
            "g": int(r["gmi"]) if not np.isnan(r["gmi"]) else 0,
            "c": [int(r[f"c{i}"]) for i in range(1, 7)],
            "s": int(r["state"]),
            "q": float(r["qqq"]) if not np.isnan(r["qqq"]) else None,
            "o": None if np.isnan(r["oo"]) else float(r["oo"]),
            "h": None if np.isnan(r["hh"]) else float(r["hh"]),
            "l": None if np.isnan(r["ll"]) else float(r["ll"]),
            "cl": None if np.isnan(r["cc"]) else float(r["cc"]),  # OHLC close; "c" key reserved for components array
            "m30": None if np.isnan(r["sma30"]) else float(r["sma30"]),
            "w10": None if np.isnan(r["wk10"]) else float(r["wk10"]),
            "w30": None if np.isnan(r["wk30"]) else float(r["wk30"]),
            "dn": int(r["day"]),
            "sd": r["side"],
            "st": int(r["stage"]),
            "d1c": None if np.isnan(r["d1c"]) else float(r["d1c"]),
            "d1d": r["d1d"],
            "rd1": None if np.isnan(r["rd1"]) else float(r["rd1"]),
            "n10t": int(r["s10_total"]) if not np.isnan(r["s10_total"]) else 0,
            "n10h": int(r["s10_higher"]) if not np.isnan(r["s10_higher"]) else 0,
            "nh": int(r["new_highs"]) if not np.isnan(r["new_highs"]) else 0,
            "f1": None if np.isnan(r["fwd1"]) else float(r["fwd1"]),
            "f5": None if np.isnan(r["fwd5"]) else float(r["fwd5"]),
            "f10": None if np.isnan(r["fwd10"]) else float(r["fwd10"]),
            "f20": None if np.isnan(r["fwd20"]) else float(r["fwd20"]),
            "f60": None if np.isnan(r["fwd60"]) else float(r["fwd60"]),
        })
    return {"rows": rows, "asof": df.index[-1], "stage_flips": stage_flips, "weekly": weekly_rows}


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GMI Daily — Dr. Wish methodology</title>
<style>
  :root {
    --bg: #0d1117;
    --panel: #161b22;
    --panel-2: #1c2330;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --green: #2ea043;
    --red: #f85149;
    --yellow: #d29922;
    --accent: #58a6ff;
    --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    font-size: 15px; line-height: 1.5; }
  /* shared top nav (matches wiki) */
  .pages-nav {
    position: sticky; top: 0; z-index: 100; display: flex; align-items: center;
    gap: 4px; padding: 10px 12px; background: rgba(13,17,23,0.95);
    backdrop-filter: blur(8px); border-bottom: 1px solid var(--border);
  }
  .pages-nav .brand { font-weight: 600; margin-right: 8px; font-size: 14px; }
  .pages-nav .brand .sub { color: var(--muted); font-weight: 400; font-size: 12px; margin-left: 6px; }
  .pages-nav a {
    color: var(--muted); text-decoration: none; padding: 4px 10px; border-radius: 999px;
    font-size: 12px; font-family: var(--mono); border: 1px solid transparent;
  }
  .pages-nav a.active { color: var(--text); border-color: var(--accent); background: rgba(88,166,255,0.18); }
  .pages-nav a:hover { color: var(--text); }
  .wrap { max-width: 820px; margin: 0 auto; padding: 16px; }
  h1 { font-size: 20px; margin: 0 0 4px; font-weight: 600; }
  h1 .sub { color: var(--muted); font-weight: 400; font-size: 13px; margin-left: 8px; }
  .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 14px; margin: 12px 0; }
  .small { color: var(--muted); font-size: 11px; font-family: var(--mono); }

  /* Hero — GMI + state + day-N + stage */
  .hero { display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: center; }
  .hero .num { font-family: var(--mono); font-size: 56px; font-weight: 700; line-height: 1; }
  .hero .denom { color: var(--muted); font-size: 24px; }
  .badge { display: inline-block; padding: 5px 12px; border-radius: 999px; font-weight: 600; font-size: 13px; letter-spacing: 0.4px; }
  .badge.green { background: rgba(46,160,67,0.18); color: var(--green); border: 1px solid rgba(46,160,67,0.4); }
  .badge.red { background: rgba(248,81,73,0.18); color: var(--red); border: 1px solid rgba(248,81,73,0.4); }
  .badge.yellow { background: rgba(210,153,34,0.18); color: var(--yellow); border: 1px solid rgba(210,153,34,0.4); }
  .meta { color: var(--muted); font-size: 13px; margin-top: 6px; }
  .meta b { color: var(--text); font-weight: 600; }

  /* Trend / stage callout */
  .callout { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
  .pill { display: inline-flex; align-items: center; gap: 6px; background: var(--panel-2);
    border: 1px solid var(--border); border-radius: 999px; padding: 5px 10px; font-size: 12px; font-family: var(--mono); }
  .pill b { color: var(--text); font-weight: 600; }
  .pill.up { color: var(--green); border-color: rgba(46,160,67,0.4); }
  .pill.down { color: var(--red); border-color: rgba(248,81,73,0.4); }
  .pill.s2 { color: var(--green); border-color: rgba(46,160,67,0.4); }
  .pill.s4 { color: var(--red); border-color: rgba(248,81,73,0.4); }
  .pill.s3, .pill.s1 { color: var(--yellow); border-color: rgba(210,153,34,0.4); }
  .stage-note { font-size: 12px; color: var(--muted); margin-top: 6px; font-style: italic; }

  /* Components grid */
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  @media (min-width: 560px) { .grid { grid-template-columns: 1fr 1fr 1fr; } }
  .comp { background: var(--panel-2); border: 1px solid var(--border); border-radius: 8px; padding: 10px; }
  .comp .name { font-size: 12px; color: var(--muted); margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center; gap: 4px; }
  .comp .mark { font-size: 22px; font-weight: 700; font-family: var(--mono); }
  .comp.on .mark { color: var(--green); }
  .comp.off .mark { color: var(--red); }
  .comp .detail { font-size: 12px; color: var(--muted); margin-top: 4px; font-family: var(--mono); }

  /* The little ? bubble — only this triggers tooltips */
  .qmark { display: inline-flex; align-items: center; justify-content: center;
    width: 18px; height: 18px; border-radius: 50%; background: rgba(88,166,255,0.22);
    color: var(--accent); font-size: 11px; font-weight: 700; cursor: pointer;
    user-select: none; border: none; padding: 0; line-height: 1; flex-shrink: 0; }
  .qmark:hover, .qmark:active { background: rgba(88,166,255,0.42); }

  /* Chart */
  .chart-wrap { position: relative; }
  .spark { width: 100%; height: 200px; display: block; }
  .chart-header { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 4px; }
  .red-chip { display: inline-flex; align-items: center; gap: 5px; padding: 3px 9px; border-radius: 999px;
    background: rgba(248,81,73,0.18); color: var(--red); border: 1px solid rgba(248,81,73,0.4);
    font-family: var(--mono); font-size: 11px; }

  /* Legend chips — chip toggles line; small ? next to it pops tooltip */
  .legend { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; font-size: 11px; font-family: var(--mono); align-items: center; }
  .legend-item { display: inline-flex; align-items: center; gap: 4px; }
  .chip { display: inline-flex; align-items: center; gap: 5px; cursor: pointer; color: var(--muted);
    user-select: none; border: 1px solid var(--border); border-radius: 999px; padding: 3px 9px; background: var(--panel-2); font-size: 11px; font-family: var(--mono); }
  .chip.on { color: var(--text); border-color: var(--accent); background: rgba(88,166,255,0.20); font-weight: 600; }
  .chip:hover { color: var(--text); }
  .legend .swatch { display: inline-block; width: 12px; height: 2px; }

  /* Date controls (now below chart) */
  .date-row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .date-row input[type=date] {
    background: var(--panel-2); color: var(--text); border: 1px solid var(--border);
    border-radius: 6px; padding: 6px 8px; font-family: var(--mono); font-size: 14px;
  }
  .date-row input[type=range] { flex: 1; min-width: 200px; accent-color: var(--accent); }
  .presets { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
  .presets button {
    background: var(--panel-2); color: var(--text); border: 1px solid var(--border);
    border-radius: 999px; padding: 4px 10px; font-size: 12px; cursor: pointer;
  }
  .presets button:hover { border-color: var(--accent); color: var(--accent); }

  /* Forward returns */
  table.fwd { width: 100%; border-collapse: collapse; font-family: var(--mono); font-size: 13px; }
  table.fwd th, table.fwd td { padding: 6px 4px; text-align: right; border-bottom: 1px solid var(--border); }
  table.fwd th:first-child, table.fwd td:first-child { text-align: left; color: var(--muted); }
  td.pos { color: var(--green); }
  td.neg { color: var(--red); }
  td.nv { color: var(--muted); }

  /* Prompt copy panel */
  .prompt-out { background: var(--panel-2); border: 1px solid var(--border); border-radius: 8px;
    padding: 12px; font-family: var(--mono); font-size: 13px; white-space: pre-wrap;
    color: var(--text); min-height: 80px; }
  .copy-row { display: flex; gap: 8px; align-items: center; margin-top: 8px; }
  .copy-btn { background: var(--accent); color: #0a0d12; border: none; border-radius: 6px;
    padding: 8px 14px; font-weight: 600; cursor: pointer; font-size: 13px; }
  .copy-btn:hover { filter: brightness(1.1); }
  .copy-status { color: var(--green); font-size: 12px; }
  .footer { color: var(--muted); font-size: 11px; margin-top: 16px; text-align: center; line-height: 1.6; }

  /* Floating popover (the tooltip bubble) */
  .pop { position: fixed; max-width: 280px; background: #0a0d12; border: 1px solid var(--accent);
    border-radius: 8px; padding: 10px 12px; font-size: 12px; line-height: 1.5; color: var(--text);
    z-index: 1000; box-shadow: 0 6px 20px rgba(0,0,0,0.6); display: none; }
  .pop.show { display: block; }
  .pop b { color: var(--accent); font-weight: 600; }
  .pop .close { position: absolute; top: 4px; right: 8px; cursor: pointer; color: var(--muted); font-size: 16px; }
  .pop .close:hover { color: var(--text); }
</style>
</head>
<body>
<nav class="pages-nav">
  <span class="brand">Dr. Wish<span class="sub">methodology</span></span>
  <a href="./" class="active">GMI Daily</a>
  <a href="./wiki.html">Wiki</a>
</nav>
<div class="wrap">
  <h1>GMI Daily<span class="sub">Dr. Wish methodology · reconstructed</span></h1>

  <!-- 1. Chart at the top -->
  <div class="panel">
    <div class="chart-header">
      <span class="small" id="chartTitle">QQQ — 6 months · daily candles</span>
      <span style="display:inline-flex; align-items:center; gap:6px;">
        <span class="legend-item" style="gap:4px;">
          <span class="chip on" id="viewDaily" data-view="daily">Daily</span>
          <span class="chip" id="viewWeekly" data-view="weekly">Weekly</span>
        </span>
        <button class="qmark" data-pop="redshade" aria-label="Red shading explanation">?</button>
      </span>
    </div>
    <div class="chart-wrap">
      <svg class="spark" id="spark" viewBox="0 0 800 200" preserveAspectRatio="none"></svg>
    </div>
    <div class="legend" id="legend">
      <!-- legend chips are rendered dynamically per view -->
    </div>
    <div class="small" style="margin-top:8px;">Tap any <b style="color:var(--accent)">?</b> for an explanation. Tap a legend chip to toggle a line.</div>
  </div>

  <!-- 2. Values + return since Day 1 of current ST trend -->
  <div class="panel" id="fwdPanel">
    <div class="small" style="display:flex; align-items:center; gap:6px; margin-bottom:6px;">
      <span>Indicator values on selected date</span>
      <button class="qmark" data-pop="vals" aria-label="Values">?</button>
    </div>
    <table class="fwd">
      <thead><tr><th>Indicator</th><th>Value</th><th>QQQ vs</th></tr></thead>
      <tbody>
        <tr><td>QQQ close</td><td id="vqqq">—</td><td class="nv">—</td></tr>
        <tr><td>30-day SMA</td><td id="vm30">—</td><td id="dm30">—</td></tr>
        <tr><td>10-week SMA</td><td id="vw10">—</td><td id="dw10">—</td></tr>
        <tr><td>30-week SMA</td><td id="vw30">—</td><td id="dw30">—</td></tr>
      </tbody>
    </table>
    <div class="small" style="display:flex; align-items:center; gap:6px; margin-top:14px; margin-bottom:4px;">
      <span>Return since Day 1 of current ST trend</span>
      <button class="qmark" data-pop="since" aria-label="Since Day 1">?</button>
    </div>
    <table class="fwd">
      <tbody>
        <tr><td>Day 1 of current ST trend</td><td id="sd1d">—</td></tr>
        <tr><td>Day 1 close</td><td id="sd1c">—</td></tr>
        <tr><td>Days elapsed</td><td id="sdn">—</td></tr>
        <tr><td><b>Return since Day 1</b></td><td id="srd1">—</td></tr>
      </tbody>
    </table>
  </div>

  <!-- 3. Date slider + regime-change shortcuts -->
  <div class="panel">
    <div class="date-row">
      <input type="date" id="datePick">
      <input type="range" id="dateSlider" min="0" max="0" value="0">
    </div>
    <div class="small" style="margin-top:8px; margin-bottom:4px;">
      Jump to first day of each Stage 2 / Stage 4 by year:
      <button class="qmark" data-pop="regime" aria-label="Stage buttons explained">?</button>
    </div>
    <div class="presets" id="presets"></div>
    <div class="small" id="dateLabel" style="margin-top:8px;">—</div>
  </div>

  <!-- 4. GMI hero (number + state + Day N + Stage) -->
  <div class="panel">
    <div class="hero">
      <div>
        <span class="num" id="gmiNum">0</span><span class="denom">/6</span>
        <button class="qmark" data-pop="gmi" aria-label="What is GMI">?</button>
      </div>
      <div>
        <span class="badge" id="stateBadge">—</span>
        <button class="qmark" data-pop="state" aria-label="What is the state" style="vertical-align:middle; margin-left:6px;">?</button>
      </div>
    </div>
    <div class="callout">
      <span class="pill" id="dayPill">Day — of —</span>
      <button class="qmark" data-pop="dayN" aria-label="Day N explanation">?</button>
      <span class="pill" id="stagePill">Stage —</span>
      <button class="qmark" data-pop="stage" aria-label="Stage explanation">?</button>
    </div>
    <div class="stage-note" id="stageNote">—</div>
  </div>

  <!-- 5. Components grid -->
  <div class="panel">
    <div class="small" style="margin-bottom:8px;">Six GMI components — tap <b style="color:var(--accent)">?</b> on any card for what it measures.</div>
    <div class="grid" id="components"></div>
  </div>

  <!-- Copy prompt -->
  <div class="panel">
    <div class="small">Prompt to copy back to Claude</div>
    <div class="prompt-out" id="prompt">—</div>
    <div class="copy-row">
      <button class="copy-btn" id="copyBtn">Copy prompt</button>
      <span class="copy-status" id="copyStatus"></span>
    </div>
  </div>

  <div class="footer">
    Reconstructed point-in-time GMI · Nasdaq-Trader universe + yfinance.
    <button class="qmark" data-pop="caveat" aria-label="Reconstruction caveat">?</button>
  </div>

  <!-- The popover bubble -->
  <div class="pop" id="pop"><span class="close" id="popClose">×</span><div id="popBody"></div></div>
</div>

<script>
const DATA = __DATA__;
const ROWS = DATA.rows;
const WEEKLY = DATA.weekly || [];
const STAGE_FLIPS = DATA.stage_flips || [];

let VIEW = "daily";  // "daily" or "weekly"

const COMPS = [
  {name:"1. Successful 10d new high"},
  {name:"2. ≥100 new 52w highs"},
  {name:"3. QQQ daily up-trend"},
  {name:"4. SPY daily up-trend"},
  {name:"5. QQQ weekly up-trend"},
  {name:"6. IBD-50 (FFTY) >50d MA"},
];

const dateMap = new Map();
ROWS.forEach((r, i) => dateMap.set(r.d, i));

const dateSlider = document.getElementById('dateSlider');
const datePick = document.getElementById('datePick');
dateSlider.max = String(ROWS.length - 1);
dateSlider.value = String(ROWS.length - 1);
datePick.min = ROWS[0].d;
datePick.max = ROWS[ROWS.length - 1].d;
datePick.value = ROWS[ROWS.length - 1].d;

const pBox = document.getElementById('presets');
// "Today" anchor first
const todayBtn = document.createElement('button');
todayBtn.textContent = "Today";
todayBtn.onclick = () => setIndex(ROWS.length - 1);
pBox.appendChild(todayBtn);
// Stage-entry buttons: first day of Stage 2 (advancing) and Stage 4 (declining) per year
STAGE_FLIPS.forEach(f => {
  const b = document.createElement('button');
  b.textContent = `ST${f.stage} ${f.year}`;
  if (f.stage === 2) {
    b.style.color = "#2ea043";
    b.style.borderColor = "rgba(46,160,67,0.5)";
  } else {
    b.style.color = "#f85149";
    b.style.borderColor = "rgba(248,81,73,0.5)";
  }
  b.title = `First day of Stage ${f.stage} (${f.stage === 2 ? "advancing" : "declining"}) in ${f.year} — ${f.d}`;
  b.onclick = () => setIndex(findNearestIndex(f.d));
  pBox.appendChild(b);
});

function findNearestIndex(dateStr) {
  if (dateMap.has(dateStr)) return dateMap.get(dateStr);
  let lo = 0, hi = ROWS.length - 1, best = 0;
  while (lo <= hi) {
    const m = (lo + hi) >> 1;
    if (ROWS[m].d <= dateStr) { best = m; lo = m + 1; } else { hi = m - 1; }
  }
  return best;
}

function setIndex(i) {
  i = Math.max(0, Math.min(ROWS.length - 1, i));
  dateSlider.value = String(i);
  datePick.value = ROWS[i].d;
  render(i);
}

dateSlider.addEventListener('input', e => render(Number(e.target.value)));
dateSlider.addEventListener('change', e => setIndex(Number(e.target.value)));
datePick.addEventListener('change', e => setIndex(findNearestIndex(e.target.value)));

function classifyState(s, g) {
  if (s === 1) return {label: "GREEN — in market", cls: "green"};
  if (g <= 2) return {label: "RED — sidelined", cls: "red"};
  return {label: "YELLOW — transition", cls: "yellow"};
}

const STAGE_INFO = {
  1: {name: "Stage 1 — Basing",     note: "Price below 30-week MA, but tape firming. Dr. Wish does not buy here.", cls: "s1"},
  2: {name: "Stage 2 — Advancing",  note: "Price above rising 30-week MA, 10wk > 30wk. Only stage he buys long.", cls: "s2"},
  3: {name: "Stage 3 — Topping",    note: "Price above 30-week but breadth weakening (10wk crossing under, or 30wk flattening). He sells into this.", cls: "s3"},
  4: {name: "Stage 4 — Declining",  note: "Price below falling 30-week, 10wk < 30wk. Defensive — cash or inverse. Got him out before 2000 and 2008.", cls: "s4"},
};

function buildPrompt(r) {
  const stateInfo = classifyState(r.s, r.g);
  const compBits = COMPS.map((c, i) => (r.c[i] ? "✓" : "✗") + " c" + (i+1)).join(" ");
  const dirWord = r.sd === "up" ? "up" : "down";
  const stageName = (STAGE_INFO[r.st] || {name:"Stage —"}).name;
  return [
    `GMI on ${r.d}: ${r.g}/6 · gate ${stateInfo.label}`,
    `Day ${r.dn} of QQQ short-term ${dirWord}-trend · ${stageName}`,
    `Components: ${compBits}`,
    `S10 = ${r.n10h}/${r.n10t} (≥50% needed); new 52w highs = ${r.nh} (≥100); QQQ close = ${r.q != null ? r.q.toFixed(2) : "—"}.`,
    "",
    "Given Dr. Wish's documented methodology, what is his most likely posture? Are any components or MAs borderline? Use only the wiki content as authority."
  ].join("\n");
}

// ============================================================================
// Chart drawing: HLC bars (doji-style — vertical H–L line + close tick on right)
// ============================================================================

const MA_COLORS = { qqq: "#58a6ff", m30: "#f0b429", w10: "#56d364", w30: "#bc8cff" };
const maOn = { qqq: true, m30: true, w10: true, w30: true };  // QQQ is always on

// Legend definitions per view (QQQ candles are always rendered — no chip needed)
const LEGEND = {
  daily: [
    {key: "m30", color: MA_COLORS.m30, label: "30-day SMA", pop: "m30"},
  ],
  weekly: [
    {key: "w10", color: MA_COLORS.w10, label: "10-week SMA", pop: "w10"},
    {key: "w30", color: MA_COLORS.w30, label: "30-week SMA", pop: "w30"},
  ],
};

function renderLegend() {
  const box = document.getElementById('legend');
  box.innerHTML = "";
  LEGEND[VIEW].forEach(item => {
    const wrap = document.createElement('span');
    wrap.className = "legend-item";
    const chip = document.createElement('span');
    chip.className = "chip" + (maOn[item.key] ? " on" : "");
    chip.dataset.key = item.key;
    chip.innerHTML = `<span class="swatch" style="background:${item.color}"></span>${item.label}`;
    chip.addEventListener('click', (e) => {
      e.stopPropagation();
      maOn[item.key] = !maOn[item.key];
      chip.classList.toggle('on', maOn[item.key]);
      drawSpark(Number(dateSlider.value));
    });
    const q = document.createElement('button');
    q.className = "qmark";
    q.dataset.pop = item.pop;
    q.setAttribute("aria-label", item.label);
    q.textContent = "?";
    wrap.appendChild(chip);
    wrap.appendChild(q);
    box.appendChild(wrap);
  });
}

function drawSpark(centerIdx) {
  const svg = document.getElementById('spark');
  svg.innerHTML = "";
  const W = 800, H = 200, PADX = 6, PADY_TOP = 4, PADY_BOT = 22;

  // Both views share the same ~6-month date window (locked axes across toggle).
  const dStart = Math.max(0, centerIdx - 100);
  const dEnd = Math.min(ROWS.length - 1, centerIdx + 26);
  const firstDate = ROWS[dStart].d;
  const lastDate = ROWS[dEnd].d;
  let slice, localCenter, daily;
  if (VIEW === "daily") {
    daily = true;
    slice = ROWS.slice(dStart, dEnd + 1).filter(r => r.h != null && r.l != null);
    localCenter = slice.findIndex(r => r.d === ROWS[centerIdx].d);
    if (localCenter < 0) localCenter = centerIdx - dStart;
  } else {
    daily = false;
    slice = WEEKLY.filter(r => r.d >= firstDate && r.d <= lastDate && r.h != null);
    if (slice.length < 2) return;
    const selWeekDate = WEEKLY[ROWS[centerIdx].wi].d;
    localCenter = slice.findIndex(r => r.d === selWeekDate);
    if (localCenter < 0) localCenter = slice.length - 1;
  }
  if (slice.length < 2) return;

  // ===== Y range (locked across views: always use daily H/L over the same date window,
  // plus the MAs from whichever view is active) =====
  const ys = [];
  if (maOn.qqq) {
    for (let i = dStart; i <= dEnd; i++) {
      const dr = ROWS[i];
      if (dr.h != null) ys.push(dr.h);
      if (dr.l != null) ys.push(dr.l);
    }
  }
  // Add the appropriate MAs to the range so they're always in view
  slice.forEach(r => {
    if (daily && maOn.m30 && r.m30 != null) ys.push(r.m30);
    if (!daily && maOn.w10 && r.m10 != null) ys.push(r.m10);
    if (!daily && maOn.w30 && r.m30 != null) ys.push(r.m30);
  });
  if (ys.length < 2) return;
  const ymin0 = Math.min(...ys), ymax0 = Math.max(...ys);
  const pad = (ymax0 - ymin0) * 0.05 || 1;
  const ymin = ymin0 - pad, ymax = ymax0 + pad;
  const yspan = ymax - ymin;
  const plotH = H - PADY_TOP - PADY_BOT;
  const plotW = W - 2 * PADX;
  const xAt = (i) => (i / (slice.length - 1)) * plotW + PADX;
  const yAt = (v) => H - PADY_BOT - ((v - ymin) / yspan) * plotH;
  const barW = plotW / slice.length;

  // ===== RED gate shading (works for both views — weekly uses end-of-week state) =====
  {
    let runStart = null;
    for (let i = 0; i < slice.length; i++) {
      const isRed = slice[i].s === 0;
      if (isRed && runStart == null) runStart = i;
      if ((!isRed || i === slice.length - 1) && runStart != null) {
        const x0 = xAt(runStart);
        const x1 = xAt(isRed ? i : i - 1);
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', x0);
        rect.setAttribute('y', 0);
        rect.setAttribute('width', Math.max(1, x1 - x0));
        rect.setAttribute('height', H - PADY_BOT);
        rect.setAttribute('fill', 'rgba(248,81,73,0.12)');
        svg.appendChild(rect);
        runStart = null;
      }
    }
  }

  // ===== MA lines (only the ones relevant to the current view) =====
  function plotLine(seriesKey, color, width, alpha) {
    let d = "", started = false;
    slice.forEach((r, i) => {
      const v = r[seriesKey];
      if (v == null) { started = false; return; }
      d += (!started ? "M" : "L") + xAt(i).toFixed(1) + "," + yAt(v).toFixed(1) + " ";
      started = true;
    });
    if (!d) return;
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', d);
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', color);
    path.setAttribute('stroke-width', String(width));
    path.setAttribute('stroke-opacity', String(alpha));
    svg.appendChild(path);
  }
  if (daily && maOn.m30) plotLine("m30", MA_COLORS.m30, 1.4, 0.85);
  if (!daily && maOn.w30) plotLine("m30", MA_COLORS.w30, 1.6, 0.9);
  if (!daily && maOn.w10) plotLine("m10", MA_COLORS.w10, 1.4, 0.85);

  // ===== Candles =====
  if (maOn.qqq) {
    const bodyW = Math.max(2.5, barW * 0.7);
    const GREEN = "#2ea043", RED = "#f85149";
    slice.forEach((r, i) => {
      const cl = daily ? r.cl : r.c;  // daily rows use "cl" (avoid collision with components array "c")
      if (r.o == null || r.h == null || r.l == null || cl == null) return;
      const x = xAt(i);
      const yh = yAt(r.h), yl = yAt(r.l), yo = yAt(r.o), yc = yAt(cl);
      const up = cl >= r.o;
      const color = up ? GREEN : RED;
      const wick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      wick.setAttribute('x1', x); wick.setAttribute('x2', x);
      wick.setAttribute('y1', yh); wick.setAttribute('y2', yl);
      wick.setAttribute('stroke', color); wick.setAttribute('stroke-width', '1');
      svg.appendChild(wick);
      const bodyTop = Math.min(yo, yc);
      const bodyH = Math.max(1, Math.abs(yc - yo));
      const body = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      body.setAttribute('x', x - bodyW / 2);
      body.setAttribute('y', bodyTop);
      body.setAttribute('width', bodyW);
      body.setAttribute('height', bodyH);
      body.setAttribute('fill', color);
      svg.appendChild(body);
    });
  }
  // In the daily view the candle "close" is r.cl (OHLC close); in weekly it's r.c. Make sure daily slice has r.c too:
  // We map daily r.cl -> r.c just-in-time so the candle code above works the same.

  // ===== Selected-date marker =====
  if (localCenter >= 0 && localCenter < slice.length) {
    const r = slice[localCenter];
    const x = xAt(localCenter);
    const vline = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    vline.setAttribute('x1', x); vline.setAttribute('x2', x);
    vline.setAttribute('y1', 0); vline.setAttribute('y2', H - PADY_BOT);
    vline.setAttribute('stroke', '#e6edf3'); vline.setAttribute('stroke-width', '1.2');
    vline.setAttribute('stroke-dasharray', '3,3');
    vline.setAttribute('stroke-opacity', '0.85');
    svg.appendChild(vline);
    const lab = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    lab.setAttribute('y', H - 6);
    lab.setAttribute('text-anchor', 'middle'); lab.setAttribute('font-size', '10');
    lab.setAttribute('font-family', 'ui-monospace,Menlo,Consolas,monospace');
    lab.setAttribute('fill', '#e6edf3');
    lab.textContent = r.d;
    const halfW = 40;
    let lx = x;
    if (lx - halfW < 4) lx = halfW + 4;
    if (lx + halfW > W - 4) lx = W - halfW - 4;
    lab.setAttribute('x', lx);
    svg.appendChild(lab);
  }

  // ===== X-axis date labels =====
  const tickPositions = [0, Math.floor(slice.length*0.25), Math.floor(slice.length*0.5), Math.floor(slice.length*0.75), slice.length - 1];
  tickPositions.forEach((i, k) => {
    if (i < 0 || i >= slice.length) return;
    const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    const x = xAt(i);
    t.setAttribute('x', x);
    t.setAttribute('y', H - 18);
    t.setAttribute('text-anchor', k === 0 ? 'start' : (k === 4 ? 'end' : 'middle'));
    t.setAttribute('font-size', '9');
    t.setAttribute('font-family', 'ui-monospace,Menlo,Consolas,monospace');
    t.setAttribute('fill', '#8b949e');
    t.textContent = slice[i].d.slice(0, 7);
    svg.appendChild(t);
    const tk = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    tk.setAttribute('x1', x); tk.setAttribute('x2', x);
    tk.setAttribute('y1', H - PADY_BOT); tk.setAttribute('y2', H - PADY_BOT + 3);
    tk.setAttribute('stroke', '#8b949e'); tk.setAttribute('stroke-width', '0.7');
    svg.appendChild(tk);
  });
  const base = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  base.setAttribute('x1', PADX); base.setAttribute('x2', W - PADX);
  base.setAttribute('y1', H - PADY_BOT); base.setAttribute('y2', H - PADY_BOT);
  base.setAttribute('stroke', '#30363d'); base.setAttribute('stroke-width', '0.7');
  svg.appendChild(base);
}

// ============================================================================
// Render
// ============================================================================

function render(i) {
  const r = ROWS[i];
  const stateInfo = classifyState(r.s, r.g);

  document.getElementById('dateLabel').textContent = `${r.d}  ·  trading day ${i + 1} of ${ROWS.length}`;
  document.getElementById('gmiNum').textContent = String(r.g);
  const badge = document.getElementById('stateBadge');
  badge.textContent = stateInfo.label;
  badge.className = "badge " + stateInfo.cls;
  // Day-N pill
  const dayPill = document.getElementById('dayPill');
  const arrow = r.sd === "up" ? "▲" : "▼";
  dayPill.innerHTML = `${arrow} <b>Day ${r.dn}</b> of QQQ short-term <b>${r.sd}-trend</b>`;
  dayPill.className = "pill " + (r.sd === "up" ? "up" : "down");

  // Stage pill
  const stagePill = document.getElementById('stagePill');
  const si = STAGE_INFO[r.st] || {name: "Stage —", note: "", cls: ""};
  stagePill.innerHTML = `<b>${si.name}</b>`;
  stagePill.className = "pill " + si.cls;
  document.getElementById('stageNote').textContent = si.note;

  // Components
  const cBox = document.getElementById('components');
  cBox.innerHTML = "";
  COMPS.forEach((c, k) => {
    const on = r.c[k] === 1;
    const d = document.createElement('div');
    d.className = "comp " + (on ? "on" : "off");
    let detail = "";
    if (k === 0) detail = `${r.n10h}/${r.n10t}`;
    else if (k === 1) detail = `${r.nh} highs`;
    else detail = on ? "above" : "below";
    d.innerHTML = `
      <div class="name">
        <span>${c.name}</span>
        <button class="qmark" data-pop="c${k+1}" aria-label="info">?</button>
      </div>
      <div class="mark">${on ? "✓" : "✗"}</div>
      <div class="detail">${detail}</div>`;
    cBox.appendChild(d);
  });

  // Values (close + each MA, with QQQ vs MA spread)
  const setVal = (id, v) => {
    const el = document.getElementById(id);
    el.textContent = v == null ? "—" : "$" + v.toFixed(2);
  };
  const setSpread = (id, q, m) => {
    const el = document.getElementById(id);
    if (q == null || m == null) { el.textContent = "—"; el.className = "nv"; return; }
    const d = (q - m) / m * 100;
    const above = q > m;
    el.textContent = (d >= 0 ? "+" : "") + d.toFixed(2) + "% " + (above ? "above" : "below");
    el.className = above ? "pos" : "neg";
  };
  const qClose = r.cl != null ? r.cl : r.q;
  setVal('vqqq', qClose);
  setVal('vm30', r.m30); setSpread('dm30', qClose, r.m30);
  setVal('vw10', r.w10); setSpread('dw10', qClose, r.w10);
  setVal('vw30', r.w30); setSpread('dw30', qClose, r.w30);

  // Return since Day 1 of current ST trend
  document.getElementById('sd1d').textContent = r.d1d ? `${r.d1d} (ST ${r.sd === "up" ? "▲" : "▼"})` : "—";
  document.getElementById('sd1c').textContent = r.d1c != null ? "$" + r.d1c.toFixed(2) : "—";
  document.getElementById('sdn').textContent = r.dn ? `Day ${r.dn}` : "—";
  const srd1 = document.getElementById('srd1');
  if (r.rd1 == null) { srd1.textContent = "—"; srd1.className = "nv"; }
  else {
    srd1.textContent = (r.rd1 >= 0 ? "+" : "") + r.rd1.toFixed(2) + "%";
    srd1.className = r.rd1 >= 0 ? "pos" : "neg";
  }

  drawSpark(i);
  document.getElementById('prompt').textContent = buildPrompt(r);
}

// ============================================================================
// Tooltip popover system — only the small ? button triggers it
// ============================================================================

const POP = {
  gmi: "<b>GMI — General Market Index</b><br>Dr. Wish's daily 0–6 score of six market-health components. ≥4 for 2 consecutive days flips the gate GREEN (willing to buy long). ≤3 for 2 days flips RED (defensive — cash or hedge).",
  state: "<b>Market state — GREEN / YELLOW / RED</b><br>Computed from the GMI with a 2-day confirmation rule. GREEN = 2 consecutive days ≥4. RED = 2 consecutive days <4 and not recovered. YELLOW = transition (GMI 3).",
  dayN: "<b>Day N of QQQ short-term trend</b><br>The count of consecutive trading days QQQ has been on its current side of the 30-day SMA. Resets to 1 when QQQ crosses through the line on a closing basis. This is the trigger Dr. Wish announces in every blog post title (e.g. 'Day 22 of QQQ short-term up-trend').<br><br>Note: 95% empirical fit to his Day-1 announcements; he never published the exact rule, this is the best-supported proxy.",
  stage: "<b>Weinstein stage</b><br>The four-stage classification from Stan Weinstein, used by Dr. Wish for the long-term picture:<br><b>Stage 1 — Basing</b>: price below 30wk, MA flat/rising. No new buys.<br><b>Stage 2 — Advancing</b>: price above rising 30wk + 10wk > 30wk. <i>Only stage he buys long.</i><br><b>Stage 3 — Topping</b>: price above 30wk but breadth weakening. Sells into this.<br><b>Stage 4 — Declining</b>: price below falling 30wk + 10wk < 30wk. Defensive.",
  redshade: "<b>RED-shaded periods</b><br>Days when the GMI gate is RED. Per Dr. Wish this is when he is <b>out of long positions</b>, in cash, or hedged. Notice these are short and rare in bull runs, long and broad in declines.",
  qqq: "<b>QQQ candles</b><br>Standard OHLC candles. <span style='color:#2ea043;font-weight:600'>Green</span> = close ≥ open. <span style='color:#f85149;font-weight:600'>Red</span> = close &lt; open. Wick = high–low; body = open–close.<br><br><b>Daily view:</b> ~126 daily candles (6 months) centered on selected day.<br><b>Weekly view:</b> ~50 Friday-close candles (1 year) — this is the timeframe Dr. Wish actually uses for his 10:30 weekly chart.",
  m30: "<b>30-day SMA (daily)</b><br>The daily short-term trend anchor. QQQ closing above = ST up; below = ST down. Drives the Day-N count and components 3 & 4 of the GMI.<br><br>Quantitatively: 95% of his published Day-1 flip announcements (2024–2026) line up with QQQ crossing this line.",
  w10: "<b>10-week SMA (weekly chart)</b><br>His medium-term hold line. Computed on Friday weekly closes. The <b>10wk crossing above 30wk</b> is his bull re-entry signal (confirmed live 2025-06 and 2026-05). The <b>10wk crossing below 30wk</b> confirms Stage 4 onset (April 2025 tariff decline).",
  w30: "<b>30-week SMA (weekly chart)</b><br>Dr. Wish's most important MA. Stan Weinstein's classic. Got him out before 2000 and 2008. Price above + line rising = Stage 2 uptrend — the only stage he buys long.",
  c1: "<b>Successful 10-day new high</b><br>Component 1 of GMI. Fires when ≥50% of stocks that hit a new 52-week high 10 trading days ago closed higher today. Tests whether breakouts are still being rewarded.",
  c2: "<b>≥100 new 52-week highs</b><br>Component 2 of GMI. Fires when more than 100 US stocks hit a new 52-week high today. Tests breadth of advance — a healthy bull has wide participation.",
  c3: "<b>QQQ daily up-trend</b><br>Component 3 of GMI. Reconstructed as QQQ close above its 30-day SMA. The Nasdaq-100's short-term trend.",
  c4: "<b>SPY daily up-trend</b><br>Component 4 of GMI. Reconstructed as SPY close above its 30-day SMA. The S&amp;P 500's short-term trend.",
  c5: "<b>QQQ weekly up-trend (Stage 2)</b><br>Component 5 of GMI. QQQ's weekly close above its 30-week SMA. The long-term Stage-2 anchor.",
  c6: "<b>IBD-50 above 50-day MA</b><br>Component 6 of GMI. Tracks whether the IBD Mutual Fund Index sits above its 50-day MA. Proxied here by FFTY (the IBD-50 ETF) spliced onto a basket of growth mutual funds for pre-2015 history.",
  regime: "<b>Stage-entry shortcuts</b><br>Each button jumps to the <b>first day each calendar year</b> the market entered a given Weinstein stage:<br><br><b style='color:#2ea043'>ST2 YYYY</b> = first day of Stage 2 (advancing) that year — when price moved above a rising 30-week SMA and 10wk &gt; 30wk. Only stage Dr. Wish buys long.<br><br><b style='color:#f85149'>ST4 YYYY</b> = first day of Stage 4 (declining) that year — when price fell below a falling 30-week SMA and 10wk &lt; 30wk. Cash / defensive trigger.<br><br>Not every year has both — sustained bull markets skip Stage 4 entries entirely.",
  since: "<b>Return since Day 1</b><br>Day 1 = the most recent day QQQ crossed its 30-day SMA (Dr. Wish's daily ST-trend signal). This box shows how much QQQ has moved since then to the close on the selected date.<br><br>A long-running positive return is a Stage-2 ride; a steep negative return is a Stage-4 leg. Watch for fading momentum near the end of a long streak.",
  vals: "<b>Indicator values on the selected date</b><br>The exact QQQ close on that day plus each of Dr. Wish's three canonical MAs, with the percentage spread (QQQ above or below each MA). Use this to read the chart precisely instead of eyeballing.",
  fwd: "<b>Forward QQQ returns</b><br>What QQQ actually did 1, 5, 10, 20, and 60 trading days after the selected date. Lets you check 'if I had acted on this reading, what would have happened?' Blank for dates where the window hasn't closed yet.",
  caveat: "<b>Reconstruction caveat</b><br>This GMI is rebuilt from public data point-in-time. Match vs Dr. Wish's posted GMI: exact ~20% of days; within ±1 ~72%; correlation ~0.60. Systematically a touch optimistic in fast declines because of survivorship bias. Treat the number as directional, not precise.",
};

const popEl = document.getElementById('pop');
const popBody = document.getElementById('popBody');
document.getElementById('popClose').addEventListener('click', (e) => { e.stopPropagation(); popEl.classList.remove('show'); });

// Tooltip triggers — ONLY <button class="qmark"> with data-pop
document.addEventListener('click', (e) => {
  const trigger = e.target.closest('button.qmark[data-pop]');
  if (trigger) {
    e.stopPropagation();
    const key = trigger.dataset.pop;
    popBody.innerHTML = POP[key] || "(no info)";
    popEl.classList.add('show');
    const rect = trigger.getBoundingClientRect();
    const pw = 300;
    let left = rect.left + rect.width / 2 - pw / 2;
    let top = rect.bottom + 8;
    if (left < 8) left = 8;
    if (left + pw > window.innerWidth - 8) left = window.innerWidth - pw - 8;
    popEl.style.left = left + "px";
    popEl.style.top = top + "px";
    popEl.style.maxWidth = Math.min(300, window.innerWidth - 16) + "px";
    // recheck vertical fit
    requestAnimationFrame(() => {
      const ph = popEl.offsetHeight;
      if (top + ph > window.innerHeight - 8) {
        let nt = rect.top - ph - 8;
        if (nt < 8) nt = 8;
        popEl.style.top = nt + "px";
      }
    });
    return;
  }
  if (!e.target.closest('#pop')) popEl.classList.remove('show');
});

// Daily / Weekly view toggle
document.querySelectorAll('[data-view]').forEach(el => {
  el.addEventListener('click', (e) => {
    e.stopPropagation();
    const v = el.dataset.view;
    if (v === VIEW) return;
    VIEW = v;
    document.querySelectorAll('[data-view]').forEach(b => b.classList.toggle('on', b.dataset.view === VIEW));
    document.getElementById('chartTitle').textContent =
      VIEW === "daily" ? "QQQ — 6 months · daily candles + 30-day SMA"
                       : "QQQ — 1 year · weekly candles + 10-week & 30-week SMA";
    renderLegend();
    drawSpark(Number(dateSlider.value));
  });
});

renderLegend();

document.getElementById('copyBtn').addEventListener('click', async () => {
  const txt = document.getElementById('prompt').textContent;
  try {
    await navigator.clipboard.writeText(txt);
    document.getElementById('copyStatus').textContent = "Copied!";
    setTimeout(() => { document.getElementById('copyStatus').textContent = ""; }, 1500);
  } catch (e) {
    document.getElementById('copyStatus').textContent = "Press & hold to copy";
  }
});

setIndex(ROWS.length - 1);
</script>
</body>
</html>
"""


def main() -> None:
    payload = build_payload()
    out = TEMPLATE.replace("__DATA__", json.dumps(payload, separators=(",", ":")))
    target = ROOT / "gmi_playground_daily.html"
    target.write_text(out, encoding="utf-8")
    print(f"wrote {target} — {len(out):,} bytes — {len(payload['rows'])} rows — asof {payload['asof']}")


if __name__ == "__main__":
    main()
