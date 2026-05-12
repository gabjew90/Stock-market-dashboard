"""A DataProvider backed by the locally-built breadth series (Plan B1) + a growth-fund proxy.

`prices()` delegates to YFinanceProvider (with an optional in-memory `prices_cache` so callers that
compute many dates pre-fetch QQQ/SPY once). The breadth/fund methods serve the precomputed columns —
so `gmi()` returns a real 0-6 and `t2108()` a real reading. See the breadth-data design spec.
"""
from __future__ import annotations

import json
import logging
from collections.abc import Sequence
from pathlib import Path

import pandas as pd

from ww.indicators.provider import DataProvider, DataUnavailable, YFinanceProvider

log = logging.getLogger(__name__)


class BreadthProvider(DataProvider):
    def __init__(
        self,
        root: Path = Path("."),
        *,
        flavor: str = "auto",          # "nyse" | "broad" | "auto" (reads validate.json, default "broad")
        nh_universe: str = "nasdaq",   # "nasdaq" | "broad" — which new-high/low columns nasdaq_new_highs_lows returns
        prices_cache: dict[tuple[str, str], pd.DataFrame] | None = None,
    ) -> None:
        self.root = Path(root)
        bdir = self.root / "data" / "breadth"
        series_path = bdir / "breadth_series.parquet"
        if not series_path.exists():
            raise RuntimeError(f"no {series_path} — run `ww breadth fetch && ww breadth build` first")
        self._bs = pd.read_parquet(series_path)
        self._bs["date"] = pd.to_datetime(self._bs["date"])
        self._bs = self._bs.set_index("date").sort_index()
        fp_path = bdir / "fund_proxy.parquet"
        if fp_path.exists():
            fp = pd.read_parquet(fp_path)
            fp["date"] = pd.to_datetime(fp["date"])
            self._fund = fp.set_index("date")["fund_proxy"].sort_index()
        else:
            self._fund = pd.Series(dtype=float, name="fund_proxy")
        # resolve flavor
        if flavor == "auto":
            vj = bdir / "validate.json"
            try:
                flavor = json.loads(vj.read_text(encoding="utf-8")).get("chosen_flavor", "broad") if vj.exists() else "broad"
            except Exception:  # noqa: BLE001
                flavor = "broad"
        if flavor not in ("nyse", "broad"):
            flavor = "broad"
        self.flavor = flavor
        self.nh_universe = "nasdaq" if nh_universe == "nasdaq" else "broad"
        self._prices_cache = prices_cache or {}
        self._yf: YFinanceProvider | None = None
        self._warned_fund = False

    # --- helpers ---------------------------------------------------------------
    def _row(self, date: str) -> pd.Series:
        d = pd.Timestamp(date)
        if d not in self._bs.index:
            raise DataUnavailable(f"breadth series has no row for {d.date()}")
        return self._bs.loc[d]

    # --- DataProvider ----------------------------------------------------------
    def prices(self, ticker: str, interval: str = "1d", *, start: str | None = None, end: str | None = None) -> pd.DataFrame:
        key = (ticker, interval)
        if key in self._prices_cache:
            return self._prices_cache[key]
        if self._yf is None:
            self._yf = YFinanceProvider()
        df = self._yf.prices(ticker, interval, start=start, end=end)
        self._prices_cache[key] = df
        return df

    def pct_above_ma(self, universe: Sequence[str], window: int, date: str) -> float:
        row = self._row(date)
        if window == 40:
            return float(row[f"t2108_{self.flavor}"])
        if window == 50:
            return float(row["pct_above_50dma_broad"])
        if window == 200:
            return float(row["pct_above_200dma_broad"])
        raise DataUnavailable(f"no precomputed % above {window}-day MA — only 40/50/200 are built")

    def nasdaq_new_highs_lows(self, start: str, end: str) -> pd.DataFrame:
        s, e = pd.Timestamp(start), pd.Timestamp(end)
        win = self._bs.loc[s:e]
        hi = "nasdaq_new_52w_highs" if self.nh_universe == "nasdaq" else "new_52w_highs"
        lo = "nasdaq_new_52w_lows" if self.nh_universe == "nasdaq" else "new_52w_lows"
        return win[[hi, lo]].rename(columns={hi: "new_highs", lo: "new_lows"})

    def successful_10day_new_high(self, date: str) -> tuple[int, int]:
        row = self._row(date)
        return int(row["s10_higher"]), int(row["s10_total"])

    def ibd_mutual_fund_index(self, start: str, end: str) -> pd.Series:
        if not self._warned_fund:
            log.warning("BreadthProvider.ibd_mutual_fund_index returns a GROWTH-FUND PROXY (avg of large growth funds), not IBD's actual Mutual Fund Index — see wiki/methodology/gmi.md.")
            self._warned_fund = True
        if self._fund.empty:
            raise DataUnavailable("no fund_proxy.parquet — run `ww breadth build`")
        return self._fund.loc[pd.Timestamp(start):pd.Timestamp(end)]
