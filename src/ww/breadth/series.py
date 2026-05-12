"""Compute the daily breadth series from the per-ticker price panel, and the growth-fund proxy."""
from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from pathlib import Path

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

# default growth-fund basket for the IBD-Mutual-Fund-Index proxy (free via yfinance, long histories)
DEFAULT_FUND_BASKET = ("AGTHX", "FCNTX", "TRBCX", "VWUSX")
_FUND_FALLBACK = "VUG"
_MIN_PRICE = 5.0
_MA_MIN_BARS = 40        # need >= this many *prior* bars for the 40d-MA universe membership
_HL_WINDOW = 252         # 52 weeks of trading days
_HL_MIN_BARS = 250


def _load_close_matrix(panel_dir: Path, tickers: Sequence[str]) -> pd.DataFrame:
    """Wide DataFrame of adjusted closes: index = date, columns = ticker (NaN where a ticker has no bar)."""
    panel_dir = Path(panel_dir)
    series = {}
    for t in tickers:
        p = panel_dir / f"{t}.parquet"
        if not p.exists():
            continue
        df = pd.read_parquet(p)
        col = "adj_close" if "adj_close" in df.columns else "close"
        series[t] = df[col].astype(float)
    if not series:
        return pd.DataFrame()
    mat = pd.DataFrame(series).sort_index()
    return mat


def compute_breadth_series(panel_dir: Path, universe: pd.DataFrame, *, min_date: str | None = None) -> pd.DataFrame:
    """Daily breadth over the panel. Returns one row per trading date with the columns documented in the design spec §4."""
    tickers = list(universe["ticker"].astype(str))
    nyse = set(universe.loc[universe["in_nyse"].astype(bool), "ticker"].astype(str))
    closes = _load_close_matrix(panel_dir, tickers)
    if closes.empty:
        return pd.DataFrame(columns=["date"])
    if min_date:
        closes = closes.loc[pd.Timestamp(min_date):]

    has_bar = closes.notna()
    bars_so_far = has_bar.cumsum()                                    # cumulative count of bars up to and incl. each date
    prior_bars = bars_so_far - has_bar.astype(int)                    # bars strictly before this date
    above_5 = closes >= _MIN_PRICE

    ma40 = closes.rolling(_MA_MIN_BARS, min_periods=_MA_MIN_BARS).mean()
    ma50 = closes.rolling(50, min_periods=50).mean()
    ma200 = closes.rolling(200, min_periods=200).mean()
    roll_max = closes.rolling(_HL_WINDOW, min_periods=_HL_MIN_BARS).max()
    roll_min = closes.rolling(_HL_WINDOW, min_periods=_HL_MIN_BARS).min()

    in_uni_ma = has_bar & (prior_bars >= _MA_MIN_BARS) & above_5      # universe membership for the MA-based ratios
    in_uni_hl = has_bar & (prior_bars >= _HL_MIN_BARS) & above_5      # universe membership for the high/low counts
    nyse_mask = pd.Series(closes.columns.isin(nyse), index=closes.columns)

    def _pct_above(ma: pd.DataFrame, in_uni: pd.DataFrame, cols_mask: pd.Series | None = None) -> pd.Series:
        m = in_uni.loc[:, cols_mask.index[cols_mask]] if cols_mask is not None else in_uni
        c = closes.loc[:, m.columns]
        a = ma.loc[:, m.columns]
        above = (c > a) & m
        denom = m.sum(axis=1)
        return (100.0 * above.sum(axis=1) / denom.replace(0, np.nan)).fillna(0.0)

    def _count_n(in_uni: pd.DataFrame, cols_mask: pd.Series | None = None) -> pd.Series:
        m = in_uni.loc[:, cols_mask.index[cols_mask]] if cols_mask is not None else in_uni
        return m.sum(axis=1).astype(int)

    new_high = (closes >= roll_max) & in_uni_hl
    new_low = (closes <= roll_min) & in_uni_hl

    out = pd.DataFrame(index=closes.index)
    out["n_nyse"] = _count_n(in_uni_ma, nyse_mask)
    out["n_broad"] = _count_n(in_uni_ma)
    out["t2108_nyse"] = _pct_above(ma40, in_uni_ma, nyse_mask)
    out["t2108_broad"] = _pct_above(ma40, in_uni_ma)
    out["pct_above_50dma_broad"] = _pct_above(ma50, in_uni_ma)
    out["pct_above_200dma_broad"] = _pct_above(ma200, in_uni_ma)
    out["new_52w_highs"] = new_high.sum(axis=1).astype(int)
    out["new_52w_lows"] = new_low.sum(axis=1).astype(int)
    out["nasdaq_new_52w_highs"] = new_high.loc[:, ~closes.columns.isin(nyse)].sum(axis=1).astype(int)
    out["nasdaq_new_52w_lows"] = new_low.loc[:, ~closes.columns.isin(nyse)].sum(axis=1).astype(int)

    # Successful 10-Day New High: of the stocks that made a new 52w high 10 trading days ago, how many closed higher today?
    new_high_10ago = new_high.shift(10).fillna(False)                  # was a new high 10 trading rows ago
    close_10ago = closes.shift(10)
    higher = (closes > close_10ago) & new_high_10ago & has_bar        # still trading today and up vs 10 days ago
    out["s10_total"] = new_high_10ago.where(has_bar, False).sum(axis=1).astype(int)
    out["s10_higher"] = higher.sum(axis=1).astype(int)

    median_n = out["n_broad"].replace(0, np.nan).median()
    out["coverage_note"] = np.where(out["n_broad"] < 0.5 * (median_n or 0), "thin", "")

    # only keep dates where there's any universe at all
    out = out[out["n_broad"] > 0].copy()
    out = out.reset_index().rename(columns={"index": "date"})
    if "date" not in out.columns:
        out = out.rename(columns={out.columns[0]: "date"})
    out["date"] = pd.to_datetime(out["date"])
    return out


