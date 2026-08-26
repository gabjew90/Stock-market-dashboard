"""The 30-week stage framework (Weinstein/Wish) and the weekly 4/10/30-week alignment.
See wiki/methodology/moving-average-rules.md.

ONE rule, three callers. `classify_stage()` below is the single definition; `weekly_stage()`
(point-in-time, used by `ww compute`), `stage_series()` (the dashboard) and the backtest's
Stage-2 filter all route through it. They used to be three separate implementations that
disagreed on 10-15% of days - the same drift that produced the GMI component-1 bug.

CALIBRATION NOTE. His stage definitions turn on whether the 30-week average is "roughly
flat", and he never published a threshold for that - not once in 4,700 posts. `_FLAT_BAND_PCT`
is therefore *our* number, not his. It is the only invented parameter here; every other
condition is quoted on the methodology page. Treat stage output as calibrated rather than
reproduced, the way `qqq_timing.py` treats the short-term trend rule.
"""
from __future__ import annotations

import pandas as pd

# --- the one invented parameter (see CALIBRATION NOTE) -----------------------------
_FLAT_BAND_PCT = 1.0         # |change in the 30wk over _SLOPE_WINDOW_WEEKS| <= this => "flat"
_SLOPE_WINDOW_WEEKS = 8      # the span we read the average's direction over
_CURL_WINDOW_WEEKS = 2       # his "30-week curved down" test: also require the MA above its value 2 bars ago
_SHALLOW_PULLBACK_PCT = 5.0  # a dip this far below a rising 30wk is still a Stage-2 pullback


def sma(close: pd.Series, window: int) -> pd.Series:
    """Simple moving average of `close` over `window` periods (NaN until enough data)."""
    return close.astype(float).rolling(window).mean()


def classify_stage(*, above_30wk: bool, slope: int, ten_above_thirty: bool, shallow_below: bool,
                   prior_stage: int = 0) -> int:
    """The four stages, from his own statements. `slope` is -1 falling / 0 flat / +1 rising.

    - **Stage 2 - advancing.** "The stock is above its rising 30-week average." The only stage
      he buys long (WW 2012-07-23).
    - **Stage 3 - topping.** Above the 30-week, but the average flattens or begins to turn down,
      with the 10-week still above it - i.e. it arrived here from an advance.
    - **Stage 4 - declining.** Both conditions, stated together in WW 2015-09-20: "When the 10
      week average falls below the 30 week average *and* the 30 week average turns down, that
      index is in a Stage 4 down-trend." A falling average alone is not enough; neither is the
      cross alone.
    - **Stage 1 - basing.** "Consolidating near or below its 30-week average after a prior
      decline. The average is roughly flat."

    `prior_stage` is the previous bar's stage (0 when unknown), and it is *required*, not a
    refinement: **a flat 30-week looks identical at a base and at a top.** Weinstein's stages are
    a cycle (1 -> 2 -> 3 -> 4 -> 1), so the same instantaneous reading means "basing" when it
    follows a decline and "topping" when it follows an advance. Without this the January-2022 top
    scored 20 days of Stage 1 - "basing" in the middle of a market top.
    """
    came_from_advance = prior_stage in (2, 3)
    if above_30wk:
        if not ten_above_thirty:
            # Price back over the line with the 10/30 cross unconfirmed: a recovery off a low,
            # unless we arrived from an advance, in which case it is the top rolling over.
            return 3 if came_from_advance else 1
        return 2 if slope > 0 else 3                   # advancing vs topping
    if ten_above_thirty:                               # dip below the line inside an up-trend
        return 2 if (slope > 0 and shallow_below) else 3
    if slope < 0:
        return 4                                       # both Stage-4 conditions met
    if slope == 0:
        return 3 if came_from_advance else 1           # flat average: topping vs basing
    return 3                                           # sharp break below a still-rising average


def _slope_state_weekly(w30_weekly: pd.Series, *, slope_window_weeks: int, flat_band_pct: float,
                        curl_window_weeks: int) -> pd.Series:
    """-1 / 0 / +1 for the 30-week average's direction, on the weekly cadence.

    Rising needs BOTH a change above `flat_band_pct` over `slope_window_weeks` AND the average
    above its value `curl_window_weeks` bars ago - the curl guard. Without it a V-recovery reads
    "rising" off a depressed base while the average is visibly curling over right now, which is
    the eyeball test he applies ("an ominous curving down of the 30 week average").
    """
    change_pct = (w30_weekly / w30_weekly.shift(slope_window_weeks) - 1.0) * 100.0
    curled_down = w30_weekly <= w30_weekly.shift(curl_window_weeks)
    state = pd.Series(0, index=w30_weekly.index, dtype=int)
    state[(change_pct > flat_band_pct) & ~curled_down] = 1
    state[change_pct < -flat_band_pct] = -1
    return state


