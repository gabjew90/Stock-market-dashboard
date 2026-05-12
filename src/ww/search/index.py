"""Build, persist, and query a BM25 search index over wiki/** + raw/posts/**."""
from __future__ import annotations

import pickle
import re
from dataclasses import dataclass
from pathlib import Path

from ww.corpus.index import read_posts_jsonl
from ww.search.bm25 import BM25
from ww.search.chunk import Chunk, chunk_markdown, tokenize

# wiki files that are NOT searchable "pages"
_WIKI_SKIP_NAMES = {"log.md"}
_WIKI_SKIP_DIRS = {"_templates"}


@dataclass
class SearchHit:
    source: str        # "wiki:<rel>" or "post:<stem>"
    heading: str
    text: str
    score: float
    citation: str      # human/paste-friendly: a wiki path+heading, or a post date + URL


class SearchIndex:
    def __init__(self, chunks: list[Chunk], *, post_meta: dict[str, tuple[str, str]]) -> None:
        # post_meta: stem -> (iso_date, url)
        self.chunks = chunks
        self.post_meta = post_meta
        self._bm25 = BM25([tokenize(c.heading + " " + c.text) for c in chunks])

    # --- citations -------------------------------------------------------------
    def _citation(self, c: Chunk) -> str:
        if c.source.startswith("wiki:"):
            return f"{c.source[len('wiki:'):]} — {c.heading}"
        stem = c.source[len("post:"):]
        date, url = self.post_meta.get(stem, ("", ""))
        return f"WW {date[:10]} — {stem} ({url})".strip()

    # --- query -----------------------------------------------------------------
    def search(self, query: str, *, top_k: int = 8, source: str | None = None, since: int | None = None) -> list[SearchHit]:
        ranked = self._bm25.query(tokenize(query), top_k=max(top_k * 4, top_k))
        hits: list[SearchHit] = []
        for idx, score in ranked:
            if score <= 0:
                continue
            c = self.chunks[idx]
            if source == "wiki" and not c.source.startswith("wiki:"):
                continue
            if source == "posts" and not c.source.startswith("post:"):
                continue
            if since is not None and c.source.startswith("post:"):
                stem = c.source[len("post:"):]
                year = int(stem[:4]) if stem[:4].isdigit() else 0
                if year < since:
                    continue
            hits.append(SearchHit(source=c.source, heading=c.heading, text=c.text, score=score, citation=self._citation(c)))
            if len(hits) >= top_k:
                break
        return hits

    # --- persistence -----------------------------------------------------------
    def save(self, path: Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as fh:
            pickle.dump({"chunks": self.chunks, "post_meta": self.post_meta}, fh)

    @classmethod
    def load(cls, path: Path) -> SearchIndex:
        with Path(path).open("rb") as fh:
            d = pickle.load(fh)
        return cls(d["chunks"], post_meta=d["post_meta"])


def _iter_wiki_files(wiki_dir: Path):
    for p in sorted(wiki_dir.rglob("*.md")):
        rel = p.relative_to(wiki_dir)
        if rel.parts[0] in _WIKI_SKIP_DIRS:
            continue
        if p.name in _WIKI_SKIP_NAMES and len(rel.parts) == 1:
            continue
        yield p, rel.as_posix()


def build_index(root: Path) -> SearchIndex:
    root = Path(root)
    chunks: list[Chunk] = []
    wiki_dir = root / "wiki"
    if wiki_dir.is_dir():
        for path, rel in _iter_wiki_files(wiki_dir):
            chunks.extend(chunk_markdown(path.read_text(encoding="utf-8"), source=f"wiki:{rel}"))
    post_meta: dict[str, tuple[str, str]] = {}
    for r in read_posts_jsonl(root / "raw" / "posts.jsonl"):
        post_meta[r.stem] = (r.date, r.url)
        mdp = root / "raw" / "posts" / f"{r.stem}.md"
        if mdp.exists():
            chunks.extend(chunk_markdown(mdp.read_text(encoding="utf-8"), source=f"post:{r.stem}"))
    return SearchIndex(chunks, post_meta=post_meta)
