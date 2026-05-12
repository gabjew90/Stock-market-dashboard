"""QQQ Short-Term Timing — the "Day N of the up/down-trend" count.

IMPORTANT: Dr. Wish has never published the exact rule that flips this signal (his GMI
component is "QQQQ daily trend positive" via "technical indicators not disclosed"). He
*does* say the 30-day moving average is "the most reliable indicator of the short term
trend." So this module APPROXIMATES the trend as: close above its 30-day simple MA = up,
below = down — and counts consecutive days since the last flip. Treat the output as a
proxy for his signal, not a reproduction of it.
See wiki/methodology/qqq-short-term-timing.md.
"""
from __future__ import annotations

import pandas as pd

_DEFAULT_WINDOW = 30


def _trend_series(close: pd.Series, window: int) -> pd.Series:
    ma = close.astype(float).rolling(window).mean()
    return (close.astype(float) > ma).where(ma.notna())  # True=up, False=down, NaN until enough data


def short_term_trend(daily_close: pd.Series, *, window: int = _DEFAULT_WINDOW) -> str:
    """'up' or 'down' for the latest bar (approximation — see module docstring)."""
    t = _trend_series(daily_close, window).dropna()
    if t.empty:
        raise ValueError(f"need at least {window} daily closes")
    return "up" if bool(t.iloc[-1]) else "down"


def trend_day_count(daily_close: pd.Series, *, window: int = _DEFAULT_WINDOW) -> int:
    """How many consecutive trading days the current (approximated) trend has been in effect — Dr. Wish's "Day N"."""
    t = _trend_series(daily_close, window).dropna()
    if t.empty:
        raise ValueError(f"need at least {window} daily closes")
    last = t.iloc[-1]
    n = 0
    for v in reversed(t.tolist()):
        if v == last:
            n += 1
        else:
            break
    return n
