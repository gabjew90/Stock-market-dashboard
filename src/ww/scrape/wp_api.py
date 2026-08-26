"""Page through the WordPress REST API for blog posts, caching each page to disk."""
from __future__ import annotations

import json
import time
from collections.abc import Iterator
from pathlib import Path

import httpx

#: Fields requested from the API. `categories`/`tags` carry Dr. Wish's own taxonomy —
#: notably "My Favorite Posts", his curation of what matters most, which no heuristic
#: reproduces. `modified` distinguishes a post he later revised from one he did not.
_DEFAULT_FIELDS = "id,date,modified,slug,link,title,content,categories,tags"
_PER_PAGE = 100
_USER_AGENT = "wishing-wealth-wiki/0.1 (personal research project)"


def _cache_path(cache_dir: Path, page: int) -> Path:
    return cache_dir / f"page-{page:04d}.json"


def iter_post_pages(
    base_url: str,
    *,
    cache_dir: Path,
    client: httpx.Client | None = None,
    per_page: int = _PER_PAGE,
    fields: str = _DEFAULT_FIELDS,
    delay: float = 1.0,
    max_pages: int | None = None,
) -> Iterator[list[dict]]:
    """Yield successive pages (lists of post dicts) from `<base_url>/wp-json/wp/v2/posts`.

    Posts are paginated **oldest-first** (`order=asc`), which is what makes the page
    cache sound: a newly published post appends to the end, so every earlier post keeps
    its offset and pages 1..N-1 are immutable. Under the newest-first ordering this used
    until 2026-08-26, publishing K new posts shifted every offset by K, so the K posts
    that crossed a cached page boundary became invisible - six were lost that way, still
    live on the blog but absent from `raw/posts.jsonl`. `comments.py` had it right.

    Each fetched page is written to `<cache_dir>/page-NNNN.json`; if that file
    already exists it is read from disk and no HTTP request is made. Only FULL pages are
    cached - the final short page is where new posts land. Pagination stops on an empty
    page, a 400 `rest_post_invalid_page_number`, or `max_pages`.
    `delay` seconds are slept between *network* requests (not cache hits).
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    own_client = client is None
    if own_client:
        client = httpx.Client(
            base_url=base_url,
            headers={"User-Agent": _USER_AGENT},
            timeout=30.0,
            follow_redirects=True,
        )
    try:
        page = 1
        while max_pages is None or page <= max_pages:
            cp = _cache_path(cache_dir, page)
            if cp.exists():
                posts = json.loads(cp.read_text(encoding="utf-8"))
            else:
                resp = client.get(
                    "/wp-json/wp/v2/posts",
                    params={"per_page": per_page, "page": page, "_fields": fields, "orderby": "date", "order": "asc"},
                )
                if resp.status_code == 400:
                    try:
                        body = resp.json()
                    except Exception:
                        body = {}
                    if body.get("code") == "rest_post_invalid_page_number":
                        break
                    resp.raise_for_status()
                resp.raise_for_status()
                posts = resp.json()
                # Cache FULL pages only. The final short page is where new posts land; caching
                # it would hide them until the total crossed the next per_page boundary.
                if len(posts) >= per_page:
                    cp.write_text(json.dumps(posts, ensure_ascii=False), encoding="utf-8")
                if delay:
                    time.sleep(delay)
            if not posts:
                break
            yield posts
            page += 1
    finally:
        if own_client:
            client.close()
