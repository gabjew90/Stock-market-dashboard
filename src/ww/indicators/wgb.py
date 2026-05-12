"""Weekly Green Bar (Dr. Wish's TC2000 scan), all conditions on the WEEKLY timeframe:

    avgc4 > avgc10 and avgc10 > avgc30        # 4wk > 10wk > 30wk simple MAs of close
    L <= avgc4 and C > avgc4                  # this week's low dipped to/below the 4wk avg, close recovered above it
    C > C1                                    # close higher than prior week's close
    avgc4 > avgc4.1                           # the 4wk avg is rising

See wiki/methodology/moving-average-rules.md.
"""
from __future__ import annotations

import pandas as pd


def weekly_green_bars(weekly_ohlc: pd.DataFrame) -> pd.DataFrame:
    """Return the sub-frame of weeks that are WGBs (same columns as the input, including 'low' for the trailing stop)."""
    df = weekly_ohlc.copy()
    c = df["close"].astype(float)
    a4, a10, a30 = c.rolling(4).mean(), c.rolling(10).mean(), c.rolling(30).mean()
    cond = (
        (a4 > a10) & (a10 > a30)
        & (df["low"].astype(float) <= a4) & (c > a4)
        & (c > c.shift(1))
        & (a4 > a4.shift(1))
    )
    return df.loc[cond.fillna(False)]


def wgb_trailing_stop(weekly_ohlc: pd.DataFrame) -> float | None:
    """The current WGB trailing stop: the `low` of the most recent Weekly Green Bar, or None if there are none yet."""
    wgbs = weekly_green_bars(weekly_ohlc)
    return None if wgbs.empty else float(wgbs["low"].iloc[-1])
