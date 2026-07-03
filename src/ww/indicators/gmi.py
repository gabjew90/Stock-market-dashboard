"""The General Market Index (GMI) — Dr. Wish's 0-6 composite. Six binary components,
each worth 1 point; GMI >= 4 is "GREEN" (be invested), <= 3 is defensive. See
wiki/methodology/gmi.md for the components and their evolution.

Components 3/4/5 (QQQ daily, SPY daily, QQQ weekly trend) are computed from free price
data. Components 1/2/6 need a daily new-high panel and the IBD Mutual Fund Index, which
the free provider can't supply — those come back as `None` and are listed in `.unavailable`.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from ww.indicators.ma_stages import sma
from ww.indicators.provider import DataProvider, DataUnavailable
from ww.indicators.qqq_timing import short_term_trend

# component keys, in GMI order
_COMPONENTS = (
    "successful_10day_new_high",   # 1
    "new_highs_ge_100",            # 2
    "qqq_daily_trend",             # 3
    "spy_daily_trend",             # 4
    "qqq_weekly_trend",            # 5
    "ibd_fund_above_50d",          # 6
)


@dataclass
class GMIResult:
    score: int                                   # number of components that are True (0..6)
    components: dict[str, bool | None]            # per-component verdict; None = data unavailable
    unavailable: list[str] = field(default_factory=list)

    @property
    def is_green(self) -> bool:
        """GMI 'GREEN' = be invested (score >= 4). Note: with components missing, score understates the true GMI."""
        return self.score >= 4


def _daily_trend_up(provider: DataProvider, ticker: str, date: str) -> bool | None:
    try:
        df = provider.prices(ticker, "1d")
    except (DataUnavailable, KeyError):
        return None
    try:
        # Truncate at `date` so a historical GMI reflects the trend as of that day,
        # not the trend at the end of whatever series the provider returned.
        return short_term_trend(df["close"].loc[: pd.Timestamp(date)]) == "up"
    except ValueError:
        return None


def _qqq_weekly_above_30wk(provider: DataProvider, date: str) -> bool | None:
    try:
        df = provider.prices("QQQ", "1wk")
    except (DataUnavailable, KeyError):
        return None
    c = df["close"].astype(float).loc[: pd.Timestamp(date)]
    ma30 = sma(c, 30).dropna()
    if ma30.empty:
        return None
    return bool(c.iloc[-1] > ma30.iloc[-1])


def _successful_10day(provider: DataProvider, date: str, *, original_rule: bool) -> bool | None:
    try:
        higher, total = provider.successful_10day_new_high(date)
    except DataUnavailable:
        return None
    if total <= 0:
        return None
    if original_rule:
        return higher >= 100
    return higher >= 0.5 * total


def _new_highs_ge_100(provider: DataProvider, date: str) -> bool | None:
    try:
        nhl = provider.nasdaq_new_highs_lows(date, date)
    except DataUnavailable:
        return None
    d = pd.Timestamp(date)
    row = nhl.loc[:d]
    if row.empty:
        return None
    return bool(row["new_highs"].iloc[-1] >= 100)


def _ibd_fund_above_50d(provider: DataProvider, date: str) -> bool | None:
    d = pd.Timestamp(date)
    try:
        s = provider.ibd_mutual_fund_index((d - pd.Timedelta(days=160)).date().isoformat(), d.date().isoformat())
    except DataUnavailable:
        return None
    s = s.astype(float).loc[:d]
    if len(s) < 50:
        return None
    return bool(s.iloc[-1] > s.rolling(50).mean().iloc[-1])


def gmi(provider: DataProvider, date: str, *, original_rule: bool = False) -> GMIResult:
    """Compute the GMI for `date`. `original_rule=True` uses the 2005 component-1 threshold (>=100);
    the default uses the 2014 refinement (>= 50% of stocks)."""
    verdicts: dict[str, bool | None] = {
        "successful_10day_new_high": _successful_10day(provider, date, original_rule=original_rule),
        "new_highs_ge_100": _new_highs_ge_100(provider, date),
        "qqq_daily_trend": _daily_trend_up(provider, "QQQ", date),
        "spy_daily_trend": _daily_trend_up(provider, "SPY", date),
        "qqq_weekly_trend": _qqq_weekly_above_30wk(provider, date),
        "ibd_fund_above_50d": _ibd_fund_above_50d(provider, date),
    }
    unavailable = [k for k in _COMPONENTS if verdicts[k] is None]
    score = sum(1 for v in verdicts.values() if v is True)
    return GMIResult(score=score, components=verdicts, unavailable=unavailable)
