"""Build a self-contained single-day-deep-dive GMI playground HTML file.

Loads breadth + prices, recomputes GMI + components + gate state, fetches QQQ OHLC,
computes Day-N of QQQ short-term trend and Weinstein stage, and emits a single HTML
file with everything embedded as JSON.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

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

# yfinance retry knobs. 3 attempts × 60s wait covers the typical 5-15 min
# transient-flakiness window we saw on 2026-05-18→19 without blowing the CI
# job's timeout. _yf_retry returns the first non-None / non-empty result.
_YF_RETRY_ATTEMPTS = 3
_YF_RETRY_WAIT_SECONDS = 60


def _yf_retry(fetch_fn, label: str = "yfinance"):
    """Run a yfinance fetch closure up to _YF_RETRY_ATTEMPTS times, sleeping
    _YF_RETRY_WAIT_SECONDS between failed attempts. Returns the first non-None
    result whose .empty (if it has one) is False; otherwise returns None.
    Exceptions inside fetch_fn are caught and counted as failures."""
    import time
    for attempt in range(1, _YF_RETRY_ATTEMPTS + 1):
        try:
            result = fetch_fn()
        except Exception as e:
            print(f"  {label}: attempt {attempt}/{_YF_RETRY_ATTEMPTS} raised {type(e).__name__}: {e}")
            result = None
        if result is not None and (not hasattr(result, "empty") or not result.empty):
            if attempt > 1:
                print(f"  {label}: attempt {attempt} succeeded after earlier failure(s)")
            return result
        if attempt < _YF_RETRY_ATTEMPTS:
            print(f"  {label}: attempt {attempt} returned empty/None; sleeping {_YF_RETRY_WAIT_SECONDS}s before retry…")
            time.sleep(_YF_RETRY_WAIT_SECONDS)
    return None


def _ensure_prices(tickers=("QQQ", "SPY", "TQQQ", "SQQQ"), max_age_days: int = 0) -> pd.DataFrame:
    """Load `data/backtest/prices.parquet`; refetch via yfinance if the cache is
    missing, incomplete, has a silently all-NaN column over its last 60 trading
    days, OR is stale. Default `max_age_days=0` means "refetch whenever the
    cache's last row is from a calendar day before today" — so every weekday CI
    run (firing at 22:00 UTC, after the US close) pulls that day's bar. On
    weekends / holidays the refetch just rewrites the cache with the same last
    trading day (harmless, ~3-second yfinance call)."""
    def _bad(df: pd.DataFrame) -> tuple[bool, str]:
        if not set(tickers) <= set(df.columns):
            return True, f"missing columns: {set(tickers) - set(df.columns)}"
        for t in tickers:
            tail = df[t].dropna().tail(60)
            if len(tail) < 5:
                return True, f"{t} has <5 non-NaN values in its last 60 rows"
        age = (pd.Timestamp.today().normalize() - df.index.max()).days
        if age > max_age_days:
            return True, f"data is {age} days old (max {max_age_days})"
        return False, ""

    cached: pd.DataFrame | None = None
    if PRICES_CACHE.exists():
        cached = pd.read_parquet(PRICES_CACHE)
        cached.index = pd.to_datetime(cached.index)
        is_bad, reason = _bad(cached)
        if not is_bad:
            return cached
        print(f"prices cache invalid — refetching ({reason})…")

    import yfinance as yf
    print(f"fetching {tickers} via yfinance…")

    def _do_one_attempt() -> pd.DataFrame | None:
        # Batch download first, falling through to per-ticker fallback for any ticker
        # the batch couldn't deliver. A network error in the batch isn't fatal — we
        # try each ticker individually.
        raw = None
        try:
            raw = yf.download(list(tickers), interval="1d", period="max",
                              auto_adjust=False, group_by="ticker", progress=False, threads=True)
        except Exception as e:
            print(f"  yf.download raised {type(e).__name__}: {e}; using per-ticker fallback for all tickers…")

        out: dict[str, pd.Series] = {}
        for t in tickers:
            if raw is None or getattr(raw, "empty", True):
                out[t] = pd.Series(dtype=float)
                continue
            try:
                sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
                col = "Adj Close" if "Adj Close" in sub.columns else "Close"
                out[t] = sub[col].astype(float)
            except (KeyError, AttributeError):
                out[t] = pd.Series(dtype=float)
        for t in tickers:
            if out[t].dropna().tail(5).shape[0] < 5:
                print(f"  batch download missing recent data for {t}; falling back to per-ticker fetch…")
                try:
                    tk = yf.Ticker(t).history(period="max", auto_adjust=False)
                    if not tk.empty:
                        col = "Adj Close" if "Adj Close" in tk.columns else "Close"
                        out[t] = tk[col].astype(float)
                except Exception as e:
                    print(f"    per-ticker fetch for {t} raised {type(e).__name__}: {e}")
        # Only count this attempt as a success if EVERY ticker has fresh data.
        # Otherwise return None so _yf_retry waits and tries again.
        all_good = all(out[t].dropna().tail(5).shape[0] >= 5 for t in tickers)
        if not all_good:
            missing = [t for t in tickers if out[t].dropna().tail(5).shape[0] < 5]
            print(f"  attempt incomplete — tickers still missing recent data: {missing}")
            return None
        return pd.DataFrame(out).dropna(how="all")

    df = _yf_retry(_do_one_attempt, label="_ensure_prices")
    if df is None:
        if cached is not None:
            print(f"  _ensure_prices: all retries failed — falling back to cached copy ending {cached.index.max().date()}")
            return cached
        raise RuntimeError("_ensure_prices: no cached prices and all yfinance retries failed")
    df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    # Don't overwrite a known-good cache with one that's older than what we already have.
    if cached is not None and df.index.max() < cached.index.max():
        print(f"  refetched data ends {df.index.max().date()}, older than cache {cached.index.max().date()}; keeping cache")
        return cached
    PRICES_CACHE.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PRICES_CACHE)
    return df


def fetch_qqq_ohlc() -> pd.DataFrame:
    """Fetch QQQ OHLC from yfinance with split/dividend adjustment so all four
    series are on the same scale. Cached at QQQ_OHLC_CACHE; refreshes whenever
    the cache's last row is from before today (matches prices.parquet's
    daily-fresh discipline). Robust to yfinance hiccups: a transient fetch
    failure or empty response falls back to the cached copy rather than
    aborting the whole build (the 2026-05-18 cron failure that left the live
    site stale for a day was caused by a yfinance call returning an empty
    frame here and the build crashing on the column subset)."""
    import yfinance as yf

    cached: pd.DataFrame | None = None
    if QQQ_OHLC_CACHE.exists():
        cached = pd.read_parquet(QQQ_OHLC_CACHE)
        cached.index = pd.to_datetime(cached.index)
        age = (pd.Timestamp.today().normalize() - cached.index.max()).days
        if age <= 0 and "volume" in cached.columns:
            return cached

    def _try_fetch() -> pd.DataFrame | None:
        # Primary: batch download. auto_adjust=True → OHLC back-adjusted for divs/splits.
        try:
            df = yf.download("QQQ", start="1999-01-01", auto_adjust=True, progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [c[0].lower() for c in df.columns]
            else:
                df.columns = [c.lower() for c in df.columns]
            if not df.empty and {"open", "high", "low", "close", "volume"} <= set(df.columns):
                df = df[["open", "high", "low", "close", "volume"]].dropna()
                if not df.empty:
                    return df
            print("  fetch_qqq_ohlc: yf.download returned empty/incomplete; trying yf.Ticker fallback…")
        except Exception as e:
            print(f"  fetch_qqq_ohlc: yf.download raised {type(e).__name__}: {e}; trying yf.Ticker fallback…")
        # Fallback: per-ticker history call (different code path inside yfinance).
        try:
            tk = yf.Ticker("QQQ").history(period="max", auto_adjust=True)
            tk.columns = [c.lower() for c in tk.columns]
            if not tk.empty and {"open", "high", "low", "close", "volume"} <= set(tk.columns):
                return tk[["open", "high", "low", "close", "volume"]].dropna()
        except Exception as e:
            print(f"  fetch_qqq_ohlc: yf.Ticker.history raised {type(e).__name__}: {e}")
        return None

    df = _yf_retry(_try_fetch, label="fetch_qqq_ohlc")
    if df is None:
        if cached is not None and "volume" in cached.columns:
            print(f"  fetch_qqq_ohlc: all retries failed — falling back to cached copy ending {cached.index.max().date()}")
            return cached
        raise RuntimeError("fetch_qqq_ohlc: no cached OHLC and all yfinance retries failed")
    df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    if cached is not None and df.index.max() < cached.index.max():
        print(f"  fetch_qqq_ohlc: fresh data ends {df.index.max().date()}, older than cache {cached.index.max().date()}; keeping cache")
        return cached
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


def _weinstein_stage(
    qqq: pd.Series,
    w10: pd.Series,
    w30: pd.Series,
    slope_window_weeks: int = 8,
    rising_threshold_pct: float = 1.0,
    shallow_pullback_pct: float = 5.0,
) -> pd.Series:
    """Stage 1/2/3/4 per Stan Weinstein, calibrated to Dr. Wish's actual usage
    (see wiki/methodology/moving-average-rules.md):

      Stage 2 = price above 30wk AND 30wk clearly rising   (advancing — only stage he buys long)
      Stage 3 = price above 30wk BUT 30wk flat / barely rising / turning down  (topping)
      Stage 4 = price below 30wk AND 10wk < 30wk (cross-down confirmation)   (declining)
      Stage 1 = price below 30wk BUT 10wk still above 30wk                   (basing / pullback inside uptrend)

    Two refinements over a strict "is the slope > 0" check:

    1. **Slope uses a percentage threshold over an 8-week window**, not "any positive
       change vs 4 trading days ago". A 30wk SMA changes slowly even at tops, so the
       strict `> 0` rule treated a barely-flattening MA the same as a fast-rising one
       and erased every topping period (2018, 2021, 2024 had zero Stage-3 days).
       1% over 8 weeks is the default — a meaningful uptrend rate, not noise.

    2. **Stage 4 requires the 10wk-below-30wk cross**, which is Wish's own
       confirmation signal ("10-week average crossing below 30-week confirms Stage 4
       onset" — WW 2025-03-30 IWM call). Without this, a 3-day price dip below the
       30wk during a strong uptrend got mis-labelled Stage 4.

    The slope is computed on the weekly cadence to avoid a calendar artifact that
    would otherwise hit every Thursday (shift(N) on the daily-reindexed series
    lands on the previous Friday update, comparing the same weekly value to
    itself and flipping the slope flag to False).
    """
    above_30wk = qqq > w30
    ten_above_thirty = w10 > w30
    # Depth qualifier: how far below the 30wk did price drop? A pullback within
    # `shallow_pullback_pct` of the 30wk (~5%) can stay Stage 1; anything deeper
    # is treated as a Stage-3 warning even before the slope flips. A 5-day
    # rolling-OR adds light hysteresis so a single rally day doesn't flip the
    # call back to Stage 1 while the trajectory is still down.
    deep_today = qqq < w30 * (1.0 - shallow_pullback_pct / 100.0)
    deep_recent = deep_today.rolling(5, min_periods=1).max().astype(bool)
    shallow_below = ~deep_recent

    # Weekly-cadence slope: deduplicate the daily-ffilled w30 back to one row per
    # actual weekly update, compare today's value to N weekly bars ago in %,
    # then propagate the boolean back to daily via ffill.
    w30_weekly = w30[w30.ne(w30.shift())].dropna()
    slope_pct_weekly = (w30_weekly / w30_weekly.shift(slope_window_weeks) - 1.0) * 100.0
    slope_rising_weekly = (slope_pct_weekly > rising_threshold_pct).fillna(False)
    slope_rising = slope_rising_weekly.reindex(qqq.index, method="ffill").fillna(False).astype(bool)

    # Mapping forces Stage 3 between Stage 2 and Stage 4 whenever the move has
    # any depth or momentum-loss. Three signals can fire Stage 3 from below the
    # 30wk: slope no longer rising, OR a deep pullback >shallow_pullback_pct.
    # Stage 1 is reserved for the SHALLOW pullback inside a still-rising 30wk
    # (the classic Aug-2024 V-shape: -3% below the rising line, 10wk still above
    # 30wk, recovered within days).
    stage = pd.Series(0, index=qqq.index, dtype=int)
    # Above 30wk
    stage[above_30wk & slope_rising] = 2     # clean uptrend
    stage[above_30wk & ~slope_rising] = 3    # topping above the line
    # Below 30wk + 10wk still above 30wk (10/30 cross hasn't fired yet)
    stage[~above_30wk & ten_above_thirty & slope_rising & shallow_below] = 1   # shallow pullback in uptrend
    stage[~above_30wk & ten_above_thirty & slope_rising & ~shallow_below] = 3  # deep drawdown — Stage 4 setup
    stage[~above_30wk & ten_above_thirty & ~slope_rising] = 3                  # slope decelerating — Stage 4 setup
    # Below 30wk + 10wk has crossed below 30wk = confirmed decline
    stage[~above_30wk & ~ten_above_thirty] = 4
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
    # Reindex OHLC to the daily index WITHOUT forward-fill: candle bodies must
    # reflect the actual session's prints, not the prior day's copied forward.
    # If the OHLC cache lags prices.parquet by a day (e.g. an aborted refetch),
    # the merge previously left today's row with yesterday's o/h/l/cl, so the
    # candle rendered green-when-red. Leaving NaN here makes the renderer skip
    # the candle until real OHLC arrives.
    ohlc = fetch_qqq_ohlc().reindex(idx)
    qopen = ohlc["open"]
    qhigh = ohlc["high"]
    qlow = ohlc["low"]
    qclose_ohlc = ohlc["close"]  # used for the candle body so o/c are self-consistent
    qvol = ohlc.get("volume", pd.Series(0, index=idx)).fillna(0)

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
        "vv": qvol.round(0).astype("Int64"),
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
    wk_v = qvol.resample("W-FRI").sum()
    wk_df = pd.DataFrame({"o": wk_o, "h": wk_h, "l": wk_l, "c": wk_c, "v": wk_v}).dropna()
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
            "v": None if pd.isna(wr["v"]) else int(wr["v"]),
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
            "v": None if pd.isna(r["vv"]) else int(r["vv"]),
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
<title>Stock market dashboard — Market Regime</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    /* Warm-dark editorial palette — like a financial paper printed on dark stock */
    --bg: #0b0a09;
    --bg-2: #14110f;
    --panel: #181513;
    --panel-2: #221c18;
    --panel-hi: #2b231e;
    --border: #2a2420;
    --border-2: #3a3128;
    --hairline: #1f1a16;
    --text: #f2ebe1;
    --text-2: #ddd1bf;
    --muted: #9c8c7c;
    --dim: #6b5d52;
    /* Bold single accent — amber gold, the page's signature */
    --accent: #e7a924;
    --accent-2: #f5c042;
    --accent-soft: rgba(231,169,36,0.14);
    --accent-glow: rgba(231,169,36,0.32);
    /* Refined bull/bear — sit closer together than punchy reds/greens */
    --bull: #4fa363;
    --bull-soft: rgba(79,163,99,0.14);
    --bull-line: rgba(79,163,99,0.42);
    --bear: #d96250;
    --bear-soft: rgba(217,98,80,0.14);
    --bear-line: rgba(217,98,80,0.42);
    --caution: #d09a2a;
    --caution-soft: rgba(208,154,42,0.14);
    --caution-line: rgba(208,154,42,0.42);
    /* Type stacks */
    --serif: "Instrument Serif", "Cormorant Garamond", "Times New Roman", Georgia, serif;
    --sans: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    --mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    font-size: 15px;
    line-height: 1.55;
    font-feature-settings: "ss01", "cv01";
    /* Subtle warm-paper texture — barely there, but kills the "flat AI" feel */
    background-image:
      radial-gradient(ellipse 80% 50% at 50% 0%, rgba(231,169,36,0.05), transparent 70%),
      radial-gradient(ellipse 60% 40% at 100% 100%, rgba(217,98,80,0.025), transparent 70%);
    background-attachment: fixed;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  /* Faint film-grain overlay */
  body::before {
    content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 1;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.95 0 0 0 0 0.85 0 0 0 0 0.7 0 0 0 0.03 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
    opacity: 0.55; mix-blend-mode: overlay;
  }
  /* Top nav — newspaper masthead style: thin top rule, brand on the left in serif, links right */
  .pages-nav {
    position: sticky; top: 0; z-index: 100;
    display: flex; align-items: center; gap: 4px;
    padding: 14px 24px;
    background: rgba(11,10,9,0.88);
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    border-bottom: 1px solid var(--border);
    box-shadow: 0 1px 0 rgba(255,255,255,0.02);
  }
  .pages-nav::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent) 18%, var(--accent) 82%, transparent);
    opacity: 0.55;
  }
  .pages-nav .brand {
    font-family: var(--serif);
    font-weight: 400; font-style: italic;
    margin-right: auto;
    font-size: 22px;
    letter-spacing: 0.005em;
    color: var(--text);
    line-height: 1;
    display: inline-flex; align-items: baseline; gap: 8px;
  }
  .pages-nav .brand .mark {
    font-family: var(--mono); font-style: normal;
    font-size: 9px; letter-spacing: 0.22em; color: var(--accent);
    text-transform: uppercase; padding: 3px 7px;
    border: 1px solid var(--accent); border-radius: 2px;
    line-height: 1; align-self: center;
  }
  .pages-nav a {
    color: var(--muted); text-decoration: none;
    padding: 8px 14px; border-radius: 2px;
    font-family: var(--mono); font-size: 11px; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
    border-bottom: 1px solid transparent;
    transition: color 0.18s ease, border-color 0.18s ease;
  }
  .pages-nav a.active { color: var(--accent); border-bottom-color: var(--accent); }
  .pages-nav a:hover { color: var(--text); border-bottom-color: var(--border-2); }
  @media (max-width: 640px) {
    .pages-nav { padding: 11px 14px; }
    .pages-nav .brand { font-size: 18px; }
    .pages-nav .brand .mark { font-size: 8px; padding: 2px 5px; }
    .pages-nav a { padding: 6px 9px; font-size: 10px; letter-spacing: 0.08em; }
  }
  @media (max-width: 420px) {
    .pages-nav .brand .mark { display: none; }
  }

  .wrap { max-width: 1120px; margin: 0 auto; padding: 28px 24px 48px; position: relative; z-index: 2; }
  @media (max-width: 640px) { .wrap { padding: 20px 14px 36px; } }

  /* Hero — editorial title block */
  .hero-block { margin: 0 0 22px; padding-bottom: 18px; border-bottom: 1px solid var(--border); }
  .dateline {
    display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
    font-family: var(--mono); font-size: 10px; letter-spacing: 0.24em;
    text-transform: uppercase; color: var(--muted);
    margin-bottom: 14px;
  }
  .dateline .vol { color: var(--accent); }
  .dateline .sep { color: var(--dim); }
  h1 {
    font-family: var(--serif); font-weight: 400;
    font-size: clamp(42px, 7vw, 72px);
    line-height: 0.98; letter-spacing: -0.015em;
    margin: 0 0 6px;
    color: var(--text);
  }
  h1 em { font-style: italic; color: var(--accent); font-weight: 400; }
  .deck {
    font-family: var(--serif); font-style: italic;
    font-size: clamp(16px, 2.2vw, 20px);
    color: var(--text-2); line-height: 1.4;
    margin: 0; max-width: 56ch;
  }
  .last-updated {
    color: var(--muted); font-family: var(--mono); font-size: 10.5px;
    letter-spacing: 0.16em; text-transform: uppercase;
    margin: 14px 0 0; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
  }
  .last-updated::before {
    content: ""; width: 6px; height: 6px; border-radius: 50%;
    background: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft);
    flex-shrink: 0;
  }

  /* Panels — refined, lift on hover, sharp inner rule */
  .panel {
    background: linear-gradient(180deg, var(--panel) 0%, var(--bg-2) 100%);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 18px 18px;
    margin: 14px 0;
    position: relative;
    box-shadow:
      0 1px 0 rgba(255,255,255,0.025) inset,
      0 18px 40px -28px rgba(0,0,0,0.6);
  }
  .panel + .panel { margin-top: 14px; }
  .small { color: var(--muted); font-size: 11px; font-family: var(--mono); letter-spacing: 0.04em; }

  /* Section header label — small uppercase mono, used as the title of every panel */
  .panel-title {
    font-size: 10px; color: var(--muted); font-family: var(--mono);
    text-transform: uppercase; letter-spacing: 0.26em; margin-bottom: 14px;
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 10px; border-bottom: 1px solid var(--hairline);
  }
  .panel-title::before {
    content: ""; width: 14px; height: 1px; background: var(--accent); flex-shrink: 0;
  }
  .panel-title .label-main { color: var(--text-2); font-weight: 600; letter-spacing: 0.22em; }

  /* Hero — GMI + state + day-N + stage */
  .hero { display: grid; grid-template-columns: auto 1fr; gap: 18px; align-items: center; }
  .hero .num {
    font-family: var(--serif); font-weight: 400;
    font-size: 84px; line-height: 0.9; color: var(--text);
    letter-spacing: -0.03em;
    font-feature-settings: "lnum", "tnum";
  }
  .hero .denom { color: var(--muted); font-family: var(--serif); font-size: 30px; font-style: italic; margin-left: 2px; }
  @media (max-width: 480px) {
    .hero .num { font-size: 64px; }
    .hero .denom { font-size: 24px; }
  }
  .badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 12px; border-radius: 2px;
    font-family: var(--mono); font-weight: 600;
    font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase;
  }
  .badge::before {
    content: ""; width: 6px; height: 6px; border-radius: 50%;
    background: currentColor;
  }
  .badge.green { background: var(--bull-soft); color: var(--bull); border: 1px solid var(--bull-line); }
  .badge.red { background: var(--bear-soft); color: var(--bear); border: 1px solid var(--bear-line); }
  .badge.yellow { background: var(--caution-soft); color: var(--caution); border: 1px solid var(--caution-line); }
  .meta { color: var(--muted); font-size: 13px; margin-top: 6px; }
  .meta b { color: var(--text); font-weight: 600; }

  /* Trend / stage callout — refined pill */
  .callout { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; align-items: center; }
  .pill {
    display: inline-flex; align-items: center; gap: 7px;
    background: var(--panel-2); border: 1px solid var(--border);
    border-radius: 2px; padding: 6px 12px;
    font-size: 11px; font-family: var(--mono);
    letter-spacing: 0.06em;
  }
  .pill b { color: var(--text); font-weight: 600; }
  .pill.up { color: var(--bull); border-color: var(--bull-line); background: var(--bull-soft); }
  .pill.down { color: var(--bear); border-color: var(--bear-line); background: var(--bear-soft); }
  .pill.s2 { color: var(--bull); border-color: var(--bull-line); background: var(--bull-soft); }
  .pill.s4 { color: var(--bear); border-color: var(--bear-line); background: var(--bear-soft); }
  .pill.s3, .pill.s1 { color: var(--caution); border-color: var(--caution-line); background: var(--caution-soft); }
  .stage-note { font-size: 12.5px; color: var(--text-2); margin-top: 10px;
    font-family: var(--serif); font-style: italic; line-height: 1.5; }

  /* Since-Day-1 strip */
  .since-panel { padding: 18px; }
  .since-header { display: flex; align-items: center; gap: 8px; font-size: 10px;
    color: var(--muted); font-family: var(--mono); text-transform: uppercase;
    letter-spacing: 0.26em; margin-bottom: 12px;
    padding-bottom: 10px; border-bottom: 1px solid var(--hairline); }
  .since-header::before {
    content: ""; width: 14px; height: 1px; background: var(--accent); flex-shrink: 0;
  }
  .since-header .since-title { color: var(--text-2); font-weight: 600; letter-spacing: 0.22em; }
  .since-meta { font-size: 13px; color: var(--text); margin-bottom: 14px;
    font-family: var(--mono); letter-spacing: 0.01em; }
  .since-meta b { font-weight: 600; color: var(--accent-2); }
  .since-meta .sub { color: var(--muted); }
  .since-returns { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
  .since-cell {
    background: var(--bg-2); border: 1px solid var(--border);
    border-radius: 3px; padding: 12px 10px;
    display: flex; flex-direction: column; align-items: flex-start; gap: 4px;
    position: relative; overflow: hidden;
  }
  .since-cell::after {
    content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 2px;
    background: var(--accent); opacity: 0;
    transition: opacity 0.2s;
  }
  .since-cell.pos::after { background: var(--bull); opacity: 0.7; }
  .since-cell.neg::after { background: var(--bear); opacity: 0.7; }
  .since-lbl {
    font-size: 9.5px; color: var(--muted); font-family: var(--mono);
    letter-spacing: 0.22em; text-transform: uppercase; font-weight: 600;
  }
  .since-val {
    font-size: 22px; font-weight: 600; font-family: var(--mono);
    line-height: 1.05; margin-top: 2px; letter-spacing: -0.01em;
    font-feature-settings: "tnum";
  }
  .since-val.pos { color: var(--bull); }
  .since-val.neg { color: var(--bear); }
  .since-val.nv { color: var(--muted); }

  /* Top state row — GMI + T2108 cards side by side on desktop, stacked on mobile */
  .state-row { display: grid; grid-template-columns: 1fr; gap: 14px; }
  @media (min-width: 760px) { .state-row { grid-template-columns: 1.15fr 1fr; } }
  .state-row > .panel { margin: 0; }
  .state-card { display: flex; flex-direction: column; }

  /* T2108 gauge bar — refined, sharp rectangles instead of pill */
  .t-bar { position: relative; width: 100%; height: 6px; border-radius: 1px;
    margin-top: 14px; overflow: visible;
    background: linear-gradient(to right,
      var(--bull) 0%, var(--bull) 10%,
      var(--bull-soft) 10%, var(--bull-soft) 30%,
      var(--border) 30%, var(--border) 70%,
      var(--bear-soft) 70%, var(--bear-soft) 80%,
      var(--bear) 80%, var(--bear) 100%);
    border: 1px solid var(--hairline);
  }
  .t-bar-fill { position: absolute; top: -4px; bottom: -4px; width: 2px;
    background: var(--text); left: 0%;
    transition: left 0.25s ease;
    box-shadow: 0 0 0 2px var(--bg), 0 0 12px var(--accent-glow);
  }
  .t-scale { display: flex; justify-content: space-between; font-family: var(--mono);
    font-size: 9px; color: var(--muted); margin-top: 8px;
    letter-spacing: 0.1em; text-transform: uppercase;
  }
  .t-scale span { white-space: nowrap; }

  /* Components row — refined sharp cards */
  .comps-row {
    display: grid; grid-template-columns: repeat(6, 1fr); gap: 5px;
    margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--hairline);
  }
  @media (max-width: 480px) { .comps-row { grid-template-columns: repeat(3, 1fr); } }
  .comp {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: 3px;
    padding: 9px 4px 7px; text-align: center; cursor: pointer; user-select: none;
    position: relative; transition: border-color 0.18s, transform 0.18s;
  }
  .comp:hover { border-color: var(--border-2); transform: translateY(-1px); }
  .comp .name {
    font-size: 9px; color: var(--muted); font-family: var(--mono);
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 4px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .comp .mark { font-size: 16px; font-weight: 700; font-family: var(--serif); line-height: 1.1; }
  .comp.on { border-color: var(--bull-line); }
  .comp.on .mark { color: var(--bull); }
  .comp.off { border-color: var(--bear-line); }
  .comp.off .mark { color: var(--bear); }
  .comp .detail {
    font-size: 9px; color: var(--muted); font-family: var(--mono);
    margin-top: 2px; letter-spacing: 0.04em;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }

  /* ? helper — refined square instead of pill */
  .qmark { display: inline-flex; align-items: center; justify-content: center;
    width: 18px; height: 18px; border-radius: 2px;
    background: transparent; color: var(--accent);
    font-size: 11px; font-weight: 600; cursor: pointer;
    user-select: none; border: 1px solid var(--accent-glow);
    padding: 0; line-height: 1; flex-shrink: 0;
    font-family: var(--serif); font-style: italic;
    transition: background 0.18s, color 0.18s, border-color 0.18s;
  }
  .qmark:hover, .qmark:active { background: var(--accent-soft); border-color: var(--accent); color: var(--accent-2); }

  /* Chart */
  .chart-wrap { position: relative; }
  .spark { width: 100%; height: 280px; display: block;
    cursor: ew-resize; touch-action: none; -webkit-user-select: none; user-select: none; }
  @media (min-width: 760px) { .spark { height: 340px; } }
  .spark.dragging { cursor: grabbing; }
  .x-axis-labels { position: absolute; left: 0; right: 0; bottom: 0; height: 30px;
    pointer-events: none; font-family: var(--mono); }
  .x-axis-labels .x-tick { position: absolute; bottom: 14px; transform: translateX(-50%);
    font-size: 10px; color: var(--muted); white-space: nowrap; letter-spacing: 0.06em; }
  .x-axis-labels .x-tick.start { transform: translateX(0); }
  .x-axis-labels .x-tick.end   { transform: translateX(-100%); }
  .x-axis-labels .x-selected { position: absolute; bottom: 0; transform: translateX(-50%);
    font-size: 11px; font-weight: 600; color: var(--accent); white-space: nowrap;
    font-family: var(--mono); letter-spacing: 0.04em; }
  @media (max-width: 480px) {
    .x-axis-labels .x-tick { font-size: 9px; }
    .x-axis-labels .x-selected { font-size: 10px; }
  }
  /* Top-left stat overlay — dynamic values for the selected date */
  .stat-overlay { position: absolute; top: 10px; left: 12px;
    display: flex; flex-direction: column; gap: 2px;
    font-family: var(--mono); font-size: 12px;
    background: rgba(11,10,9,0.86); padding: 8px 12px;
    border-radius: 2px; border: 1px solid var(--border);
    border-left: 2px solid var(--accent);
    pointer-events: none;
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  }
  .stat-overlay .stat-row { display: flex; justify-content: space-between;
    align-items: baseline; gap: 16px; min-width: 92px; line-height: 1.4; }
  .stat-overlay .stat-row .label {
    color: var(--muted); font-weight: 500; font-size: 9.5px;
    letter-spacing: 0.16em; text-transform: uppercase;
  }
  .stat-overlay .stat-row .val { font-weight: 600; text-align: right; font-feature-settings: "tnum"; }
  @media (max-width: 480px) {
    .stat-overlay { top: 7px; left: 7px; padding: 6px 9px; font-size: 11px; }
    .stat-overlay .stat-row { min-width: 80px; gap: 10px; }
    .stat-overlay .stat-row .label { font-size: 9px; }
  }
  .chart-header { display: flex; justify-content: space-between; align-items: center;
    gap: 10px; margin-bottom: 12px; flex-wrap: wrap; }
  .chart-header .small { font-family: var(--mono); font-size: 10.5px;
    color: var(--text-2); letter-spacing: 0.16em; text-transform: uppercase; }

  /* Legend */
  .legend { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px;
    font-size: 11px; font-family: var(--mono); align-items: center; }
  .legend-item { display: inline-flex; align-items: center; gap: 5px; }
  .chip {
    display: inline-flex; align-items: center; gap: 6px; cursor: pointer; color: var(--muted);
    user-select: none; border: 1px solid var(--border); border-radius: 2px;
    padding: 5px 11px; background: var(--bg-2);
    font-size: 10px; font-family: var(--mono); font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
    transition: border-color 0.18s, color 0.18s, background 0.18s;
  }
  .chip.on { color: var(--accent); border-color: var(--accent); background: var(--accent-soft); }
  .chip:hover { color: var(--text); border-color: var(--border-2); }
  .legend .swatch { display: inline-block; width: 14px; height: 2px; }

  /* Controls panel — refined */
  .ctl-panel { padding: 18px; }
  .ctl-row1 { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .ctl-row1 input[type=date] {
    flex: 1; min-width: 140px;
    background: var(--bg-2); color: var(--text);
    border: 1px solid var(--border); border-radius: 2px;
    padding: 8px 12px; font-family: var(--mono); font-size: 12px;
    letter-spacing: 0.04em;
    transition: border-color 0.18s;
  }
  .ctl-row1 input[type=date]:focus { outline: none; border-color: var(--accent); }
  .ctl-row1 input[type=date]::-webkit-calendar-picker-indicator {
    filter: invert(0.7) sepia(1) saturate(3) hue-rotate(10deg); opacity: 0.75; cursor: pointer;
  }
  .ctl-step, .ctl-today {
    background: var(--bg-2); color: var(--text);
    border: 1px solid var(--border); border-radius: 2px;
    font-family: var(--mono); cursor: pointer;
    transition: border-color 0.18s, color 0.18s, background 0.18s;
  }
  .ctl-step {
    width: 36px; padding: 8px 0; font-size: 12px; line-height: 1;
  }
  .ctl-today {
    padding: 8px 18px; font-size: 10px; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase;
  }
  .ctl-step:hover, .ctl-today:hover { color: var(--accent); border-color: var(--accent); background: var(--accent-soft); }

  .ctl-day1 {
    width: 100%; margin-top: 10px;
    padding: 11px 14px; font-size: 11px; font-family: var(--mono); font-weight: 600;
    background: var(--bull-soft); border: 1px solid var(--bull-line); color: var(--bull);
    border-radius: 2px; cursor: pointer; text-align: center;
    letter-spacing: 0.1em;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    transition: background 0.18s, border-color 0.18s;
  }
  .ctl-day1:hover { background: rgba(79,163,99,0.22); border-color: var(--bull); }
  .ctl-day1.down { color: var(--bear); border-color: var(--bear-line); background: var(--bear-soft); }
  .ctl-day1.down:hover { background: rgba(217,98,80,0.22); border-color: var(--bear); }

  .ctl-long-head {
    display: flex; align-items: center; gap: 8px;
    color: var(--muted); font-size: 9.5px; font-family: var(--mono);
    text-transform: uppercase; letter-spacing: 0.24em;
    margin-top: 18px; margin-bottom: 10px;
    padding-bottom: 8px; border-bottom: 1px solid var(--hairline);
  }
  .ctl-long-head::before {
    content: ""; width: 12px; height: 1px; background: var(--accent); flex-shrink: 0;
  }
  .ctl-long-head .label-main { color: var(--text-2); font-weight: 600; letter-spacing: 0.22em; }

  .ctl-long { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; }
  @media (min-width: 760px) { .ctl-long { grid-template-columns: repeat(4, 1fr); } }
  .ctl-long .long-pill {
    font-family: var(--mono); font-size: 10.5px;
    padding: 8px 8px;
    background: var(--bg-2); border-radius: 2px; cursor: pointer;
    text-align: center; line-height: 1.25; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis; font-weight: 600;
    letter-spacing: 0.04em;
    transition: background 0.18s, transform 0.18s;
  }
  .ctl-long .long-pill .pill-len {
    color: var(--muted); font-size: 9.5px; margin-left: 5px; font-weight: 400;
    letter-spacing: 0.05em;
  }
  .ctl-long .long-pill:hover { transform: translateY(-1px); }

  .footer {
    color: var(--muted); font-size: 10.5px; margin-top: 24px;
    padding-top: 18px; border-top: 1px solid var(--border);
    text-align: center; line-height: 1.7;
    font-family: var(--mono); letter-spacing: 0.06em;
  }

  /* Tooltip popover */
  .pop { position: fixed; max-width: 300px;
    background: var(--panel); border: 1px solid var(--accent);
    border-radius: 3px; padding: 14px 16px;
    font-size: 12.5px; line-height: 1.55; color: var(--text);
    z-index: 1000;
    box-shadow: 0 18px 50px rgba(0,0,0,0.7), 0 0 0 1px var(--accent-glow);
    display: none;
    font-family: var(--sans);
  }
  .pop.show { display: block; }
  .pop b { color: var(--accent-2); font-weight: 600; font-family: var(--mono); font-size: 11.5px;
    letter-spacing: 0.04em; }
  .pop .close { position: absolute; top: 6px; right: 10px; cursor: pointer;
    color: var(--muted); font-size: 18px; line-height: 1;
    font-family: var(--serif); font-style: italic; }
  .pop .close:hover { color: var(--text); }
</style>
</head>
<body>
<nav class="pages-nav">
  <span class="brand">Stock <em>market</em> dashboard <span class="mark">Live</span></span>
  <a href="https://gabjew90.github.io/Stock-market-dashboard/" class="active">Market Regime</a>
  <a href="https://gabjew90.github.io/Stock-market-dashboard/pulse/">Research</a>
</nav>
<div class="wrap">

  <!-- Hero block — editorial title -->
  <header class="hero-block">
    <div class="dateline">
      <span class="vol">Vol. I</span>
      <span class="sep">·</span>
      <span>QQQ Short-Term &amp; Stage Tape</span>
      <span class="sep">·</span>
      <span>Reconstructed Point-in-Time</span>
    </div>
    <h1>Market <em>Regime</em></h1>
    <p class="deck">A daily, point-in-time read of the broad market — GMI score, Weinstein stage, NYSE breadth, and the day count of the QQQ short-term trend, all on one tape.</p>
    <div class="last-updated" id="lastUpdated">—</div>
  </header>

  <!-- 1. GMI + T2108 — the headline market-state panel. -->
  <div class="state-row">
    <div class="panel state-card">
      <div class="panel-title">
        <span class="label-main">General Market Index</span>
        <button class="qmark" data-pop="gmi" aria-label="What is GMI">i</button>
      </div>
      <div class="callout day-above">
        <span class="pill" id="dayPill">Day — of —</span>
        <button class="qmark" data-pop="dayN" aria-label="Day N explanation">i</button>
      </div>
      <div class="hero">
        <div>
          <span class="num" id="gmiNum">0</span><span class="denom">/6</span>
        </div>
        <div>
          <span class="badge" id="stateBadge">—</span>
          <button class="qmark" data-pop="state" aria-label="What is the state" style="vertical-align:middle; margin-left:8px;">i</button>
        </div>
      </div>
      <div class="callout stage-below">
        <span class="pill" id="stagePill">Stage —</span>
        <button class="qmark" data-pop="stage" aria-label="Stage explanation">i</button>
      </div>
      <div class="comps-row" id="components"></div>
    </div>

    <div class="panel state-card">
      <div class="panel-title">
        <span class="label-main">T2108 · NYSE Breadth</span>
        <button class="qmark" data-pop="t2108" aria-label="What is T2108">i</button>
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
        <span>0</span><span style="color:var(--bull)">10 buy</span><span>50</span><span style="color:var(--bear)">80 ext</span><span>100</span>
      </div>
      <div class="stage-note" id="t2108Note">—</div>
    </div>
  </div>

  <!-- 2. Chart -->
  <div class="panel">
    <div class="chart-header">
      <span class="small" id="chartTitle">QQQ · 6 mo · daily candles</span>
      <span style="display:inline-flex; align-items:center; gap:8px;">
        <span class="legend-item" style="gap:4px;">
          <span class="chip on" id="viewDaily" data-view="daily">Daily</span>
          <span class="chip" id="viewWeekly" data-view="weekly">Weekly</span>
        </span>
        <button class="qmark" data-pop="redshade" aria-label="Red shading explanation">i</button>
      </span>
    </div>
    <div class="chart-wrap">
      <svg class="spark" id="spark" viewBox="0 0 800 240" preserveAspectRatio="none"></svg>
      <div class="stat-overlay" id="statOverlay"></div>
      <div class="x-axis-labels" id="xAxisLabels"></div>
    </div>
    <div class="legend" id="legend">
      <!-- legend chips are rendered dynamically per view -->
    </div>
    <div class="small" style="margin-top:10px; font-style: italic; font-family: var(--serif); font-size: 13px; color: var(--muted); letter-spacing: 0; text-transform: none;">Tap any <b style="color:var(--accent); font-family: var(--mono); font-size: 11px;">i</b> for an explanation. Tap a legend chip to toggle a line.</div>
  </div>

  <!-- 3. Controls -->
  <div class="panel ctl-panel">
    <div class="panel-title">
      <span class="label-main">Navigation</span>
    </div>
    <div class="ctl-row1">
      <input type="date" id="datePick">
      <button class="ctl-step" id="ctlPrev" title="Previous trading day">◀</button>
      <button class="ctl-step" id="ctlNext" title="Next trading day">▶</button>
      <button class="ctl-today" id="ctlToday">Today</button>
      <input type="range" id="dateSlider" min="0" max="0" value="0" style="display:none;">
    </div>
    <button class="ctl-day1" id="ctlDay1">Day 1 of current trend</button>
    <div class="ctl-long-head">
      <span class="label-main">Long ST Trends ≥ 30d</span>
      <button class="qmark" data-pop="longtrends" aria-label="Long-trend shortcuts">i</button>
    </div>
    <div class="ctl-long" id="presets"></div>
  </div>

  <!-- 4. Since Day 1 -->
  <div class="panel since-panel">
    <div class="since-header">
      <span class="since-title">Performance Since Day 1</span>
      <button class="qmark" data-pop="since" aria-label="Since Day 1">i</button>
    </div>
    <div class="since-meta" id="sinceMeta">—</div>
    <div class="since-returns">
      <div class="since-cell" id="srd1Cell"><span class="since-lbl">QQQ · 1×</span><span class="since-val" id="srd1">—</span></div>
      <div class="since-cell" id="srd1tqCell"><span class="since-lbl">TQQQ · 3×</span><span class="since-val" id="srd1tq">—</span></div>
      <div class="since-cell" id="srd1sqCell"><span class="since-lbl">SQQQ · −3×</span><span class="since-val" id="srd1sq">—</span></div>
    </div>
  </div>

  <div class="footer">
    Reconstructed Point-in-Time GMI · Nasdaq-Trader Universe + yfinance
    <button class="qmark" data-pop="caveat" aria-label="Reconstruction caveat" style="margin-left:8px;">i</button>
  </div>

  <!-- The popover bubble -->
  <div class="pop" id="pop"><span class="close" id="popClose">×</span><div id="popBody"></div></div>
</div>

<script>
const DATA = __DATA__;
const ROWS = DATA.rows;
const WEEKLY = DATA.weekly || [];
const LONG_TRENDS = DATA.long_trends || [];

// Surface when the data was last refreshed (build timestamp, in US Eastern).
// The daily-gmi workflow fires after the US close, so this is also how fresh
// today's GMI / T2108 / chart / Since-Day-1 numbers are.
{
  const el = document.getElementById('lastUpdated');
  if (el && DATA.built_at) {
    const asof = DATA.asof ? String(DATA.asof).slice(0, 10) : null;
    el.textContent = `Last updated ${DATA.built_at}` + (asof ? ` · data through ${asof}` : '');
  }
}

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

// Wire the four fixed controls
document.getElementById('ctlPrev').addEventListener('click', () => setIndex(Number(dateSlider.value) - 1));
document.getElementById('ctlNext').addEventListener('click', () => setIndex(Number(dateSlider.value) + 1));
document.getElementById('ctlToday').addEventListener('click', () => setIndex(ROWS.length - 1));

const ctlDay1Btn = document.getElementById('ctlDay1');
(function configureDay1Btn() {
  const cur = ROWS[ROWS.length - 1];
  if (cur && cur.d1d) {
    const arrow = cur.sd === "up" ? "▲" : "▼";
    ctlDay1Btn.textContent = `${arrow} Day 1 of current ${cur.sd}-trend · ${cur.d1d}`;
    ctlDay1Btn.title = `Jump to Day 1 of the current ST ${cur.sd}-trend`;
    if (cur.sd === "down") ctlDay1Btn.classList.add('down');
    ctlDay1Btn.addEventListener('click', () => setIndex(findNearestIndex(cur.d1d)));
  } else {
    ctlDay1Btn.style.display = "none";
  }
})();

// Long-trend pills (>= 30 trading days)
(function buildLongTrends() {
  pBox.innerHTML = "";
  LONG_TRENDS.forEach(t => {
    const arrow = t.dir === "up" ? "▲" : "▼";
    const b = document.createElement('button');
    b.className = "long-pill";
    b.innerHTML = `${arrow} ${t.d.slice(2)}<span class="pill-len">${t.len}d</span>`;
    b.style.color = t.dir === "up" ? "#4fa363" : "#d96250";
    b.style.border = "1px solid " + (t.dir === "up" ? "rgba(79,163,99,0.42)" : "rgba(217,98,80,0.42)");
    b.title = `Day 1 of ${t.dir}-trend that lasted ${t.len} trading days — ${t.d}`;
    b.onclick = () => setIndex(findNearestIndex(t.d));
    pBox.appendChild(b);
  });
})();

function findNearestIndex(dateStr) {
  if (dateMap.has(dateStr)) return dateMap.get(dateStr);
  let lo = 0, hi = ROWS.length - 1, best = 0;
  while (lo <= hi) {
    const m = (lo + hi) >> 1;
    if (ROWS[m].d <= dateStr) { best = m; lo = m + 1; } else { hi = m - 1; }
  }
  return best;
}

// Marker (user-selected date) vs window center (chart's visible 6-month window).
// setIndex(i) jumps BOTH (used by buttons, date picker, slider). setMarker(i)
// just moves the marker; the window only pans when the marker would leave view.
let markerIdx = ROWS.length - 1;
let windowCenterIdx = ROWS.length - 1;

function setIndex(i) {
  i = Math.max(0, Math.min(ROWS.length - 1, i));
  markerIdx = i;
  windowCenterIdx = i;
  dateSlider.value = String(i);
  datePick.value = ROWS[i].d;
  render();
}

function setMarker(i) {
  i = Math.max(0, Math.min(ROWS.length - 1, i));
  markerIdx = i;
  // Compute current visible window (matches drawSpark's logic).
  const HALF = 63;
  let dStart = windowCenterIdx - HALF;
  let dEnd = windowCenterIdx + HALF;
  if (dEnd > ROWS.length - 1) { dStart -= (dEnd - (ROWS.length - 1)); dEnd = ROWS.length - 1; }
  if (dStart < 0) { dEnd = Math.min(ROWS.length - 1, dEnd - dStart); dStart = 0; }
  // Pan only when marker reaches near an edge — keeps drag feel stable.
  if (i < dStart + 3)      windowCenterIdx = Math.max(0, i + HALF - 6);
  else if (i > dEnd - 3)   windowCenterIdx = Math.min(ROWS.length - 1, i - HALF + 6);
  dateSlider.value = String(i);
  datePick.value = ROWS[i].d;
  render();
}

dateSlider.addEventListener('input', e => setIndex(Number(e.target.value)));
dateSlider.addEventListener('change', e => setIndex(Number(e.target.value)));

// ============================================================================
// Chart-drag interaction: tap or drag on the SVG to scrub dates.
// Replaces the slider — feels more intuitive and matches how the chart actually
// displays time. Window auto-pans as the marker moves so the selected date is
// always visible.
// ============================================================================
(function attachChartDrag() {
  const svg = document.getElementById('spark');
  if (!svg) return;
  let dragging = false;

  function pointerToDate(e) {
    // Convert client coords to SVG viewBox coords via the screen CTM.
    const ctm = svg.getScreenCTM();
    if (!ctm) return null;
    const svgX = (e.clientX - ctm.e) / ctm.a;
    const v = window._chartView;
    if (!v) return null;
    const frac = Math.max(0, Math.min(1, (svgX - v.PADX) / v.plotW));
    const ts = v.firstTs + frac * v.tSpan;
    // Find the closest daily ROW by timestamp (linear within the visible window;
    // a binary search would be faster but the window is only ~126 bars).
    let bestIdx = v.dStart, bestDiff = Infinity;
    for (let i = v.dStart; i <= v.dEnd; i++) {
      const t = Date.parse(ROWS[i].d);
      const diff = Math.abs(t - ts);
      if (diff < bestDiff) { bestDiff = diff; bestIdx = i; }
    }
    // Allow dragging past the visible window — clamp to the FULL ROWS range,
    // then setIndex will recenter the chart.
    if (frac <= 0.02 && v.dStart > 0) bestIdx = Math.max(0, v.dStart - Math.ceil((0.02 - frac) * 100));
    if (frac >= 0.98 && v.dEnd < ROWS.length - 1) bestIdx = Math.min(ROWS.length - 1, v.dEnd + Math.ceil((frac - 0.98) * 100));
    return bestIdx;
  }

  svg.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    dragging = true;
    svg.classList.add('dragging');
    try { svg.setPointerCapture(e.pointerId); } catch (_) {}
    const idx = pointerToDate(e);
    if (idx != null) setMarker(idx);
  });
  svg.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    e.preventDefault();
    const idx = pointerToDate(e);
    if (idx != null) setMarker(idx);
  });
  function endDrag(e) {
    dragging = false;
    svg.classList.remove('dragging');
    try { if (e && e.pointerId != null) svg.releasePointerCapture(e.pointerId); } catch (_) {}
  }
  svg.addEventListener('pointerup', endDrag);
  svg.addEventListener('pointercancel', endDrag);
  svg.addEventListener('pointerleave', (e) => { if (!dragging) return; /* keep dragging via capture */ });
})();
datePick.addEventListener('change', e => setIndex(findNearestIndex(e.target.value)));

function classifyState(s, g) {
  if (s === 1) return {label: "GREEN — in market", cls: "green"};
  if (g <= 2) return {label: "RED — sidelined", cls: "red"};
  return {label: "YELLOW — transition", cls: "yellow"};
}

const STAGE_INFO = {
  1: {name: "Stage 1 — Basing",     note: "Price below 30-week MA, but tape firming. Not a buying stage.", cls: "s1"},
  2: {name: "Stage 2 — Advancing",  note: "Price above rising 30-week MA, 10wk > 30wk. The only stage suitable for long entries.", cls: "s2"},
  3: {name: "Stage 3 — Topping",    note: "Price above 30-week but breadth weakening (10wk crossing under, or 30wk flattening). Reduce exposure.", cls: "s3"},
  4: {name: "Stage 4 — Declining",  note: "Price below falling 30-week, 10wk < 30wk. Defensive — cash or inverse exposure.", cls: "s4"},
};


// ============================================================================
// Chart drawing: HLC bars (doji-style — vertical H–L line + close tick on right)
// ============================================================================

const MA_COLORS = { qqq: "#e7a924", m30: "#f5c042", w10: "#5fb37b", w30: "#c89a78" };
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

function drawSpark(centerIdx, markerIdx) {
  if (markerIdx === undefined) markerIdx = centerIdx;
  const svg = document.getElementById('spark');
  svg.innerHTML = "";
  const W = 800, H = 240, PADX = 6, PADY_TOP = 4, PADY_BOT = 30, VOL_H = 38;

  // Both views share the same ~6-month date window (locked axes across toggle).
  // Symmetric ±63 so the marker is centered. When the centerIdx is near today,
  // shift the window left so we always show ~126 bars (no shrinking at the right edge).
  const HALF = 63;
  let dStart = centerIdx - HALF;
  let dEnd = centerIdx + HALF;
  if (dEnd > ROWS.length - 1) { dStart -= (dEnd - (ROWS.length - 1)); dEnd = ROWS.length - 1; }
  if (dStart < 0) { dEnd = Math.min(ROWS.length - 1, dEnd - dStart); dStart = 0; }
  const firstDate = ROWS[dStart].d;
  const lastDate = ROWS[dEnd].d;
  let slice, localCenter, daily;
  if (VIEW === "daily") {
    daily = true;
    slice = ROWS.slice(dStart, dEnd + 1).filter(r => r.h != null && r.l != null);
    localCenter = slice.findIndex(r => r.d === ROWS[markerIdx].d);
    if (localCenter < 0) localCenter = markerIdx - dStart;
  } else {
    daily = false;
    slice = WEEKLY.filter(r => r.d >= firstDate && r.d <= lastDate && r.h != null);
    if (slice.length < 2) return;
    const selWeekDate = WEEKLY[ROWS[markerIdx].wi].d;
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
  const plotH = H - PADY_TOP - PADY_BOT - VOL_H;  // price plot, leaves a VOL_H band for volume
  const plotW = W - 2 * PADX;
  // Time-based x positioning: same calendar date sits at the same x in BOTH views.
  const firstTs = Date.parse(firstDate);
  const lastTs = Date.parse(lastDate);
  const tSpan = (lastTs - firstTs) || 1;
  const xAtDate = (dStr) => ((Date.parse(dStr) - firstTs) / tSpan) * plotW + PADX;
  const xAt = (i) => xAtDate(slice[i].d);
  // Price plot occupies [PADY_TOP, H - PADY_BOT - VOL_H]. Volume occupies the strip just below.
  const yAt = (v) => (H - PADY_BOT - VOL_H) - ((v - ymin) / yspan) * plotH;
  const volBaseY = H - PADY_BOT;   // bottom of volume band
  const volTopY = H - PADY_BOT - VOL_H + 2;  // top (with a 2px gap)
  // Publish the current chart window so the pointer-drag handler can map x -> date.
  window._chartView = { firstTs, lastTs, tSpan, dStart, dEnd, PADX, plotW, W };
  // Average bar width — used to size candle bodies. Daily ~3-4 px, weekly ~16-18 px.
  const barW = plotW / slice.length;

  // ===== RED shading = ST down-trend periods (matches the Day-N pill at the top) =====
  // Source = r.sd ("up"/"down"); positioning is identical in both views via xAtDate so toggling
  // Daily/Weekly doesn't shift anything.
  {
    let runStart = null;
    for (let i = dStart; i <= dEnd; i++) {
      const dr = ROWS[i];
      const isRed = dr.sd === "down";
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
    const GREEN = "#4fa363", RED = "#d96250";
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

  // ===== Volume bars (bottom band, color-matched to candle direction) =====
  if (maOn.qqq) {
    let maxV = 0;
    slice.forEach(r => { if (r.v != null && r.v > maxV) maxV = r.v; });
    if (maxV > 0) {
      const bodyW = Math.max(2.5, (slice.length > 1
        ? (Date.parse(slice[slice.length-1].d) - Date.parse(slice[0].d)) / (slice.length - 1) / tSpan * plotW * 0.7
        : plotW * 0.005));
      const volBandH = volBaseY - volTopY;
      slice.forEach((r, i) => {
        if (r.v == null || r.o == null) return;
        const cl = daily ? r.cl : r.c;
        if (cl == null) return;
        const x = xAt(i);
        const up = cl >= r.o;
        const color = up ? "rgba(46,160,67,0.55)" : "rgba(248,81,73,0.55)";
        const h = (r.v / maxV) * volBandH;
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', x - bodyW / 2);
        rect.setAttribute('y', volBaseY - h);
        rect.setAttribute('width', bodyW);
        rect.setAttribute('height', h);
        rect.setAttribute('fill', color);
        svg.appendChild(rect);
      });
      // Thin separator line between price and volume bands
      const sep = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      sep.setAttribute('x1', PADX); sep.setAttribute('x2', W - PADX);
      sep.setAttribute('y1', volTopY - 1); sep.setAttribute('y2', volTopY - 1);
      sep.setAttribute('stroke', '#3a3128'); sep.setAttribute('stroke-width', '0.5');
      sep.setAttribute('stroke-dasharray', '2,2');
      svg.appendChild(sep);
      // Tiny "Vol" label in the band
      const vlbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      vlbl.setAttribute('x', PADX + 2); vlbl.setAttribute('y', volTopY + 8);
      vlbl.setAttribute('font-size', '8');
      vlbl.setAttribute('font-family', 'ui-monospace,Menlo,Consolas,monospace');
      vlbl.setAttribute('fill', '#9c8c7c');
      vlbl.textContent = 'Vol';
      svg.appendChild(vlbl);
    }
  }

  // ===== Selected-date marker + dynamic value labels =====
  const selectedDailyDate = ROWS[markerIdx].d;
  const selDaily = ROWS[markerIdx];
  // In weekly view we still want the labels at the WEEK'S MA values (since that's what the chart shows).
  // selectedWeekly = the WEEKLY row whose Friday-date >= the selected daily date.
  const selWeeklyIdx = selDaily.wi;
  const selWeekly = WEEKLY[selWeeklyIdx] || null;
  {
    const x = xAtDate(selectedDailyDate);
    const vline = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    vline.setAttribute('x1', x); vline.setAttribute('x2', x);
    vline.setAttribute('y1', 0); vline.setAttribute('y2', H - PADY_BOT);
    vline.setAttribute('stroke', '#e7a924'); vline.setAttribute('stroke-width', '1.2');
    vline.setAttribute('stroke-dasharray', '3,3');
    vline.setAttribute('stroke-opacity', '0.85');
    svg.appendChild(vline);
    // Bottom selected-date label is rendered as HTML inside .x-axis-labels — see below.

    // ===== Top-left stat overlay (HTML, not SVG) =====
    // Replaces the per-line value pills that used to crowd the dashed-line on the
    // right side of the chart. Stacked rows in the top-left corner, off the
    // candle/volume body. Normal CSS sizing so labels don't get compressed by the
    // SVG's preserveAspectRatio="none" stretch on mobile.
    function fmtVol(v) {
      if (v == null) return null;
      if (v >= 1e9) return (v / 1e9).toFixed(2) + 'B';
      if (v >= 1e6) return (v / 1e6).toFixed(2) + 'M';
      if (v >= 1e3) return (v / 1e3).toFixed(1) + 'K';
      return String(v);
    }
    const statOverlay = document.getElementById('statOverlay');
    statOverlay.innerHTML = '';
    function addStat(label, val, color) {
      if (val == null) return;
      const row = document.createElement('div');
      row.className = 'stat-row';
      const colorStyle = color ? ` style="color:${color}"` : '';
      row.innerHTML = `<span class="label">${label}</span><span class="val"${colorStyle}>${val}</span>`;
      statOverlay.appendChild(row);
    }
    const qClose = daily ? selDaily.cl : (selWeekly && selWeekly.c);
    addStat('Q',   qClose != null ? qClose.toFixed(0) : null, "#f2ebe1");
    if (daily && maOn.m30 && selDaily.m30 != null)
      addStat('30d', selDaily.m30.toFixed(0), MA_COLORS.m30);
    if (!daily && maOn.w10 && selWeekly && selWeekly.m10 != null)
      addStat('10w', selWeekly.m10.toFixed(0), MA_COLORS.w10);
    if (!daily && maOn.w30 && selWeekly && selWeekly.m30 != null)
      addStat('30w', selWeekly.m30.toFixed(0), MA_COLORS.w30);
    const vol = daily ? selDaily.v : (selWeekly && selWeekly.v);
    const oo = daily ? selDaily.o : (selWeekly && selWeekly.o);
    if (vol != null && qClose != null && oo != null) {
      const volColor = qClose >= oo ? "#4fa363" : "#d96250";
      addStat('V', fmtVol(vol), volColor);
    }
  }

  // ===== X-axis date labels =====
  // Tick marks stay in SVG (aligned to chart geometry). Labels render as HTML
  // inside .x-axis-labels — normal CSS font sizing, no anisotropic scaling.
  const nTicks = 5;
  const xLabels = document.getElementById('xAxisLabels');
  xLabels.innerHTML = '';
  for (let k = 0; k < nTicks; k++) {
    const frac = k / (nTicks - 1);
    const ts = firstTs + frac * tSpan;
    const x = frac * plotW + PADX;
    const dateStr = new Date(ts).toISOString().slice(0, 7);  // YYYY-MM
    const span = document.createElement('span');
    span.className = 'x-tick' + (k === 0 ? ' start' : (k === nTicks - 1 ? ' end' : ''));
    span.style.left = (x / W * 100) + '%';
    span.textContent = dateStr;
    xLabels.appendChild(span);
    const tk = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    tk.setAttribute('x1', x); tk.setAttribute('x2', x);
    tk.setAttribute('y1', H - PADY_BOT); tk.setAttribute('y2', H - PADY_BOT + 3);
    tk.setAttribute('stroke', '#9c8c7c'); tk.setAttribute('stroke-width', '0.7');
    svg.appendChild(tk);
  }
  // Selected-date label (was an SVG text — now HTML overlay). Clamp horizontally
  // so the label never overflows the chart-wrap on either edge.
  {
    const xSel = xAtDate(selectedDailyDate);
    const sel = document.createElement('span');
    sel.className = 'x-selected';
    const pct = xSel / W * 100;
    sel.style.left = pct + '%';
    // Anchor depending on proximity to edges so the label sits inside the chart.
    if (pct < 12)       sel.style.transform = 'translateX(0)';
    else if (pct > 88)  sel.style.transform = 'translateX(-100%)';
    else                sel.style.transform = 'translateX(-50%)';
    sel.textContent = selectedDailyDate;
    xLabels.appendChild(sel);
  }
  const base = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  base.setAttribute('x1', PADX); base.setAttribute('x2', W - PADX);
  base.setAttribute('y1', H - PADY_BOT); base.setAttribute('y2', H - PADY_BOT);
  base.setAttribute('stroke', '#3a3128'); base.setAttribute('stroke-width', '0.7');
  svg.appendChild(base);
}

// ============================================================================
// Render
// ============================================================================

function render() {
  const i = markerIdx;
  const r = ROWS[i];
  const stateInfo = classifyState(r.s, r.g);

  // (date label removed in compact controls; the date picker shows the selected date already)
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
    if (r.t < 10) { label = "Buy zone"; cls = "green"; note = "Capitulation level. Historically a high-quality zone for accumulating SPY in tranches."; }
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
    const cell = document.getElementById(id + "Cell");
    if (v == null) {
      el.textContent = "—"; el.className = "since-val nv";
      if (cell) cell.className = "since-cell";
      return;
    }
    el.textContent = (v >= 0 ? "+" : "") + v.toFixed(2) + "%";
    const cls = v >= 0 ? "pos" : "neg";
    el.className = "since-val " + cls;
    if (cell) cell.className = "since-cell " + cls;
  }
  setPct('srd1', r.rd1);
  setPct('srd1tq', r.rd1tq);
  setPct('srd1sq', r.rd1sq);

  drawSpark(windowCenterIdx, markerIdx);
}

// ============================================================================
// Tooltip popover system — only the small ? button triggers it
// ============================================================================

const POP = {
  gmi: "<b>GMI — General Market Index</b><br>A daily 0–6 score of six market-health components. ≥4 for 2 consecutive days flips the gate GREEN (we're willing to buy long). ≤3 for 2 days flips RED (defensive — cash or hedge).",
  t2108: "<b>T2108 — NYSE breadth</b><br>The percent of NYSE stocks trading above their 40-day SMA. We use three zones:<br><b style='color:#4fa363'>&lt;10</b> = capitulation buy zone (accumulate SPY in tranches; historically marks lasting bottoms).<br><b style='color:#d09a2a'>10–30 / 70–80</b> = caution zones at either extreme.<br><b style='color:#d96250'>&gt;80</b> = extended; no new buys, take some profit.<br>30–70 is the healthy mid-range. Our value tracks the published T2108 at corr ≈ 0.93 (small +3–4 pt optimistic bias from survivorship in our universe).",
  state: "<b>Market state — GREEN / YELLOW / RED</b><br>Computed from the GMI with a 2-day confirmation rule. GREEN = 2 consecutive days ≥4. RED = 2 consecutive days <4 and not recovered. YELLOW = transition (GMI 3).",
  dayN: "<b>Day N of QQQ short-term trend</b><br>The count of consecutive trading days QQQ has been on its current side of the 30-day SMA. Resets to 1 when QQQ crosses through the line on a closing basis.",
  stage: "<b>Weinstein stage</b><br>The four-stage classification from Stan Weinstein, used for the long-term picture:<br><b>Stage 1 — Basing</b>: price below 30wk, MA flat/rising. No new buys.<br><b>Stage 2 — Advancing</b>: price above rising 30wk + 10wk > 30wk. <i>Only stage we buy long.</i><br><b>Stage 3 — Topping</b>: price above 30wk but breadth weakening. We sell into this.<br><b>Stage 4 — Declining</b>: price below falling 30wk + 10wk < 30wk. Defensive.",
  redshade: "<b>RED-shaded periods</b><br>Days when QQQ is in a <b>short-term down-trend</b> (closed below its 30-day SMA). Aligns with the Day-N pill at the top: shading ends exactly when the ST trend flips to up.<br><br>Note: this is distinct from the GMI gate (GREEN/RED badge above). The gate uses the full 6-component GMI score with a 2-day confirmation — it can stay RED for a few days after the ST trend turns up, by design.",
  qqq: "<b>QQQ candles</b><br>Standard OHLC candles. <span style='color:#4fa363;font-weight:600'>Green</span> = close ≥ open. <span style='color:#d96250;font-weight:600'>Red</span> = close &lt; open. Wick = high–low; body = open–close.<br><br><b>Daily view:</b> ~126 daily candles (6 months) centered on selected day.<br><b>Weekly view:</b> ~50 Friday-close candles (1 year) — the timeframe we use for the 10wk/30wk stage view.",
  m30: "<b>30-day SMA (daily)</b><br>The daily short-term trend anchor. QQQ closing above = ST up; below = ST down. Drives the Day-N count and components 3 & 4 of the GMI.",
  w10: "<b>10-week SMA (weekly chart)</b><br>Our medium-term hold line. Computed on Friday weekly closes. The <b>10wk crossing above 30wk</b> is the bull re-entry signal (confirmed live 2025-06 and 2026-05). The <b>10wk crossing below 30wk</b> confirms Stage 4 onset (April 2025 tariff decline).",
  w30: "<b>30-week SMA (weekly chart)</b><br>Our most important MA — Stan Weinstein's classic. Got us out before 2000 and 2008. Price above + line rising = Stage 2 uptrend — the only stage we buy long.",
  c1: "<b>Successful 10-day new high</b><br>Component 1 of GMI. Fires when ≥50% of stocks that hit a new 52-week high 10 trading days ago closed higher today. Tests whether breakouts are still being rewarded.",
  c2: "<b>≥100 new 52-week highs</b><br>Component 2 of GMI. Fires when more than 100 US stocks hit a new 52-week high today. Tests breadth of advance — a healthy bull has wide participation.",
  c3: "<b>QQQ daily up-trend</b><br>Component 3 of GMI. Reconstructed as QQQ close above its 30-day SMA. The Nasdaq-100's short-term trend.",
  c4: "<b>SPY daily up-trend</b><br>Component 4 of GMI. Reconstructed as SPY close above its 30-day SMA. The S&amp;P 500's short-term trend.",
  c5: "<b>QQQ weekly up-trend (Stage 2)</b><br>Component 5 of GMI. QQQ's weekly close above its 30-week SMA. The long-term Stage-2 anchor.",
  c6: "<b>IBD-50 above 50-day MA</b><br>Component 6 of GMI. Tracks whether the IBD Mutual Fund Index sits above its 50-day MA. Proxied here by FFTY (the IBD-50 ETF) spliced onto a basket of growth mutual funds for pre-2015 history.",
  longtrends: "<b>Long ST trends</b><br>Each pill is Day 1 of a past short-term trend (QQQ crossing its 30-day SMA) that lasted <b>30 or more trading days</b>. <span style='color:#4fa363'>▲ = up-trend</span>; <span style='color:#d96250'>▼ = down-trend</span>. The <b>Nd</b> badge shows how many trading days the trend lasted. Tap to jump the chart there. Showing the most recent 8.",
  since: "<b>Return since Day 1</b><br>Day 1 = the most recent day QQQ crossed its 30-day SMA (our daily ST-trend signal). This box shows how QQQ and two leveraged QQQ ETFs have moved since then to the close on the selected date.<br><br><b>QQQ</b> — the underlying (Invesco QQQ Trust, 1× Nasdaq-100).<br><b>TQQQ</b> — ProShares UltraPro QQQ. Targets <b>+3× the daily QQQ return</b>. The aggressive long play in an up-trend; compounds volatility drag over time so multi-month holds underperform 3× the simple QQQ move.<br><b>SQQQ</b> — ProShares UltraPro Short QQQ. Targets <b>−3× the daily QQQ return</b>. The inverse / short play used during down-trends.<br><br>A long-running positive QQQ return is a Stage-2 ride; a steep negative return is a Stage-4 leg. Watch for fading momentum near the end of a long streak.",
  vals: "<b>Indicator values on the selected date</b><br>The exact QQQ close on that day plus each of our three canonical MAs, with the percentage spread (QQQ above or below each MA). Use this to read the chart precisely instead of eyeballing.",
  fwd: "<b>Forward QQQ returns</b><br>What QQQ actually did 1, 5, 10, 20, and 60 trading days after the selected date. Lets you check 'if I had acted on this reading, what would have happened?' Blank for dates where the window hasn't closed yet.",
  caveat: "<b>Reconstruction caveat</b><br>This GMI is rebuilt from public data point-in-time. Match vs the published reference GMI: exact ~20% of days; within ±1 ~72%; correlation ~0.60. Systematically a touch optimistic in fast declines because of survivorship bias. Treat the number as directional, not precise.",
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
      VIEW === "daily" ? "QQQ · 6 mo · daily candles + 30-day SMA"
                       : "QQQ · 1 yr · weekly candles + 10-week & 30-week SMA";
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


def _format_et_now() -> str:
    """Return a human-readable build timestamp in US Eastern time, formatted
    like 'May 15, 2026 5:42 PM ET'. Eastern picks up DST automatically via
    America/New_York. Built cross-platform — %-d / %#d behaviour differs
    between POSIX and Windows so we compose the parts by hand."""
    now_et = datetime.now(timezone.utc).astimezone(ZoneInfo("America/New_York"))
    hour12 = now_et.hour % 12 or 12
    ampm = "AM" if now_et.hour < 12 else "PM"
    month = now_et.strftime("%b")
    return f"{month} {now_et.day}, {now_et.year} {hour12}:{now_et.minute:02d} {ampm} ET"


def main() -> None:
    # Diagnostic header so a CI failure shows env + cache state up front.
    import sys, platform
    print(f"build env: python={sys.version.split()[0]} platform={platform.system()}")
    try:
        import pandas as _pd
        import yfinance as _yf
        print(f"  pandas={_pd.__version__}  yfinance={_yf.__version__}")
    except Exception as e:
        print(f"  (lib version probe failed: {e})")
    for label, p in [("prices.parquet", PRICES_CACHE), ("qqq_ohlc.parquet", QQQ_OHLC_CACHE),
                     ("breadth_series.parquet", ROOT / "data" / "breadth" / "breadth_series.parquet")]:
        if p.exists():
            try:
                _df = pd.read_parquet(p)
                _df.index = pd.to_datetime(_df["date"]) if "date" in _df.columns else pd.to_datetime(_df.index)
                print(f"  {label}: {len(_df)} rows, ends {_df.index.max().date() if len(_df) else '(empty)'}")
            except Exception as e:
                print(f"  {label}: read failed ({type(e).__name__}: {e})")
        else:
            print(f"  {label}: MISSING")

    try:
        payload = build_payload()
        payload["built_at"] = _format_et_now()
        out = TEMPLATE.replace("__DATA__", json.dumps(payload, separators=(",", ":"), default=str))
        target = ROOT / "gmi_playground_daily.html"
        target.write_text(out, encoding="utf-8")
        print(f"wrote {target} — {len(out):,} bytes — {len(payload['rows'])} rows — asof {payload['asof']} — built {payload['built_at']}")
    except Exception:
        import traceback
        print("\n*** build_gmi_playground.py FAILED — full traceback follows ***", file=sys.stderr)
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
