"""A small pluggable data interface for the indicator code.

`prices()` returns a tidy OHLCV DataFrame (lowercase columns `open/high/low/close/volume`,
a DatetimeIndex). The breadth/fund methods are needed only by the GMI/T2108 indicators
(Plan 4b); the free provider raises `DataUnavailable` for them with a pointer to the
methodology page that explains what data they need.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

import pandas as pd

_OHLCV = ["open", "high", "low", "close", "volume"]


class DataUnavailable(RuntimeError):
    """Raised when a provider cannot supply a requested series (e.g. market breadth from free sources)."""


class DataProvider(ABC):
    """Interface the indicator code depends on. Implementations: YFinanceProvider, StubProvider."""

    @abstractmethod
    def prices(self, ticker: str, interval: str = "1d", *, start: str | None = None, end: str | None = None) -> pd.DataFrame:
        """OHLCV bars for `ticker`. `interval` is one of '1d', '1wk', '1mo'. Index is a DatetimeIndex."""

    def nasdaq_new_highs_lows(self, start: str, end: str) -> pd.DataFrame:  # pragma: no cover - default
        """Daily count of new 52-week highs and lows in the ~4,000-stock universe (cols: 'new_highs','new_lows')."""
        raise DataUnavailable("Nasdaq new-high/new-low counts are not available from free sources — see wiki/methodology/gmi.md.")

    def pct_above_ma(self, universe: Sequence[str], window: int, date: str) -> float:  # pragma: no cover - default
        """Percent of `universe` trading above their `window`-day simple MA on `date` (T2108 with window=40, NYSE universe)."""
        raise DataUnavailable("Computing % of a full equity universe above its MA needs bulk price data — see wiki/methodology/t2108.md.")

    def ibd_mutual_fund_index(self, start: str, end: str) -> pd.Series:  # pragma: no cover - default
        """Daily level of the IBD Mutual Fund Index (a GMI component) — not freely available."""
        raise DataUnavailable("The IBD Mutual Fund Index is not available from free sources — see wiki/methodology/gmi.md.")

    def successful_10day_new_high(self, date: str) -> tuple[int, int]:  # pragma: no cover - default
        """For stocks that hit a 52-week high 10 trading days before `date`: (#closed-higher-than-10d-ago, #total).

        GMI component 1: the indicator is positive when num_higher >= 50% of num_total (the 2014 refinement;
        the original 2005 rule was num_higher >= 100). Needs a daily new-high panel — not available from free sources.
        """
        raise DataUnavailable("The 'Successful 10-Day New High' count needs a daily new-high panel — see wiki/methodology/gmi.md.")


class StubProvider(DataProvider):
    """In-memory provider for tests and offline demos. Construct with whatever fixtures you have."""

    def __init__(
        self,
        prices: dict[tuple[str, str], pd.DataFrame] | None = None,
        *,
        nasdaq_new_highs_lows: pd.DataFrame | None = None,
        pct_above_ma: dict[tuple, float] | None = None,
        ibd_mutual_fund_index: pd.Series | None = None,
        successful_10day_new_high: dict[str, tuple[int, int]] | None = None,
    ) -> None:
        self._prices = prices or {}
        self._nhl = nasdaq_new_highs_lows
        self._pct = pct_above_ma or {}
        self._fund = ibd_mutual_fund_index
        self._s10 = successful_10day_new_high or {}

    def prices(self, ticker: str, interval: str = "1d", *, start: str | None = None, end: str | None = None) -> pd.DataFrame:
        return self._prices[(ticker, interval)]

    def nasdaq_new_highs_lows(self, start: str, end: str) -> pd.DataFrame:
        if self._nhl is None:
            raise DataUnavailable("no nasdaq_new_highs_lows fixture supplied to this StubProvider")
        return self._nhl

    def pct_above_ma(self, universe: Sequence[str], window: int, date: str) -> float:
        key = (tuple(universe), window, date)
        if key not in self._pct:
            raise DataUnavailable(f"no pct_above_ma fixture for {key}")
        return self._pct[key]

    def ibd_mutual_fund_index(self, start: str, end: str) -> pd.Series:
        if self._fund is None:
            raise DataUnavailable("no ibd_mutual_fund_index fixture supplied to this StubProvider")
        return self._fund

    def successful_10day_new_high(self, date: str) -> tuple[int, int]:
        if date not in self._s10:
            raise DataUnavailable(f"no successful_10day_new_high fixture for {date}")
        return self._s10[date]


class YFinanceProvider(DataProvider):
    """Live prices via yfinance. Breadth/fund data is not available — those methods raise DataUnavailable (the ABC default)."""

    def prices(self, ticker: str, interval: str = "1d", *, start: str | None = None, end: str | None = None) -> pd.DataFrame:
        import yfinance as yf  # local import so the module loads without a network/yfinance at import time

        period = None if (start or end) else "max"
        raw = yf.download(ticker, interval=interval, start=start, end=end, period=period, auto_adjust=False, progress=False, multi_level_index=False)
        if raw is None or raw.empty:
            raise DataUnavailable(f"yfinance returned no data for {ticker} ({interval})")
        df = raw.rename(columns=str.lower)
        df = df[[c for c in _OHLCV if c in df.columns]].copy()
        df.index = pd.to_datetime(df.index)
        df.index.name = "date"
        return df
