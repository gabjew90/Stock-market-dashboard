"""Parse Dr. Wish's daily market-pulse posts into a structured time series.

This is a conservative pre-pass: a field stays None unless it was confidently
extracted, and a row is flagged (`parse_confidence == "flagged"`) when neither the
GMI value nor the QQQ short-term-trend day count could be read. See spec §6.2.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from ww.corpus.index import read_posts_jsonl

# --- regexes -------------------------------------------------------------------
# GMI value (the 0-6 composite). Must NOT match "GMI-2"/"GMI2"/"GMI-S"/"GMI-R".
# The negative lookahead (?![-–]?[2SR]) prevents "GMI-S", "GMI-2", "GMI2", "GMI-R".
_GMI_VALUE = re.compile(
    r"\bGMI\b(?![-–]?\s*[2SR]\b)(?![-–][2SR])"
    r"[^.\d\n]{0,80}?\+?\s*([0-6])\b",
    re.IGNORECASE,
)
# "N (of 6)" — standard phrasing
_GMI_OF6 = re.compile(r"\b([0-6])\s*\(\s*of\s*6\s*\)", re.IGNORECASE)
# "N our of 6" / "N out of 6" / "N of 6" — looser phrasing (typos in real posts)
_GMI_XOFX = re.compile(r"\b([0-6])\s+(?:our?\s+of|out\s+of|of)\s+6\b", re.IGNORECASE)
_GMI2_VALUE = re.compile(r"\bGMI[-–]?2\b[^.\d\n]{0,30}?\+?\s*([0-9]|10)\b", re.IGNORECASE)
_GMI_S = re.compile(r"\bGMI[-–]?S\b[^.\d\n]{0,30}?\+?\s*(\d{1,3})\b", re.IGNORECASE)
_GMI_STATE = re.compile(r"\bGMI\b[^.\n]{0,80}?\b(Green|Red|Buy|Sell)\b", re.IGNORECASE)

# QQQ short-term-trend day count.
# Pattern 1: "Day 13 of $QQQ short term up-trend" / "3rd day of $QQQ short term down-trend"
_QQQ_DAY = re.compile(
    r"(?:Day\s+|(?:\d{1,3})\s*(?:st|nd|rd|th)\s+day\s+of\s+)"
    r"(?:the\s+|a\s+|its\s+|new\s+){0,3}"
    r"\$?QQQ+\s*(?:short[- ]term\s+)?(up|down)[- ]?trend",
    re.IGNORECASE,
)
# We need to also handle the plain "Day N of $QQQ ..." and ordinal forms separately
_QQQ_DAY_PLAIN = re.compile(
    r"(?:Day\s+(\d{1,3})\s+of\s+(?:the\s+|a\s+|its\s+)?|\b(\d{1,3})\s*(?:st|nd|rd|th)\s+day\s+of\s+(?:the\s+|a\s+|its\s+|new\s+)?\$?)"
    r"\$?QQQ+\s*(?:short[- ]term\s+)?(up|down)[- ]?trend",
    re.IGNORECASE,
)
# Pattern 2: "QQQQ is in the 26th day of its short term up-trend"
_QQQ_DAY_ALT = re.compile(
    r"\$?QQQ+[^.\n]{0,30}?\b(\d{1,3})\s*(?:st|nd|rd|th)\s+day[^.\n]{0,30}?(up|down)[- ]?trend",
    re.IGNORECASE,
)
# Pattern 3: "81st day of QQQQ up-trend" (no "short term" prefix, bare "of QQQQ")
_QQQ_DAY_BARE = re.compile(
    r"\b(\d{1,3})\s*(?:st|nd|rd|th)\s+day\s+of\s+\$?QQQ+\s+(up|down)[- ]?trend",
    re.IGNORECASE,
)
_T2108 = re.compile(r"T2108[^.\n%]{0,45}?(\d{1,3})\s*%", re.IGNORECASE)
_T2108_EQ = re.compile(r"T2108\s*=\s*(\d{1,3})\s*%", re.IGNORECASE)
_T2108_REV = re.compile(r"(\d{1,3})\s*%[^.\n]{0,25}?T2108", re.IGNORECASE)

_STANCE_CASH = re.compile(
    r"\bin\s+(?:puts\s+or\s+)?cash\b|\bin\s+cash\s+(?:or|and)\b|\b(?:all|mostly)\s+in\s+cash\b",
    re.IGNORECASE,
)
_STANCE_CAUTIOUS = re.compile(
    r"\bdefensive\b|\braise\s+(?:my\s+)?stops\b|\btighten\s+stops\b|\bcautious\b"
    r"|\breduc\w*\s+(?:my\s+)?exposure\b",
    re.IGNORECASE,
)
_STANCE_INVESTED = re.compile(
    r"\baccumulat\w*\b|\bbuying\b|\breenter\b|\bre-enter\b|\bwade\s+back\s+in\b"
    r"|\bstay\s+the\s+course\b|\bloading\s+up\b|\bready\s+to\s+reenter\b|\bback\s+in\b",
    re.IGNORECASE,
)


@dataclass
class DailyRow:
    gmi_value: int | None = None       # 0-6
    gmi_state: str | None = None       # Green / Red / Buy / Sell
    gmi2_value: int | None = None      # 0-8 (GMI2 / "GMI-2")
    gmi_s: int | None = None           # 0-100 (GMI-S strength index)
    qqq_day: int | None = None         # "Day N of the QQQ short-term trend"
    qqq_dir: str | None = None         # "up" / "down"
    t2108: int | None = None           # percent
    stance: str | None = None          # cash / cautious / invested
    parse_confidence: str = "flagged"  # "high" if gmi_value or qqq_day found, else "flagged"


def _first_int(pat: re.Pattern, text: str, lo: int | None = None, hi: int | None = None) -> int | None:
    for m in pat.finditer(text):
        v = int(m.group(1))
        if (lo is None or v >= lo) and (hi is None or v <= hi):
            return v
    return None


def _extract_qqq(text: str) -> tuple[int | None, str | None]:
    """Extract QQQ day count and direction from various phrasings."""
    # Try: "Day 13 of $QQQ short term up-trend"
    m = re.search(
        r"\bDay\s+(\d{1,3})\s+of\s+(?:the\s+|a\s+|its\s+)?\$?QQQ+\s*(?:short[- ]term\s+)?(up|down)[- ]?trend",
        text, re.IGNORECASE,
    )
    if m:
        return int(m.group(1)), m.group(2).lower()

    # Try: "3rd day of $QQQ short term down-trend"
    m = re.search(
        r"\b(\d{1,3})\s*(?:st|nd|rd|th)\s+day\s+of\s+(?:the\s+|a\s+|its\s+|new\s+)?\$?QQQ+\s*(?:short[- ]term\s+)?(up|down)[- ]?trend",
        text, re.IGNORECASE,
    )
    if m:
        return int(m.group(1)), m.group(2).lower()

    # Try: "QQQQ is in the 26th day of its short term up-trend"
    m = re.search(
        r"\$?QQQ+[^.\n]{0,30}?\b(\d{1,3})\s*(?:st|nd|rd|th)\s+day[^.\n]{0,30}?(up|down)[- ]?trend",
        text, re.IGNORECASE,
    )
    if m:
        return int(m.group(1)), m.group(2).lower()

    # Try: "81st day of QQQQ up-trend" (bare, no "short term")
    m = re.search(
        r"\b(\d{1,3})\s*(?:st|nd|rd|th)\s+day\s+of\s+\$?QQQ+\s+(up|down)[- ]?trend",
        text, re.IGNORECASE,
    )
    if m:
        return int(m.group(1)), m.group(2).lower()

    return None, None


def parse_daily_update(text: str) -> DailyRow:
    t = text or ""
    row = DailyRow()

    # GMI value — prefer an explicit "N (of 6)" if present, else loose "N of 6",
    # else the GMI-context match.
    of6 = _first_int(_GMI_OF6, t, 0, 6)
    xofx = _first_int(_GMI_XOFX, t, 0, 6)
    gmi_ctx = _first_int(_GMI_VALUE, t, 0, 6)
    row.gmi_value = of6 if of6 is not None else (xofx if xofx is not None else gmi_ctx)

    row.gmi2_value = _first_int(_GMI2_VALUE, t, 0, 10)
    row.gmi_s = _first_int(_GMI_S, t, 0, 100)

    m = _GMI_STATE.search(t)
    if m:
        row.gmi_state = m.group(1).title()

    # QQQ short-term-trend day count
    row.qqq_day, row.qqq_dir = _extract_qqq(t)

    # T2108 — try "T2108 = N%" first (exact), then forward scan, then reverse scan
    t2108_eq = _first_int(_T2108_EQ, t, 0, 100)
    t2108_fwd = _first_int(_T2108, t, 0, 100)
    t2108_rev = _first_int(_T2108_REV, t, 0, 100)
    row.t2108 = t2108_eq if t2108_eq is not None else (t2108_fwd if t2108_fwd is not None else t2108_rev)

    # stance — cash > cautious > invested (most defensive wins on ties)
    if _STANCE_CASH.search(t):
        row.stance = "cash"
    elif _STANCE_CAUTIOUS.search(t):
        row.stance = "cautious"
    elif _STANCE_INVESTED.search(t):
        row.stance = "invested"

    row.parse_confidence = "high" if (row.gmi_value is not None or row.qqq_day is not None) else "flagged"
    return row


def _post_body(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    # strip leading YAML front-matter
    return re.sub(r"^---\n.*?\n---\n", "", raw, count=1, flags=re.DOTALL).strip()


def build_timeline(root: Path) -> pd.DataFrame:
    """Parse every `daily_update` post under `<root>/raw/` into a DataFrame, one row per date, ascending."""
    root = Path(root)
    records = read_posts_jsonl(root / "raw" / "posts.jsonl")
    rows = []
    for r in records:
        if not (r.kind_guess == "daily_update" or r.tier == "daily_update"):
            continue
        body = _post_body(root / "raw" / "posts" / f"{r.stem}.md")
        d = parse_daily_update(body)
        rows.append({"date": pd.Timestamp(r.date), "source_url": r.url, "stem": r.stem, **asdict(d)})
    if not rows:
        return pd.DataFrame(columns=["date", "source_url", "stem", *DailyRow().__dataclass_fields__.keys()])
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
