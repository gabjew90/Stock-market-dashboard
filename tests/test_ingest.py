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
