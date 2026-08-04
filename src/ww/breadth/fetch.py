"""Pull the universe's daily price history into a per-ticker parquet panel via yfinance.
Used by both `ww breadth fetch` (full history) and `ww breadth update` (recent bars)."""
from __future__ import annotations

import logging
import time
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)

_OHLCV = ["open", "high", "low", "close", "adj_close", "volume"]
_YF_FIELDS = {"Open": "open", "High": "high", "Low": "low", "Close": "close", "Adj Close": "adj_close", "Volume": "volume"}


def normalize_for_yf(ticker: str) -> str:
    """Map an exchange ticker to Yahoo's convention (Yahoo uses '-' for share classes: BRK.B -> BRK-B)."""
    return ticker.replace(".", "-")


def _default_downloader(yf_tickers: Sequence[str], **kw) -> pd.DataFrame:
    import yfinance as yf

    return yf.download(list(yf_tickers), group_by="ticker", auto_adjust=False, threads=True, progress=False, **kw)


def _split_multi(frame: pd.DataFrame, yf_tickers: Sequence[str], *, stats: dict | None = None) -> dict[str, pd.DataFrame]:
    """Split a yfinance group_by='ticker' frame into {yf_ticker: tidy OHLCV DataFrame} (empty/missing dropped).

    `stats`, when given, accumulates fetch-quality counters for the caller to report.
    """
    out: dict[str, pd.DataFrame] = {}
    if frame is None or frame.empty:
        return out
    multi = isinstance(frame.columns, pd.MultiIndex)
    for t in yf_tickers:
        if multi:
            if t not in frame.columns.get_level_values(0):
                continue
            sub = frame[t]
        else:  # single-ticker download returns a flat frame
            sub = frame
        sub = sub.rename(columns={k: v for k, v in _YF_FIELDS.items() if k in sub.columns})
        sub = sub[[c for c in _OHLCV if c in sub.columns]].dropna(how="all")
        # Drop price-less rows. yfinance can return a placeholder bar for the
        # session in progress (or one it hasn't finished ingesting): NaN prices
        # but a non-NaN volume, which survives dropna(how="all"). Such a row is
        # not a bar — letting it through put a NaN close into the panel and
        # silently dropped the ticker out of that day's breadth universe.
        price_cols = [c for c in ("adj_close", "close") if c in sub.columns]
        if price_cols:
            before = len(sub)
            sub = sub.dropna(subset=price_cols, how="all")
            if stats is not None and len(sub) < before:
                stats["priceless_rows"] = stats.get("priceless_rows", 0) + (before - len(sub))
                stats["priceless_tickers"] = stats.get("priceless_tickers", 0) + 1
        if stats is not None and "adj_close" not in sub.columns:
            stats["no_adj_close"] = stats.get("no_adj_close", 0) + 1
        if sub.empty:
            continue
        sub.index = pd.to_datetime(sub.index)
        sub.index.name = "date"
        out[t] = sub
    return out


def _batched(seq: list[str], n: int) -> Iterable[list[str]]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def _download_with_retry(downloader: Callable, yf_tickers: list[str], *, retries: int = 2, delay: float = 2.0, **kw) -> pd.DataFrame:
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            f = downloader(yf_tickers, **kw)
            if f is not None and not f.empty:
                return f
        except Exception as e:  # noqa: BLE001 - yfinance throws various transient errors
            last_exc = e
        if attempt < retries:
            time.sleep(delay)
    if last_exc:
        log.warning("yfinance batch failed after retries: %s", last_exc)
    return pd.DataFrame()


def _write_panel(panel_dir: Path, ticker: str, df: pd.DataFrame, *, append: bool, stats: dict | None = None) -> None:
    out = panel_dir / f"{ticker}.parquet"
    if append and out.exists():
        old = pd.read_parquet(out)
        old = old[~old.index.duplicated(keep="last")].sort_index()
        df = df[~df.index.duplicated(keep="last")].sort_index()
        if stats is not None:
            # Bars the merge actively saved: a date both sides have, where the
            # re-fetch's price is empty but ours is not. Non-zero here means the
            # old keep="last" dedup WOULD have silently destroyed real data.
            overlap = df.index.intersection(old.index)
            for c in ("close", "adj_close"):
                if len(overlap) and c in df.columns and c in old.columns:
                    saved = int((df.loc[overlap, c].isna() & old.loc[overlap, c].notna()).sum())
                    if saved:
                        stats["rescued_bars"] = stats.get("rescued_bars", 0) + saved
                        break
        # Merge cell-by-cell, not row-by-row. The new download wins wherever it
        # actually carries a value, but a NaN in the re-fetch never erases a
        # good value we already have. The old `keep="last"` dedup was
        # destructive: a degraded re-fetch (missing the Adj Close column, or a
        # partial response) overwrote bars that were already correct, which is
        # how n_nyse collapsed from ~1,919 to 1,480 for 2026-07-24 between two
        # runs of the same day's data (build-dashboard #135 -> #136).
        merged = df.combine_first(old)
        cols = [c for c in _OHLCV if c in merged.columns] + [c for c in merged.columns if c not in _OHLCV]
        df = merged[cols].sort_index()
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out)


