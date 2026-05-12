"""T2108 — the percentage of stocks (NYSE universe) trading above their 40-day simple
moving average. A Worden/TC2000 indicator Dr. Wish uses for overbought/oversold context.
See wiki/methodology/t2108.md.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

import pandas as pd

from ww.indicators.provider import DataProvider

_DEFAULT_WINDOW = 40


def t2108(provider: DataProvider, date: str, *, universe: Sequence[str], window: int = _DEFAULT_WINDOW) -> float:
    """T2108 on `date`: percent of `universe` trading above its `window`-day SMA.

    Delegates to `provider.pct_above_ma`; raises `DataUnavailable` if the provider can't
    supply a full-universe panel (the free provider can't — see the methodology page).
    """
    return provider.pct_above_ma(universe, window, date)


def t2108_from_prices(price_frames: Mapping[str, pd.DataFrame], date, *, window: int = _DEFAULT_WINDOW) -> float:
    """Compute the same percentage directly from a dict of OHLC frames (one per ticker).

    A ticker counts toward the denominator only if it has >= `window` closes on/before `date`;
    it counts toward the numerator if its close on `date` (or the last close on/before `date`)
    is above its `window`-period SMA there. Useful for demonstrating the formula on any basket
    (T2108 proper uses the whole NYSE list).
    """
    d = pd.Timestamp(date)
    above = 0
    total = 0
    for _ticker, df in price_frames.items():
        s = df["close"].astype(float)
        s = s.loc[:d]
        if len(s) < window:
            continue
        ma = s.rolling(window).mean().iloc[-1]
        total += 1
        if s.iloc[-1] > ma:
            above += 1
    if total == 0:
        raise ValueError("no ticker in price_frames has >= window closes on/before the date")
    return 100.0 * above / total
