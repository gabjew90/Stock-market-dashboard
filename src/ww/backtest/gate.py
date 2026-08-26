"""Rebuild the daily 0-6 GMI (point-in-time, look-back only) and run the GREEN/RED state machine."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

_GMI_THRESHOLD = 4         # Buy: GMI >= 4 ("> 3") for two consecutive days (WW 2012-04-30)
_GMI_EXIT_THRESHOLD = 3    # Sell: GMI *below* 3 (i.e. <= 2) for two consecutive days (WW 2012-04-16, 2014-08-03).
                           # GMI == 3 is a HOLD state - raise stops, no new buys, but it does NOT flip the
                           # signal to Red. Corroborated 2017-04-16: GMI at 1 and "still on a GREEN signal.
                           # One more day below 3 will change it to RED."
_S10_FRAC = 0.5            # July 2005 rule: >= 50% of the 10-day-ago new-high stocks closed higher today
_S10_COUNT_MIN = 100       # April 2005 launch rule, kept as an OR-branch: >= 100 successful 10-day new highs
_S10_MIN_DENOM = 20        # Feb 2008 addition: the 50% branch needs a denominator of at least 20
_NEW_HIGHS_MIN = 100
_QQQ_DAILY_TREND_WINDOW = 30   # the 'QQQ daily trend up' proxy = close > trailing 30-day SMA (the documented evidence)
_QQQ_WEEKLY_TREND_WINDOW = 30  # weeks
_FUND_MA_WINDOW = 50           # days


def _above_trailing_sma(series: pd.Series, window: int) -> pd.Series:
    """Boolean: each day, is `series` above its trailing `window`-period SMA? False where the SMA isn't defined yet."""
    s = series.astype(float)
    ma = s.rolling(window, min_periods=window).mean()
    return (s > ma).where(ma.notna(), False).astype(bool)


def _sma_rising(series: pd.Series, window: int, *, lookback: int = 4) -> pd.Series:
    """Boolean: each day, is `series`'s trailing `window`-period SMA higher than it was `lookback` periods ago?"""
    ma = series.astype(float).rolling(window, min_periods=window).mean()
    return (ma > ma.shift(lookback)).where(ma.notna() & ma.shift(lookback).notna(), False).astype(bool)


def successful_10day_component(higher: pd.Series, total: pd.Series) -> pd.Series:
    """GMI component 1, in the form the published table has carried since 2008-02-11:

        >= 100 successful 10-day new highs, OR (>= 50% of them AND a denominator of >= 20).

    The definitional history is: raw count > 100 (2005-04-26) -> count *or* >= 50% (2005-07-11)
    -> *and* denominator >= 20 (2008-02-11), the last added because "the 50% requirement is not
    enough if it is based on fewer than 20 stocks." Thresholds are inclusive (WW 2007-09-04).
    """
    higher = higher.astype(float)
    total = total.astype(float)
    by_count = higher >= _S10_COUNT_MIN
    by_frac = (total >= _S10_MIN_DENOM) & (higher >= _S10_FRAC * total)
    return (by_count | by_frac).fillna(False).astype(bool)


def _reconstructed_gmi(root: Path, prices: pd.DataFrame) -> pd.Series:
    root = Path(root)
    bs = pd.read_parquet(root / "data" / "breadth" / "breadth_series.parquet")
    bs["date"] = pd.to_datetime(bs["date"])
    bs = bs.set_index("date").sort_index()
    idx = bs.index
    qqq = prices["QQQ"].reindex(idx).ffill()
    spy = prices["SPY"].reindex(idx).ffill() if "SPY" in prices.columns else qqq
    fp_path = root / "data" / "breadth" / "fund_proxy.parquet"
    if fp_path.exists():
        fp = pd.read_parquet(fp_path); fp["date"] = pd.to_datetime(fp["date"])
        fund = fp.set_index("date")["fund_proxy"].reindex(idx).ffill()
    else:
        fund = pd.Series(np.nan, index=idx)

    c1 = successful_10day_component(bs["s10_higher"], bs["s10_total"])
    # Component 2 counts new highs across his whole ~4,000-stock universe (NYSE + Nasdaq + AMEX),
    # which is what the >= 100 threshold was calibrated on - not the Nasdaq-only subset.
    c2 = bs["new_52w_highs"] >= _NEW_HIGHS_MIN
    c3 = _above_trailing_sma(qqq, _QQQ_DAILY_TREND_WINDOW)
    c4 = _above_trailing_sma(spy, _QQQ_DAILY_TREND_WINDOW)
    # weekly QQQ trend: resample to weekly closes, "above its trailing 30-week SMA", forward-fill onto daily
    wk = qqq.resample("W-FRI").last().dropna()
    c5_wk = _above_trailing_sma(wk, _QQQ_WEEKLY_TREND_WINDOW)
    c5 = c5_wk.reindex(idx, method="ffill").fillna(False).astype(bool)
    c6 = _above_trailing_sma(fund, _FUND_MA_WINDOW) if fund.notna().any() else pd.Series(False, index=idx)

    gmi = (c1.astype(int) + c2.astype(int) + c3.astype(int) + c4.astype(int) + c5.astype(int) + c6.astype(int)).astype(float)
    gmi.name = "gmi"
    return gmi


