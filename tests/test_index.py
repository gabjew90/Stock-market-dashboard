from pathlib import Path

from ww.corpus.index import PostRecord, read_posts_jsonl, write_posts_jsonl


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
    import json
    assert json.loads(lines[0])["post_id"] == 1
