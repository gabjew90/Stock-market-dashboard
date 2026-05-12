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