def daily_gmi_series(root: Path, prices: pd.DataFrame, *, source: str = "reconstructed") -> pd.Series:
    """Daily 0-6 GMI on the breadth-series calendar. `source`: 'reconstructed' (default) or 'reported'
    (raw/timeline.parquet's gmi_value, forward-filled; reconstructed on the leading gap; `.attrs['reported_coverage']` set)."""
    recon = _reconstructed_gmi(root, prices)
    if source == "reconstructed":
        return recon
    if source != "reported":
        raise ValueError(f"unknown gmi source {source!r}")
    tl_path = Path(root) / "raw" / "timeline.parquet"
    tl = pd.read_parquet(tl_path)
    tl["date"] = pd.to_datetime(tl["date"]).dt.normalize()
    rep = tl.dropna(subset=["gmi_value"]).groupby("date")["gmi_value"].first().astype(float)
    rep_daily = rep.reindex(recon.index, method="ffill")        # forward-fill his posted GMI
    out = rep_daily.where(rep_daily.notna(), recon)             # leading gap -> reconstructed fallback
    out.name = "gmi"
    out.attrs["reported_coverage"] = float(rep_daily.notna().mean())
    return out


def green_state_machine(gmi: pd.Series, *, gmi_threshold: int = _GMI_THRESHOLD,
                        exit_threshold: int = _GMI_EXIT_THRESHOLD, confirm_in: int = 2, confirm_out: int = 2,
                        extra_ok: pd.Series | None = None) -> pd.Series:
    """Dr. Wish's GREEN/RED signal, which is **asymmetric** around a hold state at GMI == 3.

    GREEN flips on the `confirm_in`-th consecutive day with ``gmi >= gmi_threshold`` (and `extra_ok`
    if given). RED flips on the `confirm_out`-th consecutive day with ``gmi < exit_threshold`` OR
    (`extra_ok` is False). A day that is neither - a GMI of exactly 3 - resets **both** streaks: it
    is a hold, so it breaks a run toward GREEN and a run toward RED alike.

    The two-day persistence was adopted 2011-11-28 after a self-audit found three one-day whipsaws
    among 12 regime changes: "If I had used a rule that said that a change in trend had to persist
    for two days to be valid, I would have avoided these false signals. I will use that rule."
    The thresholds are his: Buy at "GMI > 3 for two consecutive days" (2012-04-30), Sell at
    "2 consecutive days below 3" (2012-04-16). Passing ``exit_threshold=gmi_threshold`` restores the
    old symmetric behaviour, which exits on a hold reading and whipsaws ~43% more often.
    """
    g = gmi.astype(float)
    enter_ok = g >= gmi_threshold
    exit_bad = g < exit_threshold
    if extra_ok is not None:
        extra = extra_ok.reindex(g.index).fillna(False).astype(bool)
        enter_ok = enter_ok & extra
        exit_bad = exit_bad | ~extra
    out = pd.Series(False, index=g.index)
    state = False
    streak_ok = 0
    streak_bad = 0
    for ts in g.index:
        streak_ok = streak_ok + 1 if enter_ok.loc[ts] else 0
        streak_bad = streak_bad + 1 if exit_bad.loc[ts] else 0
        if not state and streak_ok >= confirm_in:
            state = True
        elif state and streak_bad >= confirm_out:
            state = False
        out.loc[ts] = state
    return out


def market_state_gate(gmi: pd.Series, prices: pd.DataFrame, *, gmi_threshold: int = _GMI_THRESHOLD,
                      exit_threshold: int = _GMI_EXIT_THRESHOLD,
                      confirm_in: int = 2, confirm_out: int = 2, require_stage2: bool = False,
                      require_st_up: bool = False) -> pd.Series:
    """Full gate: the GMI state machine, optionally requiring Stage-2 (QQQ > rising 30-week SMA) and/or
    QQQ-short-term-trend-up. `gmi` and `prices['QQQ']` should share/cover the calendar."""
    idx = gmi.index
    extra = pd.Series(True, index=idx)
    if require_stage2:
        qqq = prices["QQQ"].reindex(idx).ffill()
        wk = qqq.resample("W-FRI").last().dropna()
        above = _above_trailing_sma(wk, _QQQ_WEEKLY_TREND_WINDOW)
        rising = _sma_rising(wk, _QQQ_WEEKLY_TREND_WINDOW)
        st2_wk = above & rising
        extra = extra & st2_wk.reindex(idx, method="ffill").fillna(False).astype(bool)
    if require_st_up:
        qqq = prices["QQQ"].reindex(idx).ffill()
        # compute the 30d-SMA "up/down" point-in-time over the daily series
        st_up = _above_trailing_sma(qqq, _QQQ_DAILY_TREND_WINDOW)   # same proxy short_term_trend uses
        extra = extra & st_up
    return green_state_machine(gmi, gmi_threshold=gmi_threshold, exit_threshold=exit_threshold,
                               confirm_in=confirm_in, confirm_out=confirm_out,
                               extra_ok=(extra if (require_stage2 or require_st_up) else None))
