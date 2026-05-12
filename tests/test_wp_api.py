import json
from pathlib import Path

import httpx
import pytest

from ww.scrape.wp_api import iter_post_pages


def _mock_transport(fixtures_dir: Path) -> httpx.MockTransport:
    page1 = json.loads((fixtures_dir / "wp_api_page1.json").read_text())
    page2 = json.loads((fixtures_dir / "wp_api_page2.json").read_text())

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if page == 1:
            return httpx.Response(200, json=page1, headers={"X-WP-TotalPages": "1"})
        # WordPress returns 400 rest_post_invalid_page_number past the last page;
        # also accept an empty 200 list as an end signal.
        return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})

    return httpx.MockTransport(handler)


def test_iter_post_pages_yields_all_posts(fixtures_dir, tmp_path):
    client = httpx.Client(transport=_mock_transport(fixtures_dir), base_url="https://example.test")
    pages = list(iter_post_pages("https://example.test", cache_dir=tmp_path / "api", client=client, delay=0.0))
    assert len(pages) == 1
    assert [p["id"] for p in pages[0]] == [49378, 832]


def test_iter_post_pages_writes_cache_files(fixtures_dir, tmp_path):
    cache = tmp_path / "api"
    client = httpx.Client(transport=_mock_transport(fixtures_dir), base_url="https://example.test")
    list(iter_post_pages("https://example.test", cache_dir=cache, client=client, delay=0.0))
    assert (cache / "page-0001.json").exists()
    cached = json.loads((cache / "page-0001.json").read_text())
    assert cached[0]["id"] == 49378


def test_iter_post_pages_uses_cache_without_http(fixtures_dir, tmp_path):
    cache = tmp_path / "api"
    cache.mkdir()
    (cache / "page-0001.json").write_text(json.dumps([{"id": 1, "date": "2020-01-01T00:00:00", "slug": "x", "link": "u", "title": {"rendered": "t"}, "content": {"rendered": "<p>b</p>"}}]))

    def fail_handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("HTTP must not be called when a cache file exists")

    client = httpx.Client(transport=httpx.MockTransport(fail_handler), base_url="https://example.test")
    pages = list(iter_post_pages("https://example.test", cache_dir=cache, client=client, delay=0.0, max_pages=1))
    assert pages[0][0]["id"] == 1
