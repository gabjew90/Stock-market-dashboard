"""The ingest ledger — the curated half of `raw/posts.jsonl`, kept in version control.

`posts.jsonl` mixes two very different kinds of data: scraped facts (title, url, date,
word counts) that `ww scrape` reproduces exactly, and curated judgements — the tier,
summary, indicators, tickers, `ingested` flag and `summary_page` that Claude assigns
during Ingest — that nothing reproduces. Losing the second kind means re-reading
thousands of posts to work out what has already been done.

The ledger is that curated slice alone, keyed by post `stem`, written to
`raw/ingest-ledger.jsonl`. Both it and `posts.jsonl` are committed as of 2026-08-12
(the corpus itself is Layer 1 and is now in version control too), but the ledger is
still worth keeping separate: it is small, it diffs readably, and it survives a
re-scrape that rewrites every other field. The round trip is:

    ww ledger export      # after an Ingest batch — posts.jsonl -> ledger (then commit it)
    ww scrape             # on a machine that can reach the blog — rebuilds posts.jsonl
    ww ledger apply       # ledger -> posts.jsonl, restoring ingest state

`ww ledger rebuild` is the recovery path for when the ledger itself is missing: it
reconstructs what it can from `wiki/sources/*.md`, which records one page per ingested
teaching/trade_example post.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

from ww.corpus.index import PostRecord, read_posts_jsonl, write_posts_jsonl

#: Fields carried by the ledger. `stem` is the key; the rest is curated state.
CURATED_FIELDS = ("tier", "summary", "indicators", "tickers", "ingested", "summary_page")


@dataclass
class LedgerEntry:
    stem: str
    tier: str | None = None
    summary: str | None = None
    indicators: list[str] | None = None
    tickers: list[str] | None = None
    ingested: bool = False
    summary_page: str | None = None


def _is_curated(rec: PostRecord | LedgerEntry) -> bool:
    """True if a row carries any state that a re-scrape would not reproduce."""
    return bool(rec.tier or rec.summary or rec.indicators or rec.tickers or rec.ingested or rec.summary_page)


def write_ledger(path: Path, entries: list[LedgerEntry]) -> None:
    """Write entries as JSONL, sorted by stem so diffs stay readable."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for e in sorted(entries, key=lambda x: x.stem):
            fh.write(json.dumps(asdict(e), ensure_ascii=False))
            fh.write("\n")


def read_ledger(path: Path) -> list[LedgerEntry]:
    if not path.exists():
        return []
    known = {f.name for f in fields(LedgerEntry)}
    out: list[LedgerEntry] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            data = {k: v for k, v in json.loads(line).items() if k in known}
            out.append(LedgerEntry(**data))
    return out


def export_from_posts(posts: list[PostRecord]) -> list[LedgerEntry]:
    """Curated rows of a posts.jsonl, as ledger entries. Untouched posts are skipped."""
    return [
        LedgerEntry(stem=p.stem, **{f: getattr(p, f) for f in CURATED_FIELDS})
        for p in posts
        if _is_curated(p)
    ]


def apply_to_posts(entries: list[LedgerEntry], posts: list[PostRecord]) -> tuple[int, list[str], list[str]]:
    """Copy ledger state onto matching posts, in place.

    Returns (applied, unmatched stems, reverted stems).

    Matching is by `stem`. A stem in the ledger with no corresponding post means the
    corpus is older than the ledger (or was scraped with a different slug) — reported
    rather than silently dropped.

    `reverted` lists posts that ALREADY carried curated state differing from the ledger's —
    i.e. work done locally after the last `ww ledger export`. `apply` overwrites it (the
    ledger is the committed record), but the caller must be told, because the usual cause
    is a forgotten export and the fix is to re-export from the local state instead.
    """
    by_stem = {p.stem: p for p in posts}
    applied, unmatched, reverted = 0, [], []
    for e in entries:
        target = by_stem.get(e.stem)
        if target is None:
            unmatched.append(e.stem)
            continue
        if _is_curated(target) and any(getattr(target, f) != getattr(e, f) for f in CURATED_FIELDS):
            reverted.append(e.stem)
        for f in CURATED_FIELDS:
            setattr(target, f, getattr(e, f))
        applied += 1
    return applied, unmatched, reverted


def export_ledger(posts_jsonl: Path, ledger_path: Path) -> int:
    entries = export_from_posts(read_posts_jsonl(posts_jsonl))
    write_ledger(ledger_path, entries)
    return len(entries)


def apply_ledger(ledger_path: Path, posts_jsonl: Path) -> tuple[int, list[str], list[str]]:
    posts = read_posts_jsonl(posts_jsonl)
    if not posts:
        raise FileNotFoundError(f"no corpus at {posts_jsonl} — run `ww scrape` first")
    applied, unmatched, reverted = apply_to_posts(read_ledger(ledger_path), posts)
    write_posts_jsonl(posts_jsonl, posts)
    return applied, unmatched, reverted


_TIER_RE = re.compile(r"·\s*tier:\s*([a-z_]+)")
_H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
#: `- [WW 2018-05-20 — ...](sources/<stem>.md) — <one-line summary>` in wiki/index.md
_INDEX_RE = re.compile(r"^- \[[^\]]+\]\(sources/([^)]+?)\.md\)\s+—\s+(.+?)\s*$", re.MULTILINE)


def _index_summaries(wiki_dir: Path) -> dict[str, str]:
    """Map post stem -> the one-line summary the index catalogues for its summary page."""
    index = wiki_dir / "index.md"
    if not index.exists():
        return {}
    return dict(_INDEX_RE.findall(index.read_text(encoding="utf-8")))


def reconstruct_from_wiki(wiki_dir: Path) -> list[LedgerEntry]:
    """Recover ingest state from `wiki/sources/*.md` when the ledger is also gone.

    Every summary page is, by construction, one ingested `teaching` or `trade_example`
    post (CLAUDE.md §4), and its filename is the post stem. The tier comes from the
    page's `**Source:**` line; the summary prefers the richer one-liner catalogued in
    `wiki/index.md` and falls back to the page's H1. This cannot recover state for posts
    that were tiered but never given a summary page — notably the `daily_update` and
    `meta` rows — so it is a floor, not a full restore.
    """
    summaries = _index_summaries(wiki_dir)
    entries: list[LedgerEntry] = []
    for page in sorted((wiki_dir / "sources").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        tier_match = _TIER_RE.search(text)
        h1 = _H1_RE.search(text)
        entries.append(
            LedgerEntry(
                stem=page.stem,
                tier=tier_match.group(1) if tier_match else "teaching",
                summary=summaries.get(page.stem) or (h1.group(1).strip() if h1 else None),
                ingested=True,
                summary_page=f"wiki/sources/{page.name}",
            )
        )
    return entries
