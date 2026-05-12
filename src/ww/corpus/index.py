"""The raw-sources index: one `PostRecord` per blog post, persisted as JSONL."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path


@dataclass
class PostRecord:
    post_id: int
    url: str
    date: str                       # ISO datetime as returned by the WP API
    slug: str
    stem: str                       # filename stem under raw/posts/ (no extension)
    title: str
    word_count: int
    chart_count: int
    chart_image_urls: list[str] = field(default_factory=list)
    kind_guess: str = "unknown"     # daily_update | long_form | unknown  (heuristic, Plan 1)
    tier: str | None = None         # teaching | trade_example | daily_update | meta  (Plan 3, Claude)
    summary: str | None = None      # one-line summary  (Plan 3, Claude)
    indicators: list[str] | None = None   # entities referenced  (Plan 3, Claude)
    tickers: list[str] | None = None      # tickers referenced  (Plan 3, Claude)
    ingested: bool = False          # processed into the wiki yet?  (Plan 3)
    summary_page: str | None = None # path under wiki/sources/ if a summary page was written


def write_posts_jsonl(path: Path, records: list[PostRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(asdict(rec), ensure_ascii=False))
            fh.write("\n")


def read_posts_jsonl(path: Path) -> list[PostRecord]:
    if not path.exists():
        return []
    known = {f.name for f in fields(PostRecord)}
    out: list[PostRecord] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            data = {k: v for k, v in json.loads(line).items() if k in known}
            out.append(PostRecord(**data))
    return out


def update_records(path: Path, updates: dict[int, dict]) -> None:
    """Patch existing rows in a posts.jsonl file, in place, preserving row order.

    `updates` maps `post_id` -> dict of field names to new values. Every key in
    `updates` must match an existing row's `post_id` (else `KeyError`), and every
    field name must be a real `PostRecord` field (else `ValueError`).
    """
    known = {f.name for f in fields(PostRecord)}
    records = read_posts_jsonl(path)
    by_id = {r.post_id: r for r in records}
    for pid, patch in updates.items():
        if pid not in by_id:
            raise KeyError(f"post_id {pid} not found in {path}")
        bad = set(patch) - known
        if bad:
            raise ValueError(f"unknown PostRecord field(s) for post_id {pid}: {sorted(bad)}")
        for k, v in patch.items():
            setattr(by_id[pid], k, v)
    write_posts_jsonl(path, records)