def _run_download(
    universe: pd.DataFrame,
    panel_dir: Path,
    *,
    yf_period: str,
    downloader: Callable | None,
    force: bool,
    batch_size: int,
    append: bool,
) -> int:
    panel_dir = Path(panel_dir)
    panel_dir.mkdir(parents=True, exist_ok=True)
    dl = downloader or _default_downloader
    tickers = list(universe["ticker"].astype(str))
    todo = tickers if (force or append) else [t for t in tickers if not (panel_dir / f"{t}.parquet").exists()]
    yf_map = {normalize_for_yf(t): t for t in todo}
    written = 0
    failed_yf: list[str] = []
    stats: dict[str, int] = {}
    for batch in _batched(list(yf_map), batch_size):
        frame = _download_with_retry(dl, batch, period=yf_period, interval="1d")
        split = _split_multi(frame, batch, stats=stats)
        for yf_t in batch:
            df = split.get(yf_t)
            if df is None or df.empty:
                failed_yf.append(yf_t)
                continue
            _write_panel(panel_dir, yf_map[yf_t], df, append=append, stats=stats)
            written += 1
    # one retry pass over the failures (some are transient)
    if failed_yf:
        retry_yf = list(failed_yf)
        failed_yf = []
        for batch in _batched(retry_yf, batch_size):
            frame = _download_with_retry(dl, batch, period=yf_period, interval="1d")
            split = _split_multi(frame, batch, stats=stats)
            for yf_t in batch:
                df = split.get(yf_t)
                if df is None or df.empty:
                    failed_yf.append(yf_t)
                    continue
                _write_panel(panel_dir, yf_map[yf_t], df, append=append, stats=stats)
                written += 1
    if failed_yf:
        log.warning("%d tickers had no data and were skipped: %s%s", len(failed_yf), failed_yf[:20], " ..." if len(failed_yf) > 20 else "")
    _report_fetch_quality(stats, attempted=len(yf_map))
    return written


# A degraded yfinance response no longer corrupts the panel (the merge is
# non-destructive), which also means it no longer shows up as a failed build.
# Report it explicitly so the degradation stays visible in breadth_update.log
# instead of passing silently.
_DEGRADED_FETCH_FRACTION = 0.05


def _report_fetch_quality(stats: dict[str, int], *, attempted: int) -> None:
    if not stats or not attempted:
        return
    priceless_tickers = stats.get("priceless_tickers", 0)
    parts = []
    if priceless_tickers:
        parts.append(f"{stats.get('priceless_rows', 0)} price-less rows dropped across {priceless_tickers} tickers")
    if stats.get("no_adj_close"):
        parts.append(f"{stats['no_adj_close']} tickers returned no adj_close column")
    if stats.get("rescued_bars"):
        parts.append(f"{stats['rescued_bars']} existing bars preserved against empty re-fetch cells")
    if not parts:
        return
    degraded = priceless_tickers >= _DEGRADED_FETCH_FRACTION * attempted
    log.warning(
        "%sfetch quality over %d tickers: %s",
        "DEGRADED yfinance response — " if degraded else "",
        attempted,
        "; ".join(parts),
    )


def fetch_panel(universe: pd.DataFrame, panel_dir: Path, *, downloader: Callable | None = None, force: bool = False, batch_size: int = 200) -> int:
    """Download the full daily history (`period='max'`) for every ticker in `universe` -> panel_dir/<TICKER>.parquet.
    Skips tickers whose parquet already exists unless `force`. Returns the number of panels written this run."""
    return _run_download(universe, panel_dir, yf_period="max", downloader=downloader, force=force, batch_size=batch_size, append=False)


def update_panel(universe: pd.DataFrame, panel_dir: Path, *, downloader: Callable | None = None, batch_size: int = 200) -> int:
    """Download the last ~month of bars (`period='1mo'`) for every ticker and append (dedup on date) to its panel parquet.
    Tickers the downloader returns nothing for are skipped (their last bar stays put). Returns the number updated."""
    return _run_download(universe, panel_dir, yf_period="1mo", downloader=downloader, force=False, batch_size=batch_size, append=True)
