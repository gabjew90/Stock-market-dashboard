from pathlib import Path

from ww.corpus.index import PostRecord, write_posts_jsonl
from ww.stats import corpus_stats


def _rec(**over) -> PostRecord:
    base = dict(post_id=1, url="u", date="2020-01-01T00:00:00", slug="s", stem="2020-01-01-s",
                title="t", word_count=10, chart_count=0, chart_image_urls=[], kind_guess="unknown")
    base.update(over)
    return PostRecord(**base)


def test_stats_on_missing_index(tmp_path: Path):
    s = corpus_stats(tmp_path)
    assert s["total_posts"] == 0


def test_stats_counts_and_dates(tmp_path: Path):
    write_posts_jsonl(tmp_path / "raw" / "posts.jsonl", [
        _rec(post_id=1, date="2005-04-17T00:00:00", stem="2005-04-17-a", kind_guess="long_form", chart_count=2, chart_image_urls=["x", "y"]),
        _rec(post_id=2, date="2026-05-10T00:00:00", stem="2026-05-10-b", kind_guess="daily_update", chart_count=1, chart_image_urls=["z"]),
        _rec(post_id=3, date="2015-01-01T00:00:00", stem="2015-01-01-c", kind_guess="daily_update", ingested=True, tier="daily_update"),
    ])
    s = corpus_stats(tmp_path)
    assert s["total_posts"] == 3
    assert s["date_range"] == ("2005-04-17T00:00:00", "2026-05-10T00:00:00")
    assert s["by_kind_guess"] == {"long_form": 1, "daily_update": 2}
    assert s["by_tier"] == {"daily_update": 1, None: 2}  # only post 3 has a tier
    assert s["ingested"] == 1
    assert s["posts_with_charts"] == 2
    assert s["total_chart_images"] == 3
