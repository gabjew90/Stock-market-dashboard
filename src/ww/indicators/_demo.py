"""Illustrative (NOT real) fixtures so `ww compute gmi/t2108 --demo` has something tangible
to print offline. Numbers here are made up to demonstrate the formulas, not actual market data.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ww.indicators.provider import StubProvider

DEMO_DATE = "2014-08-01"


def _trend(n, lo, hi, freq):
    idx = pd.date_range("2014-01-01" if freq == "B" else "2014-01-05", periods=n, freq=freq)
    c = np.linspace(lo, hi, n)
    return pd.DataFrame({"open": c, "high": c, "low": c, "close": c}, index=idx)


def demo_provider() -> StubProvider:
    """A StubProvider where every GMI component is bullish — score 6 — with illustrative inputs."""
    return StubProvider(
        prices={
            ("QQQ", "1d"): _trend(400, 100, 300, "B"),
            ("SPY", "1d"): _trend(400, 100, 300, "B"),
            ("QQQ", "1wk"): _trend(120, 100, 300, "W-SUN"),
        },
        nasdaq_new_highs_lows=pd.DataFrame({"new_highs": [320], "new_lows": [12]}, index=pd.to_datetime([DEMO_DATE])),
        successful_10day_new_high={DEMO_DATE: (170, 240)},     # ~71% >= 50% -> positive
        ibd_mutual_fund_index=pd.Series(np.linspace(10, 30, 90), index=pd.date_range("2014-04-01", periods=90, freq="B")),
        pct_above_ma={(("AAA", "BBB", "CCC"), 40, DEMO_DATE): 66.67},
    )
