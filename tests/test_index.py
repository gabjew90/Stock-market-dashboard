import json
from pathlib import Path

import pytest

from ww.corpus.index import PostRecord, read_posts_jsonl, update_records, write_posts_jsonl


def _rec(**over) -> PostRecord:
    base = dict(
        post_id=1,
        url="https://wishingwealthblog.com/2020/01/x/",
        date="2020-01-01T00:00:00",
        slug="x",
        stem="2020-01-01-x",
        title="X",
        word_count=10,
        chart_count=0,
        chart_image_urls=[],
        kind_guess="unknown",
        tier=None,
        summary=None,
        indicators=None,
        tickers=None,
        ingested=False,
        summary_page=None,
    )
    base.update(over)
    return PostRecord(**base)


def test_round_trips_records(tmp_path: Path):
    path = tmp_path / "posts.jsonl"
    recs = [_rec(post_id=1, slug="a", stem="2020-01-01-a"), _rec(post_id=2, slug="b", stem="2020-01-02-b")]
    write_posts_jsonl(path, recs)
    loaded = read_posts_jsonl(path)
    assert [r.post_id for r in loaded] == [1, 2]
    assert loaded[0].slug == "a"
    assert loaded[1].ingested is False


def test_read_missing_file_returns_empty(tmp_path: Path):
    assert read_posts_jsonl(tmp_path / "nope.jsonl") == []


def test_write_is_one_json_object_per_line(tmp_path: Path):
    path = tmp_path / "posts.jsonl"
    write_posts_jsonl(path, [_rec(post_id=1), _rec(post_id=2)])
    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["post_id"] == 1


def test_read_ignores_unknown_jsonl_fields(tmp_path: Path):
    """read_posts_jsonl must not crash if a JSONL line has an unknown future field."""
    path = tmp_path / "posts.jsonl"
    row = dict(
        post_id=42,
        url="https://wishingwealthblog.com/2020/01/x/",
        date="2020-01-01T00:00:00",
        slug="x",
        stem="2020-01-01-x",
        title="X",
        word_count=5,
        chart_count=0,
        FUTURE_FIELD=1,
    )
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    records = read_posts_jsonl(path)
    assert len(records) == 1
    assert records[0].post_id == 42


def test_update_records_patches_matching_rows_only(tmp_path: Path):
    path = tmp_path / "posts.jsonl"
    write_posts_jsonl(path, [
        _rec(post_id=1, slug="a", stem="2020-01-01-a"),
        _rec(post_id=2, slug="b", stem="2020-01-02-b"),
        _rec(post_id=3, slug="c", stem="2020-01-03-c"),
    ])
    update_records(path, {
        2: {"tier": "teaching", "summary": "explains GMI", "ingested": True, "summary_page": "wiki/sources/2020-01-02-b.md"},
        3: {"tier": "daily_update", "ingested": True},
    })
    loaded = {r.post_id: r for r in read_posts_jsonl(path)}
    assert loaded[1].tier is None and loaded[1].ingested is False           # untouched
    assert loaded[2].tier == "teaching" and loaded[2].summary == "explains GMI"
    assert loaded[2].ingested is True and loaded[2].summary_page == "wiki/sources/2020-01-02-b.md"
    assert loaded[3].tier == "daily_update" and loaded[3].ingested is True
    assert loaded[3].summary is None                                        # not in the patch -> unchanged
    # order preserved
    assert [r.post_id for r in read_posts_jsonl(path)] == [1, 2, 3]


def test_update_records_unknown_post_id_raises(tmp_path: Path):
    path = tmp_path / "posts.jsonl"
    write_posts_jsonl(path, [_rec(post_id=1, slug="a", stem="2020-01-01-a")])
    with pytest.raises(KeyError):
        update_records(path, {999: {"tier": "meta"}})


def test_update_records_unknown_field_raises(tmp_path: Path):
    path = tmp_path / "posts.jsonl"
    write_posts_jsonl(path, [_rec(post_id=1, slug="a", stem="2020-01-01-a")])
    with pytest.raises(ValueError):
        update_records(path, {1: {"not_a_field": 1}})
