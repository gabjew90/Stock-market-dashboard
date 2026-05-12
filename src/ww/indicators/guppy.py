"""GMMA / Guppy Multiple Moving Average — the RWB ("Red White Blue", bullish) and
BWR ("Blue White Red", bearish) patterns Dr. Wish uses for stock selection, plus the
Red Line Count (RLC) he reads off the daily chart.

NOTE: Dr. Wish never published the exact EMA periods. This module uses the standard
TC2000/Guppy defaults — short (red): 3, 5, 8, 10, 12, 15 ; long (blue): 30, 35, 40,
45, 50, 60 — which is what most "GMMA" indicators ship with. The shapes and rules below
match his prose (band over band + white space + slope; close below all 12 = BWR); only
the numeric periods are an assumption.
See wiki/methodology/moving-average-rules.md.
"""
from __future__ import annotations

import pandas as pd

SHORT_PERIODS = (3, 5, 8, 10, 12, 15)   # "red" band
LONG_PERIODS = (30, 35, 40, 45, 50, 60)  # "blue" band


def gmma(close: pd.Series, *, short_periods=SHORT_PERIODS, long_periods=LONG_PERIODS) -> pd.DataFrame:
    """A DataFrame of the 12 EMAs (short band first, then long band), indexed like `close`."""
    s = close.astype(float)
    cols = {f"ema{p}": s.ewm(span=p, adjust=False).mean() for p in (*short_periods, *long_periods)}
    return pd.DataFrame(cols)


def _bands(close: pd.Series, short_periods, long_periods):
    g = gmma(close, short_periods=short_periods, long_periods=long_periods)
    short = g[[f"ema{p}" for p in short_periods]]
    long_ = g[[f"ema{p}" for p in long_periods]]
    return short, long_


def rwb_state(close: pd.Series, *, short_periods=SHORT_PERIODS, long_periods=LONG_PERIODS) -> str:
    """Classify the latest bar as 'RWB' (bull), 'BWR' (bear), or 'transition'.

    RWB  := every short ("red") EMA > every long ("blue") EMA, and both bands rising.
    BWR  := every short EMA < every long EMA, AND the close is below all 12 EMAs.
    else := 'transition' (bands overlapping / direction unclear — Dr. Wish stays on the sidelines).
    """
    short, long_ = _bands(close, short_periods, long_periods)
    s_last, l_last = short.iloc[-1], long_.iloc[-1]
    c_last = float(close.iloc[-1])
    # slopes over ~10 bars
    look = min(10, len(close) - 1)
    rising = (short.iloc[-1] > short.iloc[-1 - look]).all() and (long_.iloc[-1] > long_.iloc[-1 - look]).all()
    falling = (short.iloc[-1] < short.iloc[-1 - look]).all() and (long_.iloc[-1] < long_.iloc[-1 - look]).all()
    if (s_last.min() > l_last.max()) and rising:
        return "RWB"
    if (s_last.max() < l_last.min()) and falling and c_last < min(s_last.min(), l_last.min()):
        return "BWR"
    return "transition"


def red_line_count(close: pd.Series, *, short_periods=SHORT_PERIODS) -> int:
    """RLC: how many of the 6 short ("red") EMAs the latest close is above (0..6) — read off Dr. Wish's daily chart."""
    s = close.astype(float)
    last_c = float(s.iloc[-1])
    return int(sum(last_c > s.ewm(span=p, adjust=False).mean().iloc[-1] for p in short_periods))