def stage_series(
    price_daily: pd.Series,
    w10: pd.Series,
    w30: pd.Series,
    *,
    slope_window_weeks: int = _SLOPE_WINDOW_WEEKS,
    flat_band_pct: float = _FLAT_BAND_PCT,
    shallow_pullback_pct: float = _SHALLOW_PULLBACK_PCT,
    curl_window_weeks: int = _CURL_WINDOW_WEEKS,
) -> pd.Series:
    """Daily Stage 1/2/3/4 series. `price_daily` is the daily close; `w10`/`w30` are the 10- and
    30-week SMAs of weekly (W-FRI) closes forward-filled onto the same daily index.

    Every day is classified by `classify_stage()`; this function only prepares its four inputs.
    """
    price = price_daily.astype(float)
    above_30wk = (price > w30).fillna(False).astype(bool)
    ten_above_thirty = (w10 > w30).fillna(False).astype(bool)
    # Depth qualifier for the pullback branch, with a 5-day rolling-OR of hysteresis so that one
    # rally day does not flip the call back while the trajectory is still down.
    deep_today = (price < w30 * (1.0 - shallow_pullback_pct / 100.0)).fillna(False).astype(bool)
    shallow_below = ~deep_today.rolling(5, min_periods=1).max().astype(bool)

    # Slope on the weekly cadence: dedupe the daily-ffilled w30 back to one row per weekly update,
    # otherwise shift(N) on the daily series lands on the same weekly value every Thursday.
    w30_weekly = w30[w30.ne(w30.shift())].dropna()
    slope = _slope_state_weekly(w30_weekly, slope_window_weeks=slope_window_weeks,
                                flat_band_pct=flat_band_pct, curl_window_weeks=curl_window_weeks)
    slope = slope.reindex(price.index, method="ffill").fillna(0).astype(int)

    # Sequential, because classify_stage() needs the prior bar to tell a base from a top. There is
    # deliberately no vectorised twin: a second copy of the rule is exactly how the GMI component-1
    # and Stage-2 definitions drifted apart.
    a = above_30wk.to_numpy(); t = ten_above_thirty.to_numpy()
    sh = shallow_below.to_numpy(); sl = slope.to_numpy()
    out = []
    prior = 0
    for i in range(len(price)):
        prior = classify_stage(above_30wk=bool(a[i]), slope=int(sl[i]),
                               ten_above_thirty=bool(t[i]), shallow_below=bool(sh[i]),
                               prior_stage=prior)
        out.append(prior)
    return pd.Series(out, index=price.index, dtype=int)


#: Back-compat alias - the dashboard imports this name.
weinstein_stage_series = stage_series


def weekly_stage(weekly_close: pd.Series, *, ma_window: int = 30, **kwargs) -> int:
    """The current stage from a series of weekly closes - the point-in-time variant `ww compute`
    uses. Routes through the same rule as `stage_series()`, so the two cannot disagree."""
    s = weekly_close.astype(float)
    w30 = sma(s, ma_window)
    if w30.dropna().empty:
        raise ValueError(f"need at least {ma_window} weekly closes to classify a stage")
    return int(stage_series(s, sma(s, 10), w30, **kwargs).iloc[-1])


def ma_alignment_4_10_30(weekly_close: pd.Series) -> bool:
    """True iff, on the latest week, SMA4 > SMA10 > SMA30 of weekly closes (the weekly stock-trend rule)."""
    s = weekly_close.astype(float)
    a4, a10, a30 = sma(s, 4).iloc[-1], sma(s, 10).iloc[-1], sma(s, 30).iloc[-1]
    if pd.isna(a4) or pd.isna(a10) or pd.isna(a30):
        return False
    return bool(a4 > a10 > a30)


def tenwk_below_thirtywk(weekly_close: pd.Series) -> bool:
    """True iff the 10-week SMA is currently below the 30-week SMA (half of the Stage-4 test)."""
    s = weekly_close.astype(float)
    a10, a30 = sma(s, 10).iloc[-1], sma(s, 30).iloc[-1]
    if pd.isna(a10) or pd.isna(a30):
        return False
    return bool(a10 < a30)


def is_stage2(price_daily: pd.Series, w10: pd.Series, w30: pd.Series, **kwargs) -> pd.Series:
    """Boolean Stage-2 mask - the single definition the dashboard, `ww compute` and the
    backtest's `require_stage2` filter all share."""
    return stage_series(price_daily, w10, w30, **kwargs) == 2
