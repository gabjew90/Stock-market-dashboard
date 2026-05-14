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
    # Track Day-1 close for QQQ + the two leveraged ETFs (TQQQ 3×, SQQQ -3×) so the user can
    # see the actual % move since Day 1 in each vehicle.
    qq_vals = qqq.values
    tq_series = prices["TQQQ"].reindex(idx).ffill() if "TQQQ" in prices.columns else pd.Series(np.nan, index=idx)
    sq_series = prices["SQQQ"].reindex(idx).ffill() if "SQQQ" in prices.columns else pd.Series(np.nan, index=idx)
    tq_vals = tq_series.values
    sq_vals = sq_series.values
    day1_close_arr = np.empty(len(qq_vals))
    day1_date_arr = np.empty(len(qq_vals), dtype=object)
    day1_tq_arr = np.empty(len(qq_vals))
    day1_sq_arr = np.empty(len(qq_vals))
    for i, dn in enumerate(day_count.values):
        j = max(0, i - (int(dn) - 1))
        day1_close_arr[i] = qq_vals[j]
        day1_date_arr[i] = qqq.index[j].strftime("%Y-%m-%d")
        day1_tq_arr[i] = tq_vals[j]
        day1_sq_arr[i] = sq_vals[j]
    day1_close = pd.Series(day1_close_arr, index=qqq.index)
    day1_date = pd.Series(day1_date_arr, index=qqq.index)
    day1_tq = pd.Series(day1_tq_arr, index=qqq.index)
    day1_sq = pd.Series(day1_sq_arr, index=qqq.index)
    ret_since_day1 = (qqq / day1_close - 1.0) * 100
    ret_since_day1_tq = (tq_series / day1_tq - 1.0) * 100
    ret_since_day1_sq = (sq_series / day1_sq - 1.0) * 100

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
        "rd1_tq": ret_since_day1_tq.round(2),
        "rd1_sq": ret_since_day1_sq.round(2),
        "s10_total": bs["s10_total"].astype(int),
        "s10_higher": bs["s10_higher"].astype(int),
        "new_highs": bs["nasdaq_new_52w_highs"].astype(int),
        "t2108": bs["t2108_nyse"].round(1),
        "fwd1": (fwd1 * 100).round(2),
        "fwd5": (fwd5 * 100).round(2),
        "fwd10": (fwd10 * 100).round(2),
        "fwd20": (fwd20 * 100).round(2),
        "fwd60": (fwd60 * 100).round(2),
    })
    df = df.loc[START:].copy()

    # Long-trend shortcuts: every ST trend (QQQ above/below 30d SMA) that lasted >= 30 trading days,
    # plus the most recent N for the jump menu.
    dc = day_count.loc[df.index]
    sd = side.loc[df.index]
    # Find each trend's Day 1 (where day_count == 1) and its full length.
    day1_mask = (dc == 1)
    day1_dates = dc.index[day1_mask].tolist()
    long_trends: list[dict] = []
    for i, start in enumerate(day1_dates):
        end = day1_dates[i + 1] if i + 1 < len(day1_dates) else dc.index[-1]
        # length = the max day_count between start and end (exclusive of next start)
        seg = dc.loc[start:end]
        if i + 1 < len(day1_dates):
            seg = seg.iloc[:-1]   # drop the next-trend's Day 1
        length = int(seg.max()) if len(seg) else 0
        if length < 30:
            continue
        long_trends.append({
            "d": start.strftime("%Y-%m-%d"),
            "len": length,
            "dir": sd.loc[start],
        })
    # keep most recent 8 long trends (chronological, newest first)
    long_trends.sort(key=lambda f: f["d"], reverse=True)
    long_trends = long_trends[:8]

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
            "rd1tq": None if np.isnan(r["rd1_tq"]) else float(r["rd1_tq"]),
            "rd1sq": None if np.isnan(r["rd1_sq"]) else float(r["rd1_sq"]),
            "n10t": int(r["s10_total"]) if not np.isnan(r["s10_total"]) else 0,
            "n10h": int(r["s10_higher"]) if not np.isnan(r["s10_higher"]) else 0,
            "nh": int(r["new_highs"]) if not np.isnan(r["new_highs"]) else 0,
            "t": None if np.isnan(r["t2108"]) else float(r["t2108"]),
            "f1": None if np.isnan(r["fwd1"]) else float(r["fwd1"]),
            "f5": None if np.isnan(r["fwd5"]) else float(r["fwd5"]),
            "f10": None if np.isnan(r["fwd10"]) else float(r["fwd10"]),
            "f20": None if np.isnan(r["fwd20"]) else float(r["fwd20"]),
            "f60": None if np.isnan(r["fwd60"]) else float(r["fwd60"]),
        })
    return {"rows": rows, "asof": df.index[-1], "long_trends": long_trends, "weekly": weekly_rows}


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Stock market dashboard — GMI Daily</title>
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

  /* Compact Since-Day-1 strip (replaces the old indicator-values + returns table) */
  .since-panel { padding: 12px 14px; }
  .since-header { display: flex; align-items: center; gap: 6px; font-size: 11px;
    color: var(--muted); font-family: var(--mono); text-transform: uppercase;
    letter-spacing: 0.6px; margin-bottom: 6px; }
  .since-meta { font-size: 13px; color: var(--text); margin-bottom: 10px;
    font-family: var(--mono); }
  .since-meta b { font-weight: 600; }
  .since-meta .sub { color: var(--muted); }
  .since-returns { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
  .since-cell { background: var(--panel-2); border: 1px solid var(--border);
    border-radius: 8px; padding: 8px 10px; display: flex; flex-direction: column; align-items: center; }
  .since-lbl { font-size: 10px; color: var(--muted); font-family: var(--mono);
    letter-spacing: 0.5px; }
  .since-val { font-size: 18px; font-weight: 700; font-family: var(--mono);
    line-height: 1.1; margin-top: 2px; }
  .since-val.pos { color: var(--green); }
  .since-val.neg { color: var(--red); }
  .since-val.nv { color: var(--muted); }

  /* Top market-state row: GMI + T2108 cards side by side */
  .state-row { display: grid; grid-template-columns: 1fr; gap: 12px; }
  @media (min-width: 640px) { .state-row { grid-template-columns: 1fr 1fr; } }
  .state-row > .panel { margin: 0; }   /* overrides default .panel margin so the row gap controls spacing */
  .state-card { display: flex; flex-direction: column; }
  .panel-title { font-size: 12px; color: var(--muted); font-family: var(--mono);
    text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px;
    display: flex; align-items: center; gap: 6px; }

  /* T2108 gauge bar */
  .t-bar { position: relative; width: 100%; height: 8px; border-radius: 999px;
    margin-top: 10px; overflow: visible;
    background: linear-gradient(to right,
      rgba(46,160,67,0.55) 0%, rgba(46,160,67,0.55) 10%,
      rgba(46,160,67,0.15) 10%, rgba(46,160,67,0.15) 30%,
      rgba(139,148,158,0.22) 30%, rgba(139,148,158,0.22) 70%,
      rgba(248,81,73,0.15) 70%, rgba(248,81,73,0.15) 80%,
      rgba(248,81,73,0.55) 80%, rgba(248,81,73,0.55) 100%); }
  .t-bar-fill { position: absolute; top: -2px; bottom: -2px; width: 3px;
    background: var(--text); border-radius: 2px; left: 0%;
    transition: left 0.2s ease; box-shadow: 0 0 0 2px var(--bg); }
  .t-scale { display: flex; justify-content: space-between; font-family: var(--mono);
    font-size: 9px; color: var(--muted); margin-top: 6px; gap: 4px; flex-wrap: wrap; }

  /* Compact components row (lives inside the GMI hero pane) */
  .comps-row {
    display: grid; grid-template-columns: repeat(6, 1fr); gap: 4px;
    margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border);
  }
  @media (max-width: 460px) { .comps-row { grid-template-columns: repeat(3, 1fr); } }
  .comp {
    background: var(--panel-2); border: 1px solid var(--border); border-radius: 6px;
    padding: 6px 4px; text-align: center; cursor: pointer; user-select: none;
    position: relative;
  }
  .comp .name { font-size: 10px; color: var(--muted); font-family: var(--mono); margin-bottom: 2px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .comp .mark { font-size: 16px; font-weight: 700; font-family: var(--mono); line-height: 1.1; }
  .comp.on { border-color: rgba(46,160,67,0.45); }
  .comp.on .mark { color: var(--green); }
  .comp.off { border-color: rgba(248,81,73,0.35); }
  .comp.off .mark { color: var(--red); }
  .comp .detail { font-size: 9px; color: var(--muted); font-family: var(--mono); margin-top: 1px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

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
  .presets { margin-top: 10px; }
  .presets button {
    background: var(--panel-2); color: var(--text); border: 1px solid var(--border);
    border-radius: 999px; padding: 5px 12px; font-size: 12px; cursor: pointer;
    font-family: var(--mono);
  }
  .presets button:hover { border-color: var(--accent); color: var(--accent); }
  /* Navigation row: [Prev] [Today] [Next] [Day 1 current] */
  .nav-row { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
  .nav-row .nav-arrow { padding: 5px 10px; min-width: 56px; }
  .nav-row .nav-day1 { font-weight: 600; margin-left: auto; }
  /* Long-trend pills row */
  .long-label { color: var(--muted); margin-top: 12px; margin-bottom: 6px;
    display: flex; align-items: center; gap: 5px; }
  .long-row { display: flex; gap: 6px; flex-wrap: wrap; }
  .long-pill { font-size: 11px !important; padding: 4px 9px !important;
    font-weight: 500; display: inline-flex; align-items: center; gap: 5px; }
  .long-pill .dur { color: var(--muted); font-size: 10px; }

  /* Forward returns */
  table.fwd { width: 100%; border-collapse: collapse; font-family: var(--mono); font-size: 13px; }
  table.fwd th, table.fwd td { padding: 6px 4px; text-align: right; border-bottom: 1px solid var(--border); }
  table.fwd th:first-child, table.fwd td:first-child { text-align: left; color: var(--muted); }
  td.pos { color: var(--green); }
  td.neg { color: var(--red); }
  td.nv { color: var(--muted); }

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
  <span class="brand">Stock market dashboard</span>
  <a href="https://gabjew90.github.io/Stock-market-dashboard/" class="active">GMI Daily</a>
  <a href="https://gabjew90.github.io/Stock-market-dashboard/pulse/">Daily Pulse</a>
  <a href="https://gabjew90.github.io/Stock-market-dashboard/wiki.html">Methodology</a>
</nav>
<div class="wrap">
  <h1>GMI Daily<span class="sub">market-state reconstruction</span></h1>

  <!-- 1. GMI + T2108 — the headline market-state panel. Two cards side-by-side. -->
  <div class="state-row">
    <div class="panel state-card">
      <div class="panel-title">
        GMI <button class="qmark" data-pop="gmi" aria-label="What is GMI">?</button>
      </div>
      <!-- Day N pill ABOVE the GREEN/RED badge -->
      <div class="callout day-above">
        <span class="pill" id="dayPill">Day — of —</span>
        <button class="qmark" data-pop="dayN" aria-label="Day N explanation">?</button>
      </div>
      <div class="hero">
        <div>
          <span class="num" id="gmiNum">0</span><span class="denom">/6</span>
        </div>
        <div>
          <span class="badge" id="stateBadge">—</span>
          <button class="qmark" data-pop="state" aria-label="What is the state" style="vertical-align:middle; margin-left:6px;">?</button>
        </div>
      </div>
      <!-- Stage pill BELOW the badge -->
      <div class="callout stage-below">
        <span class="pill" id="stagePill">Stage —</span>
        <button class="qmark" data-pop="stage" aria-label="Stage explanation">?</button>
      </div>
      <div class="comps-row" id="components"></div>
    </div>

    <div class="panel state-card">
      <div class="panel-title">
        T2108 <button class="qmark" data-pop="t2108" aria-label="What is T2108">?</button>
      </div>
      <div class="hero">
        <div>
          <span class="num" id="t2108Num">—</span><span class="denom">%</span>
        </div>
        <div>
          <span class="badge" id="t2108Badge">—</span>
        </div>
      </div>
      <div class="t-bar"><div class="t-bar-fill" id="t2108Fill"></div></div>
      <div class="t-scale">
        <span>0</span><span style="color:var(--green)">10 buy zone</span><span>50</span><span style="color:var(--red)">80 extended</span><span>100</span>
      </div>
      <div class="stage-note" id="t2108Note">—</div>
    </div>
  </div>

  <!-- 2. Chart -->
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

  <!-- 2. Compact Since-Day-1 strip (MA/QQQ values now live on the chart) -->
  <div class="panel since-panel">
    <div class="since-header">
      <span class="since-title">Since Day 1 of current ST trend</span>
      <button class="qmark" data-pop="since" aria-label="Since Day 1">?</button>
    </div>
    <div class="since-meta" id="sinceMeta">—</div>
    <div class="since-returns">
      <div class="since-cell"><span class="since-lbl">QQQ</span><span class="since-val" id="srd1">—</span></div>
      <div class="since-cell"><span class="since-lbl">TQQQ</span><span class="since-val" id="srd1tq">—</span></div>
      <div class="since-cell"><span class="since-lbl">SQQQ</span><span class="since-val" id="srd1sq">—</span></div>
    </div>
  </div>

  <!-- 3. Date slider + regime-change shortcuts -->
  <div class="panel">
    <div class="date-row">
      <input type="date" id="datePick">
      <input type="range" id="dateSlider" min="0" max="0" value="0">
    </div>
    <div class="small" style="margin-top:8px; margin-bottom:0;"></div>
    <div class="presets" id="presets"></div>
    <div class="small" id="dateLabel" style="margin-top:8px;">—</div>
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
const LONG_TRENDS = DATA.long_trends || [];

let VIEW = "daily";  // "daily" or "weekly"

const COMPS = [
  {name:"S10"},     // Successful 10d new high
  {name:"NH≥100"},  // 100+ new 52w highs
  {name:"QQQ↑"},    // QQQ daily up-trend
  {name:"SPY↑"},    // SPY daily up-trend
  {name:"QQQ wk"},  // QQQ weekly up-trend
  {name:"FFTY"},    // IBD-50 >50d MA
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
function buildPresets() {
  pBox.innerHTML = "";
  // Row 1: navigation [Prev] [Today] [Next] [Day 1 of current trend]
  const nav = document.createElement('div');
  nav.className = "nav-row";
  const mkBtn = (label, onclick, opts = {}) => {
    const b = document.createElement('button');
    b.innerHTML = label;
    b.onclick = onclick;
    if (opts.title) b.title = opts.title;
    if (opts.cls) b.className = opts.cls;
    if (opts.color) { b.style.color = opts.color; b.style.borderColor = opts.color.replace('1)', '0.5)'); }
    return b;
  };
  nav.appendChild(mkBtn("◀ Prev", () => setIndex(Number(dateSlider.value) - 1), {title: "Previous trading day", cls: "nav-arrow"}));
  nav.appendChild(mkBtn("Today",  () => setIndex(ROWS.length - 1)));
  nav.appendChild(mkBtn("Next ▶", () => setIndex(Number(dateSlider.value) + 1), {title: "Next trading day",     cls: "nav-arrow"}));
  // Day 1 of CURRENT (most recent) trend — same color as the current trend direction
  const cur = ROWS[ROWS.length - 1];
  if (cur && cur.d1d) {
    const arrow = cur.sd === "up" ? "▲" : "▼";
    const col = cur.sd === "up" ? "rgba(46,160,67,1)" : "rgba(248,81,73,1)";
    nav.appendChild(mkBtn(`${arrow} Day 1 (current)`, () => setIndex(findNearestIndex(cur.d1d)),
                          {title: `Day 1 of the current ST ${cur.sd}-trend — ${cur.d1d}`, color: col, cls: "nav-day1"}));
  }
  pBox.appendChild(nav);

  // Row 2: long-trend shortcuts (>= 30 trading days each)
  if (LONG_TRENDS.length) {
    const lbl = document.createElement('div');
    lbl.className = "small long-label";
    lbl.innerHTML = "Long ST trends (≥30 trading days): <button class='qmark' data-pop='longtrends' aria-label='What's a long trend'>?</button>";
    pBox.appendChild(lbl);
    const lg = document.createElement('div');
    lg.className = "long-row";
    LONG_TRENDS.forEach(t => {
      const arrow = t.dir === "up" ? "▲" : "▼";
      const col = t.dir === "up" ? "rgba(46,160,67,1)" : "rgba(248,81,73,1)";
      const b = document.createElement('button');
      b.className = "long-pill";
      b.innerHTML = `${arrow} ${t.d} <span class="dur">${t.len}d</span>`;
      b.style.color = t.dir === "up" ? "#2ea043" : "#f85149";
      b.style.borderColor = t.dir === "up" ? "rgba(46,160,67,0.4)" : "rgba(248,81,73,0.4)";
      b.title = `Day 1 of ${t.dir}-trend that lasted ${t.len} trading days — ${t.d}`;
      b.onclick = () => setIndex(findNearestIndex(t.d));
      lg.appendChild(b);
    });
    pBox.appendChild(lg);
  }
}
buildPresets();

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
  // Time-based x positioning: same calendar date sits at the same x in BOTH views.
  const firstTs = Date.parse(firstDate);
  const lastTs = Date.parse(lastDate);
  const tSpan = (lastTs - firstTs) || 1;
  const xAtDate = (dStr) => ((Date.parse(dStr) - firstTs) / tSpan) * plotW + PADX;
  const xAt = (i) => xAtDate(slice[i].d);
  const yAt = (v) => H - PADY_BOT - ((v - ymin) / yspan) * plotH;
  // Average bar width — used to size candle bodies. Daily ~3-4 px, weekly ~16-18 px.
  const barW = plotW / slice.length;

  // ===== RED gate shading — ALWAYS from daily ROWS so it's pixel-identical in both views =====
  {
    let runStart = null;
    for (let i = dStart; i <= dEnd; i++) {
      const dr = ROWS[i];
      const isRed = dr.s === 0;
      if (isRed && runStart == null) runStart = i;
      const isLast = i === dEnd;
      if ((!isRed || isLast) && runStart != null) {
        const x0 = xAtDate(ROWS[runStart].d);
        const x1 = xAtDate(ROWS[isRed ? i : i - 1].d);
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
    // Time-based bar width — derived from the avg inter-bar gap in the current slice so daily candles
    // stay thin (~3 px) and weekly candles get correspondingly wider (~18 px) while everything else
    // (MAs, red shading, marker) remains anchored to the same calendar dates.
    const avgGap = slice.length > 1 ? (Date.parse(slice[slice.length-1].d) - Date.parse(slice[0].d)) / (slice.length - 1) : 24*3600*1000;
    const bodyW = Math.max(2.5, (avgGap / tSpan) * plotW * 0.7);
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

  // ===== Selected-date marker + dynamic value labels =====
  const selectedDailyDate = ROWS[centerIdx].d;
  const selDaily = ROWS[centerIdx];
  // In weekly view we still want the labels at the WEEK'S MA values (since that's what the chart shows).
  // selectedWeekly = the WEEKLY row whose Friday-date >= the selected daily date.
  const selWeeklyIdx = selDaily.wi;
  const selWeekly = WEEKLY[selWeeklyIdx] || null;
  {
    const x = xAtDate(selectedDailyDate);
    const vline = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    vline.setAttribute('x1', x); vline.setAttribute('x2', x);
    vline.setAttribute('y1', 0); vline.setAttribute('y2', H - PADY_BOT);
    vline.setAttribute('stroke', '#e6edf3'); vline.setAttribute('stroke-width', '1.2');
    vline.setAttribute('stroke-dasharray', '3,3');
    vline.setAttribute('stroke-opacity', '0.85');
    svg.appendChild(vline);
    // Bottom date label
    const lab = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    lab.setAttribute('y', H - 6);
    lab.setAttribute('text-anchor', 'middle'); lab.setAttribute('font-size', '10');
    lab.setAttribute('font-family', 'ui-monospace,Menlo,Consolas,monospace');
    lab.setAttribute('fill', '#e6edf3');
    lab.textContent = selectedDailyDate;
    const halfW = 40;
    let lx = x;
    if (lx - halfW < 4) lx = halfW + 4;
    if (lx + halfW > W - 4) lx = W - halfW - 4;
    lab.setAttribute('x', lx);
    svg.appendChild(lab);

    // ===== Dynamic value labels next to the dashed line at the SELECTED date =====
    // Each label is a small pill (bg + text) just to the right of the dashed line, at the y of
    // that line's value on the selected date. Updates whenever the slider moves.
    function valuePill(yVal, text, color) {
      if (yVal == null || isNaN(yVal)) return;
      const tw = text.length * 5.5 + 8;  // approx width
      const ty = Math.max(10, Math.min(H - PADY_BOT - 4, yVal));
      // Choose left/right side depending on space available
      const goLeft = (x + tw + 4) > (W - PADX);
      const px = goLeft ? (x - tw - 4) : (x + 4);
      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', px); rect.setAttribute('y', ty - 7);
      rect.setAttribute('width', tw); rect.setAttribute('height', 12);
      rect.setAttribute('rx', 3);
      rect.setAttribute('fill', 'rgba(13,17,23,0.85)');
      rect.setAttribute('stroke', color); rect.setAttribute('stroke-width', '0.6');
      svg.appendChild(rect);
      const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      t.setAttribute('x', px + tw / 2); t.setAttribute('y', ty + 3);
      t.setAttribute('text-anchor', 'middle'); t.setAttribute('font-size', '9');
      t.setAttribute('font-family', 'ui-monospace,Menlo,Consolas,monospace');
      t.setAttribute('font-weight', '600'); t.setAttribute('fill', color);
      t.textContent = text;
      svg.appendChild(t);
    }
    // QQQ close at selected date (always show — it's the main price)
    const qClose = daily ? selDaily.cl : (selWeekly && selWeekly.c);
    if (qClose != null) valuePill(yAt(qClose), `Q ${qClose.toFixed(0)}`, "#58a6ff");
    if (daily && maOn.m30 && selDaily.m30 != null) valuePill(yAt(selDaily.m30), `30d ${selDaily.m30.toFixed(0)}`, MA_COLORS.m30);
    if (!daily && maOn.w10 && selWeekly && selWeekly.m10 != null) valuePill(yAt(selWeekly.m10), `10w ${selWeekly.m10.toFixed(0)}`, MA_COLORS.w10);
    if (!daily && maOn.w30 && selWeekly && selWeekly.m30 != null) valuePill(yAt(selWeekly.m30), `30w ${selWeekly.m30.toFixed(0)}`, MA_COLORS.w30);
  }

  // ===== X-axis date labels (time-based — 5 evenly-spaced timestamps; identical in both views) =====
  const nTicks = 5;
  for (let k = 0; k < nTicks; k++) {
    const frac = k / (nTicks - 1);
    const ts = firstTs + frac * tSpan;
    const x = frac * plotW + PADX;
    const dateStr = new Date(ts).toISOString().slice(0, 7);  // YYYY-MM
    const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    t.setAttribute('x', x);
    t.setAttribute('y', H - 18);
    t.setAttribute('text-anchor', k === 0 ? 'start' : (k === nTicks - 1 ? 'end' : 'middle'));
    t.setAttribute('font-size', '9');
    t.setAttribute('font-family', 'ui-monospace,Menlo,Consolas,monospace');
    t.setAttribute('fill', '#8b949e');
    t.textContent = dateStr;
    svg.appendChild(t);
    const tk = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    tk.setAttribute('x1', x); tk.setAttribute('x2', x);
    tk.setAttribute('y1', H - PADY_BOT); tk.setAttribute('y2', H - PADY_BOT + 3);
    tk.setAttribute('stroke', '#8b949e'); tk.setAttribute('stroke-width', '0.7');
    svg.appendChild(tk);
  }
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

  // T2108 — NYSE breadth: % of NYSE stocks above 40-day SMA
  const tn = document.getElementById('t2108Num');
  const tb = document.getElementById('t2108Badge');
  const tf = document.getElementById('t2108Fill');
  const tnote = document.getElementById('t2108Note');
  if (r.t == null) {
    tn.textContent = "—"; tb.textContent = "—"; tb.className = "badge"; tnote.textContent = "no breadth data for this date.";
  } else {
    tn.textContent = r.t.toFixed(1);
    tf.style.left = Math.max(0, Math.min(100, r.t)) + "%";
    let label, cls, note;
    if (r.t < 10) { label = "Buy zone"; cls = "green"; note = "Capitulation level. Dr. Wish accumulates SPY in tranches starting from here."; }
    else if (r.t > 80) { label = "Extended"; cls = "red"; note = "Market extended; profit-take / no new buys. Pullback typically follows."; }
    else if (r.t > 70) { label = "Hot"; cls = "yellow"; note = "Approaching extended. Watch for rollover."; }
    else if (r.t < 30) { label = "Cool"; cls = "yellow"; note = "Below normal. Below 10 is the buy zone."; }
    else { label = "Normal"; cls = "green"; note = "Healthy mid-range breadth (30–70)."; }
    tb.textContent = label; tb.className = "badge " + cls;
    tnote.textContent = note;
  }
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

  // Components
  const cBox = document.getElementById('components');
  cBox.innerHTML = "";
  COMPS.forEach((c, k) => {
    const on = r.c[k] === 1;
    const d = document.createElement('button');  // whole card is the tooltip trigger
    d.type = "button";
    d.className = "comp " + (on ? "on" : "off");
    d.dataset.pop = "c" + (k+1);
    d.setAttribute("aria-label", c.name);
    // tiny detail: show numeric for c1/c2, just the mark for the rest
    let detail = "";
    if (k === 0) detail = `${r.n10h}/${r.n10t}`;
    else if (k === 1) detail = `${r.nh}`;
    d.innerHTML = `
      <div class="name">${c.name}</div>
      <div class="mark">${on ? "✓" : "✗"}</div>
      ${detail ? `<div class="detail">${detail}</div>` : ""}`;
    cBox.appendChild(d);
  });

  // Compact Since-Day-1 strip (MA values now live on the chart as dynamic pills)
  document.getElementById('sinceMeta').innerHTML =
    r.d1d
      ? `<b>${arrow} Day ${r.dn} of ST ${r.sd}-trend</b> <span class="sub">· since ${r.d1d} (QQQ $${r.d1c != null ? r.d1c.toFixed(2) : "—"})</span>`
      : "—";
  function setPct(id, v) {
    const el = document.getElementById(id);
    if (v == null) { el.textContent = "—"; el.className = "since-val nv"; return; }
    el.textContent = (v >= 0 ? "+" : "") + v.toFixed(2) + "%";
    el.className = "since-val " + (v >= 0 ? "pos" : "neg");
  }
  setPct('srd1', r.rd1);
  setPct('srd1tq', r.rd1tq);
  setPct('srd1sq', r.rd1sq);

  drawSpark(i);
}

// ============================================================================
// Tooltip popover system — only the small ? button triggers it
// ============================================================================

const POP = {
  gmi: "<b>GMI — General Market Index</b><br>Dr. Wish's daily 0–6 score of six market-health components. ≥4 for 2 consecutive days flips the gate GREEN (willing to buy long). ≤3 for 2 days flips RED (defensive — cash or hedge).",
  t2108: "<b>T2108 — NYSE breadth</b><br>The percent of NYSE stocks trading above their 40-day SMA. Dr. Wish uses three zones:<br><b style='color:#2ea043'>&lt;10</b> = capitulation buy zone (he accumulates SPY in tranches; historically marks lasting bottoms).<br><b style='color:#d29922'>10–30 / 70–80</b> = caution zones at either extreme.<br><b style='color:#f85149'>&gt;80</b> = extended; no new buys, take some profit.<br>30–70 is the healthy mid-range. Validated against his reported T2108 at corr ≈ 0.93 (with a small +3–4 pt optimistic bias from survivorship in our universe).",
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
  longtrends: "<b>Long ST trends</b><br>Each pill is Day 1 of a past short-term trend (QQQ crossing its 30-day SMA) that lasted <b>30 or more trading days</b>. <span style='color:#2ea043'>▲ = up-trend</span>; <span style='color:#f85149'>▼ = down-trend</span>. The <b>Nd</b> badge shows how many trading days the trend lasted. Tap to jump the chart there. Showing the most recent 8.",
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
  const trigger = e.target.closest('button.qmark[data-pop], button.comp[data-pop]');
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
