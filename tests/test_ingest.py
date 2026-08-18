import json
from pathlib import Path

import httpx

from ww.scrape.ingest import scrape_blog


def _mock_client(fixtures_dir: Path) -> httpx.Client:
    page1 = json.loads((fixtures_dir / "wp_api_page1.json").read_text())

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if page == 1:
            return httpx.Response(200, json=page1, headers={"X-WP-TotalPages": "1"})
        return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})

    return httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")


def test_scrape_writes_markdown_files_with_frontmatter(fixtures_dir, tmp_path):
    n = scrape_blog("https://example.test", root=tmp_path, client=_mock_client(fixtures_dir), delay=0.0)
    assert n == 2
    md_files = sorted((tmp_path / "raw" / "posts").glob("*.md"))
    assert [p.name for p in md_files] == [
        "2005-04-17-april-17-2005-short-or-in-cash.md",
        "2026-05-10-day-22-of-qqq-short-term-up-trend.md",
    ]
    body = (tmp_path / "raw" / "posts" / "2026-05-10-day-22-of-qqq-short-term-up-trend.md").read_text(encoding="utf-8")
    assert body.startswith("---\n")
    assert "post_id: 49378" in body
    assert "url: https://wishingwealthblog.com/2026/05/day-22-of-qqq-short-term-up-trend/" in body
    assert "The 10 week average is back above its 30 week average." in body


