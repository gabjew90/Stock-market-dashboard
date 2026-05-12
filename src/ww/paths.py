"""Filesystem path helpers for the wiki repo."""
from __future__ import annotations

import re

_UNSAFE = re.compile(r"[^a-z0-9\-]+")
_MAX_STEM_LEN = 120


def post_stem(date: str, slug: str) -> str:
    """Return a filesystem-safe stem `YYYY-MM-DD-<slug>` for a post.

    `date` may be an ISO datetime ("2026-05-10T18:47:42") or a date ("2026-05-10").
    The slug is lowercased, non-`[a-z0-9-]` runs collapsed to a single `-`, and the
    whole stem truncated to `_MAX_STEM_LEN` chars (trailing `-` trimmed).
    """
    day = date[:10]
    clean_slug = _UNSAFE.sub("-", slug.lower()).strip("-") or "post"
    stem = f"{day}-{clean_slug}"
    if len(stem) > _MAX_STEM_LEN:
        stem = stem[:_MAX_STEM_LEN].rstrip("-")
    return stem
