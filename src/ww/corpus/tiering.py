"""Bulk tiering: decide which un-ingested posts are routine daily notes.

Two triage seams were worked by hand across 2026-08-18 (see `wiki/log.md`): filtering
post *titles* for teaching hooks, then scanning post *bodies* for first-person rule
statements. The body scan found teaching in posts whose titles gave no sign of it, so it
is the more reliable of the two and is codified here.

`screen()` is deliberately conservative: it only proposes `daily_update` for posts that
show **no** teaching marker and are **short**. Anything else is *held* — left untiered and
un-ingested — so the remaining queue stays a real, small, prioritised list rather than
being swept flat. A held post is not a classification; it is "a human or an LLM should
read this one".
"""
from __future__ import annotations

import re
from dataclasses import dataclass

#: First-person phrases Dr. Wish uses when he is stating a rule rather than reporting a
#: reading. Derived from the posts that the hand triage confirmed carried teaching.
_TEACHING_MARKERS = re.compile(
    r"(I have (?:learned|found|discovered)"
    r"|my rule is"
    r"|the key (?:to|is)"
    r"|I never |I always "
    r"|one must "
    r"|the lesson"
    r"|I define |I compute"
    r"|criteria (?:are|for)"
    r"|formula"
    r"|I created a (?:new )?(?:scan|column)"
    r"|I changed|I have revised"
    r"|note that I"
    r"|teaches us"
    r"|the reason I"
    r"|I look for|I want to see|I prefer"
    r"|my strategy"
    r"|I use the|I place my"
    r"|remember,)",
    re.IGNORECASE,
)

#: Above this word count a post is held for reading even with no marker — length
#: correlates with teaching, and the cost of reading one extra post is far lower than
#: the cost of burying a rule.
_HOLD_MIN_WORDS = 400


def teaching_markers(text: str) -> set[str]:
    """The distinct teaching-marker phrases present in `text`, lower-cased."""
    return {m.group(0).lower() for m in _TEACHING_MARKERS.finditer(text or "")}


@dataclass(frozen=True)
class Screen:
    """The outcome of screening one post.

    `hold` and `tier` are mutually exclusive: a held post gets no tier, because "not yet
    read" is not a classification.
    """

    tier: str | None
    hold: bool
    reason: str


def screen(*, kind_guess: str, word_count: int, text: str, title: str = "") -> Screen:
    """Propose a tier for an un-ingested post, or hold it for reading.

    `long_form` posts are never bulk-tiered: they are the curated ingest queue.
    """
    if kind_guess == "long_form":
        return Screen(None, True, "long_form is the curated ingest queue — read it")

    markers = teaching_markers(text)
    if markers:
        n = len(markers)
        return Screen(None, True, f"holds {n} teaching marker{'s' if n != 1 else ''}: "
                                  + ", ".join(sorted(markers)[:3]))

    if word_count >= _HOLD_MIN_WORDS:
        return Screen(None, True, f"long body ({word_count} words) — read before dismissing")

    return Screen("daily_update", False, f"no teaching marker, {word_count} words — routine market note")
