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


def _split_multi(frame: pd.DataFrame, yf_tickers: Sequence[str]) -> dict[str, pd.DataFrame]:
    """Split a yfinance group_by='ticker' frame into {yf_ticker: tidy OHLCV DataFrame} (empty/missing dropped)."""
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


def _write_panel(panel_dir: Path, ticker: str, df: pd.DataFrame, *, append: bool) -> None:
    out = panel_dir / f"{ticker}.parquet"
    if append and out.exists():
        old = pd.read_parquet(out)
        df = pd.concat([old, df])
        df = df[~df.index.duplicated(keep="last")].sort_index()
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
    for batch in _batched(list(yf_map), batch_size):
        frame = _download_with_retry(dl, batch, period=yf_period, interval="1d")
        split = _split_multi(frame, batch)
        for yf_t in batch:
            df = split.get(yf_t)
            if df is None or df.empty:
                failed_yf.append(yf_t)
                continue
            _write_panel(panel_dir, yf_map[yf_t], df, append=append)
            written += 1
    # one retry pass over the failures (some are transient)
    if failed_yf:
        retry_yf = list(failed_yf)
        failed_yf = []
        for batch in _batched(retry_yf, batch_size):
            frame = _download_with_retry(dl, batch, period=yf_period, interval="1d")
            split = _split_multi(frame, batch)
            for yf_t in batch:
                df = split.get(yf_t)
                if df is None or df.empty:
                    failed_yf.append(yf_t)
                    continue
                _write_panel(panel_dir, yf_map[yf_t], df, append=append)
                written += 1
    if failed_yf:
        log.warning("%d tickers had no data and were skipped: %s%s", len(failed_yf), failed_yf[:20], " ..." if len(failed_yf) > 20 else "")
    return written


def fetch_panel(universe: pd.DataFrame, panel_dir: Path, *, downloader: Callable | None = None, force: bool = False, batch_size: int = 200) -> int:
    """Download the full daily history (`period='max'`) for every ticker in `universe` -> panel_dir/<TICKER>.parquet.
    Skips tickers whose parquet already exists unless `force`. Returns the number of panels written this run."""
    return _run_download(universe, panel_dir, yf_period="max", downloader=downloader, force=force, batch_size=batch_size, append=False)


def update_panel(universe: pd.DataFrame, panel_dir: Path, *, downloader: Callable | None = None, batch_size: int = 200) -> int:
    """Download the last ~month of bars (`period='1mo'`) for every ticker and append (dedup on date) to its panel parquet.
    Tickers the downloader returns nothing for are skipped (their last bar stays put). Returns the number updated."""
    return _run_download(universe, panel_dir, yf_period="1mo", downloader=downloader, force=False, batch_size=batch_size, append=True)
