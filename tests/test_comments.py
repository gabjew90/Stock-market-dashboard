"""Reader comments are primary material the post bodies do not contain.

On a methodology blog the comment threads are where a reader asks "what exactly counts
as a close below the green line?" and Dr. Wish answers. The scraper ignored them for the
project's whole life; these tests pin the behaviour that fixes that.
"""
import json

import httpx

from ww.scrape.comments import CommentRecord, read_comments_jsonl, scrape_comments

_PAGE1 = [
    {
        "id": 11,
        "post": 49378,
        "date": "2026-05-11T08:00:00",
        "author_name": "A Reader",
        "parent": 0,
        "link": "https://example.test/p/#comment-11",
        "content": {"rendered": "<p>Does a <em>close</em> below the green line count intraday?</p>"},
    },
    {
        "id": 12,
        "post": 49378,
        "date": "2026-05-11T09:30:00",
        "author_name": "Dr. Wish",
        "parent": 11,
        "link": "https://example.test/p/#comment-12",
        "content": {"rendered": "<p>No &#8212; only the weekly close matters.</p>"},
    },
]


def _client(pages: dict[int, list[dict]]) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        body = pages.get(page)
        if body is None:
            return httpx.Response(400, json={"code": "rest_comment_invalid_page_number"})
        return httpx.Response(200, json=body)

    return httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")


def test_scrape_comments_writes_jsonl_with_text_and_threading(tmp_path):
    n = scrape_comments("https://example.test", root=tmp_path, client=_client({1: _PAGE1}), delay=0.0)
    assert n == 2

    rows = read_comments_jsonl(tmp_path / "raw" / "comments.jsonl")
    assert [r.comment_id for r in rows] == [11, 12]
    assert all(isinstance(r, CommentRecord) for r in rows)

    q, a = rows
    assert q.post_id == 49378
    assert q.author == "A Reader"
    assert q.parent == 0
    # HTML stripped and entities decoded, so the text is searchable alongside post bodies.
    assert q.text == "Does a close below the green line count intraday?"
    assert a.text == "No — only the weekly close matters."
    # Threading preserved: the reply points at the question it answers.
    assert a.parent == q.comment_id


def test_scrape_comments_paginates_and_stops_on_invalid_page(tmp_path):
    page2 = [dict(_PAGE1[0], id=13, post=1, parent=0, date="2026-05-12T07:00:00")]
    n = scrape_comments("https://example.test", root=tmp_path, client=_client({1: _PAGE1, 2: page2}), delay=0.0)
    assert n == 3
    # Rows come out in chronological order regardless of which page they arrived on.
    assert [r.comment_id for r in read_comments_jsonl(tmp_path / "raw" / "comments.jsonl")] == [11, 12, 13]


def test_scrape_comments_caches_pages_and_reuses_them(tmp_path):
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        page = int(request.url.params.get("page", "1"))
        if page == 1:
            return httpx.Response(200, json=_PAGE1)
        return httpx.Response(400, json={"code": "rest_comment_invalid_page_number"})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test")
    scrape_comments("https://example.test", root=tmp_path, client=client, delay=0.0)
    assert calls["n"] == 2                     # page 1 (data) + page 2 (the terminal 400)
    assert (tmp_path / "raw" / "api-comments" / "page-0001.json").exists()

    scrape_comments("https://example.test", root=tmp_path, client=client, delay=0.0)
    # Page 1 is served from cache; only the terminal 400 probe is re-issued, because a
    # 400 is not a cacheable result — the next run must re-check whether page 2 now exists.
    assert calls["n"] == 3


def test_read_comments_jsonl_missing_file_is_empty(tmp_path):
    assert read_comments_jsonl(tmp_path / "nope.jsonl") == []


def test_comment_text_survives_a_round_trip(tmp_path):
    scrape_comments("https://example.test", root=tmp_path, client=_client({1: _PAGE1}), delay=0.0)
    raw = (tmp_path / "raw" / "comments.jsonl").read_text(encoding="utf-8").splitlines()
    assert json.loads(raw[0])["text"].startswith("Does a close")
