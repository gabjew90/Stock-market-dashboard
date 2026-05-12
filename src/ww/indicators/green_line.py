"""Green Line Breakouts (Dr. Wish): an all-time-high level that has held >= 3 months,
drawn on a monthly chart; the breakout is a close above the most recent such level.
See wiki/methodology/green-line-breakouts.md.
"""
from __future__ import annotations

import pandas as pd

_DEFAULT_MIN_MONTHS = 3


def green_lines(monthly: pd.DataFrame, *, min_months_held: int = _DEFAULT_MIN_MONTHS) -> list[tuple[pd.Timestamp, float]]:
    """All green lines over the history, oldest first, as (month_end_timestamp, price_level).

    A bar's `high` is a green line if it is a running all-time high AND no later bar's
    `high` exceeds it for at least `min_months_held` subsequent bars. (The very last
    `min_months_held` bars can't yet qualify.)
    """
    highs = monthly["high"].astype(float)
    n = len(highs)
    out: list[tuple[pd.Timestamp, float]] = []
    running_ath = float("-inf")
    for i in range(n):
        h = highs.iloc[i]
        if h <= running_ath:
            continue
        running_ath = h
        # need min_months_held subsequent bars, all with high < h
        if i + min_months_held >= n:
            continue
        if (highs.iloc[i + 1 : i + 1 + min_months_held] < h).all():
            out.append((highs.index[i], float(h)))
    return out


def current_green_line(monthly: pd.DataFrame, *, min_months_held: int = _DEFAULT_MIN_MONTHS) -> float | None:
    """The most recent green line level, or None if the stock has never set one (always making new highs)."""
    gls = green_lines(monthly, min_months_held=min_months_held)
    return gls[-1][1] if gls else None


def is_green_line_breakout(*, close: float, green_line: float | None) -> bool:
    """True iff `close` is strictly above the (non-None) green line — the GLB entry condition."""
    return green_line is not None and close > green_line
