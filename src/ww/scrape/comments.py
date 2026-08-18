"""Fetch the blog's reader comments — primary material absent from the post bodies.

Post text is Dr. Wish explaining his method to a general audience. The comment threads
are where a specific reader pins him down ("does an intraday dip below the green line
count?") and he answers in one line. Those clarifications exist nowhere else, and the
scraper ignored them until 2026-08-12.

    ww comments            # -> raw/comments.jsonl (+ page cache under raw/api-comments/)

Threading is preserved via `parent`, so a question and its reply can be reassembled.
"""
from __future__ import annotations

import html as _html
import json
import re
import time
from dataclasses import asdict, dataclass, fields
from pathlib import Path

import httpx

_PER_PAGE = 100
_USER_AGENT = "wishing-wealth-wiki/0.1 (personal research project)"
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


@dataclass
class CommentRecord:
    comment_id: int
    post_id: int
    date: str
    author: str
    parent: int          # 0 for a top-level comment, else the comment_id being replied to
    text: str            # HTML stripped, entities decoded
    url: str = ""


def _plain(rendered: str) -> str:
    """Rendered comment HTML -> searchable plain text."""
    text = _TAG.sub(" ", rendered or "")
    return _WS.sub(" ", _html.unescape(text)).strip()


def _cache_path(cache_dir: Path, page: int) -> Path:
    return cache_dir / f"page-{page:04d}.json"


def iter_comment_pages(
    base_url: str,
    *,
    cache_dir: Path,
    client: httpx.Client | None = None,
    per_page: int = _PER_PAGE,
    delay: float = 1.0,
    max_pages: int | None = None,
):
    """Yield pages from `<base_url>/wp-json/wp/v2/comments`, caching each to disk.

    Mirrors `wp_api.iter_post_pages`: cached pages cost no request, pagination stops on an
    empty page, a 400 invalid-page-number, or `max_pages`.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    own = client is None
    if own:
        client = httpx.Client(
            base_url=base_url, headers={"User-Agent": _USER_AGENT}, timeout=30.0, follow_redirects=True
        )
    try:
        page = 1
        while max_pages is None or page <= max_pages:
            cp = _cache_path(cache_dir, page)
            if cp.exists():
                body = json.loads(cp.read_text(encoding="utf-8"))
            else:
                resp = client.get(
                    "/wp-json/wp/v2/comments",
                    params={"per_page": per_page, "page": page, "orderby": "date", "order": "asc"},
                )
                if resp.status_code == 400:
                    # Only "past the last page" is a legitimate end. Anything else (a bad
                    # per_page, a WAF block, a renamed param) is an error — treating it as
                    # the end would return zero rows and let the caller clobber good data.
                    try:
                        code = resp.json().get("code")
                    except Exception:
                        code = None
                    if code == "rest_comment_invalid_page_number":
                        break
                    resp.raise_for_status()
                resp.raise_for_status()
                body = resp.json()
                if not body:
                    break
                # Cache only FULL pages. The final short page is where new comments land;
                # if we cached it, `ww comments` would never see them until the total
                # crossed the next per_page boundary.
                if len(body) >= per_page:
                    cp.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
                if delay:
                    time.sleep(delay)
            if not body:
                break
            yield body
            page += 1
    finally:
        if own:
            client.close()


def write_comments_jsonl(path: Path, records: list[CommentRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(asdict(rec), ensure_ascii=False))
            fh.write("\n")


def read_comments_jsonl(path: Path) -> list[CommentRecord]:
    if not path.exists():
        return []
    known = {f.name for f in fields(CommentRecord)}
    out: list[CommentRecord] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            out.append(CommentRecord(**{k: v for k, v in json.loads(line).items() if k in known}))
    return out


def scrape_comments(
    base_url: str,
    *,
    root: Path,
    client: httpx.Client | None = None,
    delay: float = 1.0,
    max_pages: int | None = None,
    force: bool = False,
) -> int:
    """Pull every comment into `<root>/raw/comments.jsonl`. Returns the count fetched.

    Refuses to overwrite an existing, LARGER file unless `force=True` — a partial or
    truncated fetch must never silently shrink the committed corpus.
    """
    root = Path(root)
    records: list[CommentRecord] = []
    for page in iter_comment_pages(
        base_url, cache_dir=root / "raw" / "api-comments", client=client, delay=delay, max_pages=max_pages
    ):
        for c in page:
            records.append(
                CommentRecord(
                    comment_id=c["id"],
                    post_id=c.get("post", 0),
                    date=c.get("date", ""),
                    author=_html.unescape(c.get("author_name") or ""),
                    parent=c.get("parent", 0) or 0,
                    text=_plain((c.get("content") or {}).get("rendered", "")),
                    url=c.get("link", "") or "",
                )
            )
    records.sort(key=lambda r: (r.date, r.comment_id))
    out = root / "raw" / "comments.jsonl"
    existing = len(read_comments_jsonl(out))
    if existing > len(records) and not force:
        # Do not clobber. The caller decides whether the shrink is real (force=True).
        return len(records)
    write_comments_jsonl(out, records)
    return len(records)