def build_fund_proxy(*, tickers: Sequence[str] = DEFAULT_FUND_BASKET, downloader: Callable | None = None) -> pd.Series:
    """Equal-weighted average of the basket's adjusted closes (the IBD-Mutual-Fund-Index proxy). yfinance unless `downloader` given.
    Tickers that come back empty are dropped; if the whole basket is empty, falls back to a single growth ETF."""
    def _dl(ts):
        if downloader is not None:
            return downloader(list(ts), period="max", interval="1d")
        import yfinance as yf
        return yf.download(list(ts), group_by="ticker", auto_adjust=False, threads=True, progress=False, period="max", interval="1d")

    frame = _dl(tickers)
    cols: dict[str, pd.Series] = {}
    if frame is not None and not frame.empty:
        multi = isinstance(frame.columns, pd.MultiIndex)
        for t in tickers:
            sub = frame[t] if (multi and t in frame.columns.get_level_values(0)) else (frame if not multi else None)
            if sub is None:
                continue
            field = "Adj Close" if "Adj Close" in getattr(sub, "columns", []) else ("adj_close" if "adj_close" in getattr(sub, "columns", []) else None)
            if field is None:
                continue
            s = sub[field].astype(float).dropna()
            if not s.empty:
                cols[t] = s
    if not cols:
        log.warning("growth-fund basket empty; falling back to %s", _FUND_FALLBACK)
        f2 = _dl([_FUND_FALLBACK])
        if f2 is not None and not f2.empty:
            s = (f2[_FUND_FALLBACK] if isinstance(f2.columns, pd.MultiIndex) else f2)
            field = "Adj Close" if "Adj Close" in s.columns else "adj_close"
            cols[_FUND_FALLBACK] = s[field].astype(float).dropna()
    if not cols:
        return pd.Series(dtype=float)
    proxy = pd.DataFrame(cols).mean(axis=1).sort_index()
    proxy.name = "fund_proxy"
    proxy.index.name = "date"
    return proxy
