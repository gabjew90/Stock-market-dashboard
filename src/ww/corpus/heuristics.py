"""Cheap, deterministic pre-classification of posts (refined later by the LLM)."""
from __future__ import annotations

import re

# Word-bounded, case-insensitive markers that strongly indicate a routine
# market-pulse post when they appear in a *short* body.
_DAILY_MARKERS = re.compile(
    r"\b(gmi|t2108|qqq\s+short[- ]term|short[- ]term\s+(?:up|down)[- ]?trend|green\s+line\s+breakout)\b",
    re.IGNORECASE,
)

# Title patterns of his routine market-pulse posts. These are checked on the TITLE because
# 485 posts have an empty body (the title IS the post) and ~1,900 more carry the day count or
# GMI reading only in the title — the body regex alone labelled all of them "unknown", which
# in turn excluded them from `raw/timeline.parquet` (which parses only `daily_update`).
_DAILY_TITLE = re.compile(
    r"\b(?:day\s+\d+\s+of|\d+(?:st|nd|rd|th)\s+day\s+of)\s+\$?qqqq?\b"  # "Day 12 of $QQQ..." / "41st day of QQQQ..."
    r"|\bgmi\s*[:=]\s*\d"                                                  # "GMI: 3;" / "GMI:1" / "GMI=6"
    r"|\b\d+\s+(?:us\s+)?new\s+highs?\b",                                  # "88 US new highs"
    re.IGNORECASE,
)

_SHORT_MAX_WORDS = 250
_LONG_MIN_WORDS = 600


def kind_guess(*, word_count: int, chart_count: int, text: str, title: str = "") -> str:
    """Return one of "daily_update", "long_form", "unknown".

    - Long bodies (>= `_LONG_MIN_WORDS` words) -> "long_form" (a daily-style title does
      not override a genuine essay).
    - Short bodies (<= `_SHORT_MAX_WORDS` words) whose TITLE matches his daily-post
      patterns, or whose body mentions his routine indicators -> "daily_update".
    - Everything else -> "unknown" (the LLM will tier these in Plan 3).
    """
    if word_count >= _LONG_MIN_WORDS:
        return "long_form"
    if word_count <= _SHORT_MAX_WORDS and (
        _DAILY_TITLE.search(title or "") or _DAILY_MARKERS.search(text or "")
    ):
        return "daily_update"
    return "unknown"