def test_scrape_writes_jsonl_index(fixtures_dir, tmp_path):
    scrape_blog("https://example.test", root=tmp_path, client=_mock_client(fixtures_dir), delay=0.0)
    lines = (tmp_path / "raw" / "posts.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    by_id = {json.loads(l)["post_id"]: json.loads(l) for l in lines}
    assert by_id[49378]["kind_guess"] == "daily_update"     # short + mentions GMI
    assert by_id[832]["kind_guess"] == "long_form"          # padded fixture body
    assert by_id[49378]["ingested"] is False
    assert by_id[49378]["tier"] is None
    assert by_id[49378]["stem"] == "2026-05-10-day-22-of-qqq-short-term-up-trend"


def test_scrape_is_idempotent_and_skips_existing(fixtures_dir, tmp_path):
    scrape_blog("https://example.test", root=tmp_path, client=_mock_client(fixtures_dir), delay=0.0)
    md = tmp_path / "raw" / "posts" / "2026-05-10-day-22-of-qqq-short-term-up-trend.md"
    md.write_text(md.read_text(encoding="utf-8") + "\nHAND EDIT\n", encoding="utf-8")
    # Second run without --force: existing file untouched, jsonl still rebuilt with 2 rows.
    scrape_blog("https://example.test", root=tmp_path, client=_mock_client(fixtures_dir), delay=0.0)
    assert "HAND EDIT" in md.read_text(encoding="utf-8")
    assert len((tmp_path / "raw" / "posts.jsonl").read_text(encoding="utf-8").splitlines()) == 2


def test_scrape_force_rewrites(fixtures_dir, tmp_path):
    scrape_blog("https://example.test", root=tmp_path, client=_mock_client(fixtures_dir), delay=0.0)
    md = tmp_path / "raw" / "posts" / "2026-05-10-day-22-of-qqq-short-term-up-trend.md"
    md.write_text("STALE", encoding="utf-8")
    scrape_blog("https://example.test", root=tmp_path, client=_mock_client(fixtures_dir), delay=0.0, force=True)
    assert "The 10 week average is back above its 30 week average." in md.read_text(encoding="utf-8")


def test_scrape_captures_categories_tags_and_modified(fixtures_dir, tmp_path):
    """His own WordPress taxonomy is curation we cannot reconstruct — notably the
    'My Favorite Posts' category. It must survive the scrape onto PostRecord."""
    from ww.corpus.index import read_posts_jsonl

    scrape_blog("https://example.test", root=tmp_path, client=_mock_client(fixtures_dir), delay=0.0)
    by_slug = {r.slug: r for r in read_posts_jsonl(tmp_path / "raw" / "posts.jsonl")}

    tagged = by_slug["day-22-of-qqq-short-term-up-trend"]
    assert tagged.categories == [1, 42]
    assert tagged.tags == [7]
    assert tagged.modified == "2026-05-11T09:00:00"

    # A post the API returns without those keys must not blow up, and must default empty.
    bare = by_slug["april-17-2005-short-or-in-cash"]
    assert bare.categories == []
    assert bare.tags == []
    assert bare.modified is None


def test_default_fields_request_the_taxonomy(fixtures_dir, tmp_path):
    """Guard the field list itself: dropping 'categories' silently loses his curation."""
    from ww.scrape.wp_api import _DEFAULT_FIELDS

    for wanted in ("categories", "tags", "modified"):
        assert wanted in _DEFAULT_FIELDS


def test_rescrape_picks_up_a_newly_published_post(fixtures_dir, tmp_path):
    """Posts are fetched newest-first, so a NEW post lands on page 1. If page 1 is served
    from the disk cache forever, `ww scrape` can never surface it — which silently breaks
    the documented 'ww scrape to pull new posts' workflow."""
    import json as _json
    from ww.corpus.index import read_posts_jsonl

    page1 = _json.loads((fixtures_dir / "wp_api_page1.json").read_text())
    state = {"posts": list(page1)}

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if page == 1:
            return httpx.Response(200, json=state["posts"], headers={"X-WP-TotalPages": "1"})
        return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")
    scrape_blog("https://example.test", root=tmp_path, client=client, delay=0.0)
    assert len(read_posts_jsonl(tmp_path / "raw" / "posts.jsonl")) == 2

    # A new post is published.
    state["posts"] = [{
        "id": 99999, "date": "2026-08-13T10:00:00", "slug": "brand-new-post",
        "link": "https://example.test/2026/08/brand-new-post/",
        "title": {"rendered": "Brand new"}, "content": {"rendered": "<p>New content.</p>"},
    }] + list(page1)

    scrape_blog("https://example.test", root=tmp_path, client=client, delay=0.0)
    stems = {r.stem for r in read_posts_jsonl(tmp_path / "raw" / "posts.jsonl")}
    assert "2026-08-13-brand-new-post" in stems


def test_scrape_writes_categories_json_from_the_taxonomy_endpoint(fixtures_dir, tmp_path):
    """CLAUDE.md says `ww scrape` captures his category taxonomy to raw/categories.json,
    and `ww batch --category` depends on that file. Nothing in src/ wrote it until now."""
    import json as _json
    from ww.scrape.ingest import scrape_blog

    page1 = _json.loads((fixtures_dir / "wp_api_page1.json").read_text())

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        page = int(request.url.params.get("page", "1"))
        if path.endswith("/categories"):
            return httpx.Response(200, json=[
                {"id": 1, "name": "All Posts", "count": 2},
                {"id": 42, "name": "My Favorite Posts", "count": 1},
                {"id": 7, "name": "Empty", "count": 0},
            ])
        if path.endswith("/posts"):
            cats = request.url.params.get("categories")
            if cats == "42":
                return httpx.Response(200, json=page1[:1]) if page == 1 else httpx.Response(400, json={"code": "rest_post_invalid_page_number"})
            return httpx.Response(200, json=page1) if page == 1 else httpx.Response(400, json={"code": "rest_post_invalid_page_number"})
        return httpx.Response(404)

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")
    scrape_blog("https://example.test", root=tmp_path, client=client, delay=0.0)

    cats = _json.loads((tmp_path / "raw" / "categories.json").read_text(encoding="utf-8"))["categories"]
    assert "My Favorite Posts" in cats and cats["My Favorite Posts"]["id"] == 42
    assert "Empty" not in cats                       # zero-count categories dropped
    assert "All Posts" not in cats                   # the catch-all is noise
    stems = [m["stem"] for m in cats["My Favorite Posts"]["posts"]]
    assert stems == ["2026-05-10-day-22-of-qqq-short-term-up-trend"]
