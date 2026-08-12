import json
from pathlib import Path

import pytest

from ww.search.index import SearchIndex, build_index


def _make_corpus(root: Path) -> None:
    (root / "wiki" / "methodology").mkdir(parents=True)
    (root / "wiki" / "_templates").mkdir(parents=True)
    (root / "raw" / "posts").mkdir(parents=True)
    (root / "wiki" / "methodology" / "green-line-breakouts.md").write_text(
        "---\ntitle: GLB\n---\n\n# Green Line Breakouts\n\n## What it is\n\nA green line is an all-time-high level held three months; the breakout is a close above it.\n\n## Sources\n\n_None._\n", encoding="utf-8")
    (root / "wiki" / "methodology" / "t2108.md").write_text(
        "---\ntitle: T2108\n---\n\n# T2108\n\nThe percent of stocks above their forty day moving average.\n\n## Sources\n\n_None._\n", encoding="utf-8")
    (root / "wiki" / "log.md").write_text("# Wiki log\n\n## [2026-05-11] note | x\n", encoding="utf-8")
    (root / "wiki" / "_templates" / "entity-page.md").write_text("template green line breakout placeholder\n", encoding="utf-8")
    (root / "raw" / "posts" / "2012-07-23-stage.md").write_text(
        "---\nurl: https://wishingwealthblog.com/2012/07/stage/\ndate: '2012-07-23T00:00:00'\npost_id: 1\ntitle: Stage analysis\n---\n\nI draw a green line on the monthly chart at the all time high.\n", encoding="utf-8")
    rows = [{"post_id": 1, "url": "https://wishingwealthblog.com/2012/07/stage/", "date": "2012-07-23T00:00:00",
             "slug": "stage", "stem": "2012-07-23-stage", "title": "Stage analysis", "word_count": 20,
             "chart_count": 0, "chart_image_urls": [], "kind_guess": "long_form"}]
    (root / "raw" / "posts.jsonl").write_text(json.dumps(rows[0]) + "\n", encoding="utf-8")


def test_build_index_covers_wiki_and_posts_but_not_templates_or_log(tmp_path):
    _make_corpus(tmp_path)
    idx = build_index(tmp_path)
    sources = {c.source for c in idx.chunks}
    assert "wiki:methodology/green-line-breakouts.md" in sources
    assert "wiki:methodology/t2108.md" in sources
    assert "post:2012-07-23-stage" in sources
    assert not any(s.startswith("wiki:_templates") for s in sources)
    assert "wiki:log.md" not in sources


def test_search_returns_relevant_cited_hits(tmp_path):
    _make_corpus(tmp_path)
    idx = build_index(tmp_path)
    hits = idx.search("green line breakout all time high", top_k=3)
    assert hits, "expected some hits"
    top = hits[0]
    assert "green" in top.text.lower() and "line" in top.text.lower()
    # citation: wiki hits carry the page path; post hits carry the date + url
    assert top.citation  # non-empty
    # a post hit's citation should include the date / url
    post_hits = [h for h in hits if h.source.startswith("post:")]
    if post_hits:
        assert "2012-07-23" in post_hits[0].citation or "wishingwealthblog.com" in post_hits[0].citation


def test_search_source_filter(tmp_path):
    _make_corpus(tmp_path)
    idx = build_index(tmp_path)
    assert all(h.source.startswith("wiki:") for h in idx.search("green line", top_k=5, source="wiki"))
    assert all(h.source.startswith("post:") for h in idx.search("green line", top_k=5, source="posts"))


def test_search_since_filters_posts_by_year(tmp_path):
    _make_corpus(tmp_path)
    idx = build_index(tmp_path)
    assert idx.search("green line", top_k=5, since=2020) == [] or all(not h.source.startswith("post:2012") for h in idx.search("green line", top_k=5, since=2020))
    assert any(h.source == "post:2012-07-23-stage" for h in idx.search("green line monthly chart", top_k=5, since=2010))


def test_index_save_load_roundtrip(tmp_path):
    _make_corpus(tmp_path)
    idx = build_index(tmp_path)
    p = tmp_path / "data" / "index" / "wiki.pkl"
    idx.save(p)
    assert p.exists()
    idx2 = SearchIndex.load(p)
    assert len(idx2.chunks) == len(idx.chunks)
    assert idx2.search("green line breakout", top_k=1)[0].text == idx.search("green line breakout", top_k=1)[0].text


def _add_comments(root: Path) -> None:
    """Two comments on the indexed post: a reader question and Dr. Wish's answer."""
    rows = [
        {"comment_id": 11, "post_id": 1, "date": "2012-07-24T08:00:00", "author": "A Reader",
         "parent": 0, "text": "Does an intraday dip below the green line count as a violation?",
         "url": "https://wishingwealthblog.com/2012/07/stage/#comment-11"},
        {"comment_id": 12, "post_id": 1, "date": "2012-07-24T09:00:00", "author": "Dr. Wish",
         "parent": 11, "text": "No, I only heed the weekly closing price below the green line.",
         "url": "https://wishingwealthblog.com/2012/07/stage/#comment-12"},
    ]
    (root / "raw" / "comments.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def test_build_index_includes_comments(tmp_path):
    """4,136 reader comments carry rule clarifications absent from the post bodies —
    they are useless unless `ww search` can reach them."""
    _make_corpus(tmp_path)
    _add_comments(tmp_path)
    idx = build_index(tmp_path)
    assert any(c.source.startswith("comment:") for c in idx.chunks)


def test_search_finds_a_clarification_only_present_in_a_comment(tmp_path):
    _make_corpus(tmp_path)
    _add_comments(tmp_path)
    idx = build_index(tmp_path)
    hits = idx.search("intraday dip below the green line violation", top_k=5)
    assert any(h.source.startswith("comment:") for h in hits)


def test_comment_hits_cite_author_date_and_parent_post(tmp_path):
    _make_corpus(tmp_path)
    _add_comments(tmp_path)
    idx = build_index(tmp_path)
    hit = next(h for h in idx.search("weekly closing price below the green line", top_k=8)
               if h.source.startswith("comment:"))
    # A comment is only usable as evidence if you can attribute it and find the thread.
    assert "Dr. Wish" in hit.citation
    assert "2012-07-24" in hit.citation
    assert "2012-07-23-stage" in hit.citation


def test_search_source_filter_comments(tmp_path):
    _make_corpus(tmp_path)
    _add_comments(tmp_path)
    idx = build_index(tmp_path)
    hits = idx.search("green line", top_k=8, source="comments")
    assert hits and all(h.source.startswith("comment:") for h in hits)


def test_index_without_comments_file_still_builds(tmp_path):
    _make_corpus(tmp_path)
    idx = build_index(tmp_path)
    assert idx.chunks and not any(c.source.startswith("comment:") for c in idx.chunks)
