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


def test_iter_post_pages_writes_cache_files_for_full_pages_beyond_page_one(fixtures_dir, tmp_path):
    """Page 1 is deliberately NEVER cached (newest-first: new posts land there), and short
    pages are not cached either. A full page 2+ IS cached. Simulate 3 pages at per_page=2."""
    page1 = json.loads((fixtures_dir / "wp_api_page1.json").read_text())
    mk = lambda i: {"id": i, "date": f"2019-01-{i:02d}T00:00:00", "slug": f"s{i}", "link": "u",
                    "title": {"rendered": "t"}, "content": {"rendered": "<p>b</p>"}}
    pages = {1: page1[:2], 2: [mk(3), mk(4)], 3: [mk(5)]}  # page 3 is short

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if page in pages:
            return httpx.Response(200, json=pages[page])
        return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})

    cache = tmp_path / "api"
    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")
    list(iter_post_pages("https://example.test", cache_dir=cache, client=client, delay=0.0, per_page=2))
    assert not (cache / "page-0001.json").exists()   # never cached
    assert (cache / "page-0002.json").exists()       # full page 2+: cached
    assert json.loads((cache / "page-0002.json").read_text())[0]["id"] == 3
    assert not (cache / "page-0003.json").exists()   # short final page: not cached


def test_iter_post_pages_non_json_400_raises_http_status_error(fixtures_dir, tmp_path):
    """A 400 with a non-JSON body (e.g. CDN/WAF block) must raise HTTPStatusError,
    not JSONDecodeError, and page 1 posts must have been yielded before the error."""
    page1 = json.loads((fixtures_dir / "wp_api_page1.json").read_text())

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if page == 1:
            return httpx.Response(200, json=page1)
        return httpx.Response(400, text="<html>blocked</html>")

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")
    gen = iter_post_pages("https://example.test", cache_dir=tmp_path / "api", client=client, delay=0.0)
    yielded = []
    with pytest.raises(httpx.HTTPStatusError):
        for page in gen:
            yielded.append(page)
    assert len(yielded) == 1
    assert [p["id"] for p in yielded[0]] == [49378, 832]


def test_iter_post_pages_uses_cache_without_http_for_page_two_onward(fixtures_dir, tmp_path):
    """Cached pages 2+ are served from disk with no request. Page 1 is always re-fetched
    (see wp_api.py) so that newly published posts are picked up on re-scrape."""
    cache = tmp_path / "api"
    cache.mkdir()
    rec = lambda i: {"id": i, "date": "2020-01-01T00:00:00", "slug": f"x{i}", "link": "u",
                     "title": {"rendered": "t"}, "content": {"rendered": "<p>b</p>"}}
    (cache / "page-0002.json").write_text(json.dumps([rec(3), rec(4)]))
    calls = {"pages": []}

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        calls["pages"].append(page)
        if page == 1:
            return httpx.Response(200, json=[rec(1), rec(2)])
        raise AssertionError(f"HTTP must not be called for cached page {page}")

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")
    pages = list(iter_post_pages("https://example.test", cache_dir=cache, client=client, delay=0.0, per_page=2, max_pages=2))
    assert calls["pages"] == [1]                # page 1 fetched, page 2 from cache
    assert [p[0]["id"] for p in pages] == [1, 3]
