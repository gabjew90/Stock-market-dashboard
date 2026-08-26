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


def test_iter_post_pages_caches_full_pages_including_page_one(fixtures_dir, tmp_path):
    """Under oldest-first ordering every full page is immutable, so all of them are cached.
    Only the final short page - where new posts land - is left uncached."""
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
    assert (cache / "page-0001.json").exists()       # full page 1: now cached
    assert (cache / "page-0002.json").exists()       # full page 2: cached
    assert json.loads((cache / "page-0002.json").read_text())[0]["id"] == 3
    assert not (cache / "page-0003.json").exists()   # short final page: not cached


def test_iter_post_pages_requests_oldest_first(fixtures_dir, tmp_path):
    """`order=asc` is what makes the page cache sound - see the regression test below."""
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen.update(dict(request.url.params))
        return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")
    list(iter_post_pages("https://example.test", cache_dir=tmp_path / "api", client=client, delay=0.0))
    assert seen["order"] == "asc"
    assert seen["orderby"] == "date"


def test_newly_published_posts_do_not_displace_cached_pages(tmp_path):
    """Regression (2026-08-26): six live posts vanished from raw/posts.jsonl on re-scrape.

    Under the old newest-first ordering, publishing K posts shifted every offset by K, so
    the K posts that had been at the tail of a cached page slid past the boundary and were
    never fetched again. Oldest-first ordering appends new posts at the end, so this
    scrape-publish-rescrape sequence must lose nothing.
    """
    rec = lambda i: {"id": i, "date": f"2020-01-01T00:00:{i % 60:02d}", "slug": f"s{i}", "link": "u",
                     "title": {"rendered": "t"}, "content": {"rendered": "<p>b</p>"}}
    corpus = [rec(i) for i in range(1, 11)]          # 10 posts, oldest first
    cache = tmp_path / "api"

    def make_client(store):
        def handler(request: httpx.Request) -> httpx.Response:
            page = int(request.url.params.get("page", "1"))
            per = int(request.url.params.get("per_page", "100"))
            assert request.url.params.get("order") == "asc", "the fix depends on oldest-first"
            chunk = store[(page - 1) * per: page * per]
            if not chunk:
                return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})
            return httpx.Response(200, json=chunk)
        return httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")

    def scrape(store):
        pages = list(iter_post_pages("https://example.test", cache_dir=cache,
                                     client=make_client(store), delay=0.0, per_page=4))
        return [p["id"] for page in pages for p in page]

    assert scrape(corpus) == list(range(1, 11))
    # ...the blog publishes 3 more, shifting nothing that came before.
    grown = corpus + [rec(i) for i in range(11, 14)]
    assert scrape(grown) == list(range(1, 14)), "a post was lost across the page boundary"


def test_iter_post_pages_uses_cache_without_http_for_full_pages(fixtures_dir, tmp_path):
    """Cached full pages are served from disk with no request; only the uncached tail is fetched."""
    cache = tmp_path / "api"
    cache.mkdir()
    rec = lambda i: {"id": i, "date": "2020-01-01T00:00:00", "slug": f"x{i}", "link": "u",
                     "title": {"rendered": "t"}, "content": {"rendered": "<p>b</p>"}}
    (cache / "page-0001.json").write_text(json.dumps([rec(1), rec(2)]))
    calls = {"pages": []}

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        calls["pages"].append(page)
        if page == 2:
            return httpx.Response(200, json=[rec(3), rec(4)])
        return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")
    pages = list(iter_post_pages("https://example.test", cache_dir=cache, client=client, delay=0.0, per_page=2, max_pages=2))
    assert calls["pages"] == [2]                # page 1 from cache, page 2 fetched
    assert [p[0]["id"] for p in pages] == [1, 3]


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
