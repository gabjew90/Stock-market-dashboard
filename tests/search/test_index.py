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
