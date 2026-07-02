"""The 30-week stage framework (Weinstein/Wish) and the weekly 4/10/30-week alignment.
Stages are defined by the latest weekly close vs the 30-week simple MA of closes, and
the slope of that MA. See wiki/methodology/moving-average-rules.md.
"""
from __future__ import annotations

import pandas as pd

# Relative-slope threshold used by _slope_sign(): a per-period relative change whose
# magnitude is at or below this counts the MA as "flat" (vs rising/falling).
_FLAT_SLOPE_EPS = 1e-3


def sma(close: pd.Series, window: int) -> pd.Series:
    """Simple moving average of `close` over `window` periods (NaN until enough data)."""
    return close.astype(float).rolling(window).mean()


def _slope_sign(ma: pd.Series, lookback: int = 4) -> int:
    """+1 rising / -1 falling / 0 flat — based on the change in the MA over `lookback` periods, scaled by level."""
    valid = ma.dropna()
    if len(valid) < lookback + 1:
        return 0
    change = valid.iloc[-1] - valid.iloc[-1 - lookback]
    level = abs(valid.iloc[-1]) or 1.0
    rel = change / level / lookback
    if rel > _FLAT_SLOPE_EPS:
        return 1
    if rel < -_FLAT_SLOPE_EPS:
        return -1
    return 0


def weekly_stage(weekly_close: pd.Series, *, ma_window: int = 30) -> int:
    """Return the current Weinstein stage (1, 2, 3, or 4) for a series of weekly closes.

    - Stage 2: close above a rising 30-week MA.
    - Stage 4: close below a falling 30-week MA.
    - Stage 1: close at/below the MA and the MA is flat (basing).
    - Stage 3: close above the MA but the MA is no longer rising (topping).
    """
    s = weekly_close.astype(float)
    ma = sma(s, ma_window)
    if ma.dropna().empty:
        raise ValueError(f"need at least {ma_window} weekly closes to classify a stage")
    last_close = s.iloc[-1]
    last_ma = ma.dropna().iloc[-1]
    slope = _slope_sign(ma)
    above = last_close > last_ma
    if above and slope > 0:
        return 2
    if (not above) and slope < 0:
        return 4
    if above:           # above but MA not rising -> topping
        return 3
    return 1            # at/below MA, MA not falling -> basing


