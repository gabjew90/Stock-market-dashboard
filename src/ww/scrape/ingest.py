"""Orchestrate: WordPress API pages -> raw/posts/<stem>.md + raw/posts.jsonl."""
from __future__ import annotations

import html as _html
from pathlib import Path

import httpx
import yaml

from ww.corpus.heuristics import kind_guess
from ww.corpus.index import PostRecord, write_posts_jsonl
from ww.paths import post_stem
from ww.scrape.clean import clean_post_html
from ww.scrape.wp_api import iter_post_pages


def _front_matter(*, url: str, date: str, post_id: int, title: str) -> str:
    fm = yaml.safe_dump(
        {"url": url, "date": date, "post_id": post_id, "title": title},
        sort_keys=False,
        allow_unicode=True,
    )
    return f"---\n{fm}---\n\n"


def scrape_blog(
    base_url: str = "https://wishingwealthblog.com",
    *,
    root: Path,
    client: httpx.Client | None = None,
    delay: float = 1.0,
    force: bool = False,
    max_pages: int | None = None,
) -> int:
    """Scrape every public post into `<root>/raw/posts/` and rebuild `<root>/raw/posts.jsonl`.

    Returns the number of posts processed. Markdown files that already exist are
    left untouched unless `force=True`; the JSONL index is always rebuilt fully
    from the (cached) API responses, so it stays consistent.
    """
    root = Path(root)
    posts_dir = root / "raw" / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = root / "raw" / "api"

    records: list[PostRecord] = []
    seen_ids: set[int] = set()

    for page in iter_post_pages(base_url, cache_dir=cache_dir, client=client, delay=delay, max_pages=max_pages):
        for post in page:
            post_id = int(post["id"])
            if post_id in seen_ids:  # WP can repeat sticky posts across pages
                continue
            seen_ids.add(post_id)

            date = post["date"]
            slug = post["slug"]
            title = _html.unescape(post.get("title", {}).get("rendered", "") or "")
            url = post["link"]
            stem = post_stem(date, slug)

            cleaned = clean_post_html(post.get("content", {}).get("rendered", "") or "")

            md_path = posts_dir / f"{stem}.md"
            if force or not md_path.exists():
                md_path.write_text(
                    _front_matter(url=url, date=date, post_id=post_id, title=title) + cleaned.markdown + "\n",
                    encoding="utf-8",
                )

            records.append(
                PostRecord(
                    post_id=post_id,
                    url=url,
                    date=date,
                    slug=slug,
                    stem=stem,
                    title=title,
                    word_count=cleaned.word_count,
                    chart_count=cleaned.chart_count,
                    chart_image_urls=cleaned.chart_image_urls,
                    categories=list(post.get("categories") or []),
                    tags=list(post.get("tags") or []),
                    modified=post.get("modified"),
                    kind_guess=kind_guess(
                        word_count=cleaned.word_count,
                        chart_count=cleaned.chart_count,
                        text=cleaned.markdown,
                    ),
                )
            )

    records.sort(key=lambda r: (r.date, r.post_id))
    write_posts_jsonl(root / "raw" / "posts.jsonl", records)
    # His own category taxonomy — notably "My Favorite Posts", the primary ingest queue.
    # Non-fatal: a taxonomy fetch failure must not lose a completed post scrape.
    try:
        scrape_categories(base_url, root=root, client=client, delay=delay)
    except Exception as exc:  # pragma: no cover - network-dependent
        print(f"warning: category taxonomy not refreshed ({exc}); raw/categories.json left as-is")
    return len(records)


def scrape_categories(
    base_url: str,
    *,
    root: Path,
    client: httpx.Client | None = None,
    delay: float = 1.0,
) -> int:
    """Write `raw/categories.json`: every non-empty category and the stems of its posts.

    Skips the "All Posts" catch-all and zero-count categories. Stems are built with
    `post_stem` so they join to `raw/posts.jsonl` (an earlier hand-built version did not
    truncate identically and matched only 82/145 favorites).
    """
    import json
    import time

    root = Path(root)
    own = client is None
    if own:
        client = httpx.Client(base_url=base_url, headers={"User-Agent": "wishing-wealth-wiki/0.1"}, timeout=30.0, follow_redirects=True)
    try:
        cats = client.get("/wp-json/wp/v2/categories", params={"per_page": 100}).json()
        out: dict = {
            "_note": "Dr. Wish's own WordPress category taxonomy, written by `ww scrape`. "
                     "'My Favorite Posts' is his curation of what matters most — the primary ingest queue.",
            "categories": {},
        }
        for cat in sorted(cats, key=lambda c: -int(c.get("count", 0))):
            if not cat.get("count") or cat.get("name") == "All Posts":
                continue
            members = []
            page = 1
            while True:
                resp = client.get(
                    "/wp-json/wp/v2/posts",
                    params={"categories": cat["id"], "per_page": 100, "page": page, "_fields": "date,slug,title"},
                )
                if resp.status_code != 200:
                    break
                body = resp.json()
                if not body:
                    break
                members += [
                    {"stem": post_stem(x["date"], x["slug"]), "date": x["date"][:10],
                     "title": _html.unescape((x.get("title") or {}).get("rendered", ""))}
                    for x in body
                ]
                if len(body) < 100:
                    break
                page += 1
                if delay:
                    time.sleep(delay)
            out["categories"][cat["name"]] = {"id": cat["id"], "count": cat["count"], "posts": members}
        (root / "raw" / "categories.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        return len(out["categories"])
    finally:
        if own:
            client.close()
