"""Build the US-common-stock universe from the free Nasdaq Trader symbol-directory files."""
from __future__ import annotations

import re
from pathlib import Path

import httpx
import pandas as pd

_BASE = "https://www.nasdaqtrader.com/dynamic/SymDir"
_FILES = ("nasdaqtraded.txt",)   # the comprehensive file (all Nasdaq-traded securities on all US exchanges)
_USER_AGENT = "wishing-wealth-wiki/0.1 (personal research project)"
# Listing-exchange codes we keep: N = NYSE, A = NYSE American (AMEX), Q = Nasdaq.
_KEEP_EXCHANGES = {"N", "A", "Q"}
# Reject a security if its name matches any of these (case-insensitive, word-bounded) — preferreds, warrants, rights, etc.
_REJECT_NAME = re.compile(
    r"\b(Preferred|Pref\.?|Warrant|Warrants|Right|Rights|Unit|Units|Notes?|Debenture|Debentures|Bond|Bonds|ETN|"
    r"Depositary\s+(?:Shares|Receipt)|Subordinated|Trust\s+Preferred|Convertible\s+(?:Preferred|Notes))\b",
    re.IGNORECASE,
)


def download_symbol_files(dest_dir: Path, *, client: httpx.Client | None = None, refresh: bool = False) -> None:
    """Download the Nasdaq Trader symbol-directory file(s) into `dest_dir` (cached unless `refresh`)."""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    own = client is None
    if own:
        client = httpx.Client(headers={"User-Agent": _USER_AGENT}, timeout=60.0, follow_redirects=True)
    try:
        for name in _FILES:
            out = dest_dir / name
            if out.exists() and not refresh:
                continue
            resp = client.get(f"{_BASE}/{name}")
            resp.raise_for_status()
            out.write_text(resp.text, encoding="utf-8")
    finally:
        if own:
            client.close()


def build_universe(symbol_files_dir: Path) -> pd.DataFrame:
    """Parse the Nasdaq Trader file(s) and return the common-stock universe as a DataFrame
    with columns: ticker, name, listing_exchange, in_nyse (bool — True iff listed on NYSE proper)."""
    path = Path(symbol_files_dir) / "nasdaqtraded.txt"
    df = pd.read_csv(path, sep="|", dtype=str, keep_default_na=False)
    # drop the trailer line ("File Creation Time: ...")
    df = df[~df["Symbol"].astype(str).str.startswith("File Creation Time")]
    df.columns = [c.strip() for c in df.columns]
    keep = (
        (df["ETF"].str.strip() == "N")
        & (df["Test Issue"].str.strip() == "N")
        & (df["Listing Exchange"].str.strip().isin(_KEEP_EXCHANGES))
        & (~df["Security Name"].str.contains(_REJECT_NAME.pattern, flags=re.IGNORECASE, na=False))
    )
    u = df[keep].copy()
    out = pd.DataFrame({
        "ticker": u["Symbol"].str.strip(),
        "name": u["Security Name"].str.strip(),
        "listing_exchange": u["Listing Exchange"].str.strip(),
    })
    out["in_nyse"] = out["listing_exchange"] == "N"
    return out.drop_duplicates(subset="ticker").reset_index(drop=True)