def weinstein_stage_series(
    price_daily: pd.Series,
    w10: pd.Series,
    w30: pd.Series,
    *,
    slope_window_weeks: int = 8,
    rising_threshold_pct: float = 1.0,
    shallow_pullback_pct: float = 5.0,
    curl_window_weeks: int = 2,
) -> pd.Series:
    """Daily Stage 1/2/3/4 series per Stan Weinstein, calibrated to Dr. Wish's actual
    usage (see wiki/methodology/moving-average-rules.md). This is the dashboard's stage;
    `weekly_stage()` above is the simple point-in-time variant for one-off reads.

    `price_daily` is the daily close; `w10`/`w30` are the 10- and 30-week SMAs of
    weekly (W-FRI) closes forward-filled onto the same daily index.

      Stage 2 = price above 30wk AND 30wk clearly rising AND 10wk > 30wk (advancing —
                the only stage he buys long; the weekly 10>30 cross is his own
                confirmation, WW 2026-05-10 / the 2010-05-09 pension rule)
      Stage 3 = price above 30wk BUT 30wk flat / barely rising / curling down (topping)
      Stage 4 = price below 30wk AND 10wk < 30wk (cross-down confirmation) (declining)
      Stage 1 = basing / unconfirmed: EITHER a shallow pullback below a rising 30wk
                with 10wk still above, OR price back above a rising 30wk while the
                10wk>30wk cross hasn't confirmed yet (recovery not yet Stage 2)

    Refinements over a strict "is the slope > 0" check:

    1. **Slope uses a percentage threshold over `slope_window_weeks`**, not "any
       positive change vs 4 trading days ago". A 30wk SMA changes slowly even at
       tops, so the strict `> 0` rule treated a barely-flattening MA the same as a
       fast-rising one and erased every topping period (2018, 2021, 2024 had zero
       Stage-3 days). 1% over 8 weeks is the default.
    2. **A short-window curl guard**: after a crash-and-V-recovery the MA-8-weeks-ago
       is depressed, so the long-window slope can read "rising" while the MA is
       actually curling over *right now* (his "30-week curved down" eyeball test).
       `rising` therefore also requires the MA to be above its value
       `curl_window_weeks` weekly bars ago.
    3. **Stage 4 requires the 10wk-below-30wk cross** — without it, a 3-day price dip
       below the 30wk during a strong uptrend got mis-labelled Stage 4.

    The slope is computed on the weekly cadence to avoid a calendar artifact that
    would otherwise hit every Thursday (shift(N) on the daily-reindexed series lands
    on the previous Friday update, comparing the same weekly value to itself).
    """
    price = price_daily.astype(float)
    above_30wk = price > w30
    ten_above_thirty = w10 > w30
    # Depth qualifier: a pullback within `shallow_pullback_pct` of the 30wk can stay
    # Stage 1; anything deeper is a Stage-3 warning even before the slope flips. A
    # 5-day rolling-OR adds light hysteresis so a single rally day doesn't flip the
    # call back to Stage 1 while the trajectory is still down.
    deep_today = price < w30 * (1.0 - shallow_pullback_pct / 100.0)
    deep_recent = deep_today.rolling(5, min_periods=1).max().astype(bool)
    shallow_below = ~deep_recent

    # Weekly-cadence slope: deduplicate the daily-ffilled w30 back to one row per
    # actual weekly update, compare in % over the long window AND against the curl
    # window, then propagate the boolean back to daily via ffill.
    w30_weekly = w30[w30.ne(w30.shift())].dropna()
    slope_pct_weekly = (w30_weekly / w30_weekly.shift(slope_window_weeks) - 1.0) * 100.0
    not_curled = w30_weekly > w30_weekly.shift(curl_window_weeks)
    slope_rising_weekly = ((slope_pct_weekly > rising_threshold_pct) & not_curled).fillna(False)
    slope_rising = slope_rising_weekly.reindex(price.index, method="ffill").fillna(False).astype(bool)

    stage = pd.Series(0, index=price.index, dtype=int)
    # Above 30wk
    stage[above_30wk & slope_rising & ten_above_thirty] = 2   # confirmed uptrend
    stage[above_30wk & slope_rising & ~ten_above_thirty] = 1  # recovery, 10/30 cross not confirmed yet
    stage[above_30wk & ~slope_rising] = 3                     # topping above the line
    # Below 30wk + 10wk still above 30wk (10/30 cross hasn't fired yet)
    stage[~above_30wk & ten_above_thirty & slope_rising & shallow_below] = 1   # shallow pullback in uptrend
    stage[~above_30wk & ten_above_thirty & slope_rising & ~shallow_below] = 3  # deep drawdown — Stage 4 setup
    stage[~above_30wk & ten_above_thirty & ~slope_rising] = 3                  # slope decelerating — Stage 4 setup
    # Below 30wk + 10wk has crossed below 30wk = confirmed decline
    stage[~above_30wk & ~ten_above_thirty] = 4
    return stage


def ma_alignment_4_10_30(weekly_close: pd.Series) -> bool:
    """True iff, on the latest week, SMA4 > SMA10 > SMA30 of weekly closes (the weekly stock-trend rule)."""
    s = weekly_close.astype(float)
    a4, a10, a30 = sma(s, 4).iloc[-1], sma(s, 10).iloc[-1], sma(s, 30).iloc[-1]
    if pd.isna(a4) or pd.isna(a10) or pd.isna(a30):
        return False
    return bool(a4 > a10 > a30)


def tenwk_below_thirtywk(weekly_close: pd.Series) -> bool:
    """True iff the 10-week SMA is currently below the 30-week SMA (the Stage-4-onset confirmation)."""
    s = weekly_close.astype(float)
    a10, a30 = sma(s, 10).iloc[-1], sma(s, 30).iloc[-1]
    if pd.isna(a10) or pd.isna(a30):
        return False
    return bool(a10 < a30)
