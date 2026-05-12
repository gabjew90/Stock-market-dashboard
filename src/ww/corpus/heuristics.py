"""Cheap, deterministic pre-classification of posts (refined later by the LLM)."""
from __future__ import annotations

import re

# Word-bounded, case-insensitive markers that strongly indicate a routine
# market-pulse post when they appear in a *short* body.
_DAILY_MARKERS = re.compile(
    r"\b(gmi|t2108|qqq\s+short[- ]term|short[- ]term\s+(?:up|down)[- ]?trend|green\s+line\s+breakout)\b",
    re.IGNORECASE,
)

_SHORT_MAX_WORDS = 250
_LONG_MIN_WORDS = 600


def kind_guess(*, word_count: int, chart_count: int, text: str) -> str:
    """Return one of "daily_update", "long_form", "unknown".

    - Long bodies (>= `_LONG_MIN_WORDS` words) -> "long_form".
    - Short bodies (<= `_SHORT_MAX_WORDS` words) that mention his routine
      indicators -> "daily_update".
    - Everything else -> "unknown" (the LLM will tier these in Plan 3).
    """
    if word_count >= _LONG_MIN_WORDS:
        return "long_form"
    if word_count <= _SHORT_MAX_WORDS and _DAILY_MARKERS.search(text or ""):
        return "daily_update"
    return "unknown"
