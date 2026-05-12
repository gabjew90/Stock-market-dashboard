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
                    kind_guess=kind_guess(
                        word_count=cleaned.word_count,
                        chart_count=cleaned.chart_count,
                        text=cleaned.markdown,
                    ),
                )
            )

    records.sort(key=lambda r: (r.date, r.post_id))
    write_posts_jsonl(root / "raw" / "posts.jsonl", records)
    return len(records)
