import json
from pathlib import Path

from typer.testing import CliRunner

from ww import cli
from ww.corpus.index import PostRecord, read_posts_jsonl, write_posts_jsonl

runner = CliRunner()


def _rec(post_id: int, stem: str, **over) -> PostRecord:
    base = dict(post_id=post_id, url="u", date="2020-01-01T00:00:00", slug=stem[11:], stem=stem,
                title="t", word_count=20, chart_count=0, chart_image_urls=[], kind_guess="daily_update")
    base.update(over)
    return PostRecord(**base)


def _corpus(root: Path, posts: list[tuple[PostRecord, str]]) -> None:
    (root / "raw" / "posts").mkdir(parents=True, exist_ok=True)
    for rec, body in posts:
        (root / "raw" / "posts" / f"{rec.stem}.md").write_text(
            f"---\ntitle: {rec.title}\n---\n{body}", encoding="utf-8")
    write_posts_jsonl(root / "raw" / "posts.jsonl", [r for r, _ in posts])


def test_dry_run_reports_the_split_and_writes_nothing(tmp_path: Path):
    _corpus(tmp_path, [
        (_rec(1, "2020-01-01-routine"), "GMI = 6. T2108 61%."),
        (_rec(2, "2020-01-02-teaches"), "I have learned that the key to this is patience."),
    ])
    result = runner.invoke(cli.app, ["tier", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "1 -> daily_update, 1 held" in result.stdout
    assert "dry run" in result.stdout
    assert all(r.tier is None for r in read_posts_jsonl(tmp_path / "raw" / "posts.jsonl"))


def test_apply_writes_tiers_only_for_the_screened_posts(tmp_path: Path):
    _corpus(tmp_path, [
        (_rec(1, "2020-01-01-routine"), "GMI = 6. T2108 61%."),
        (_rec(2, "2020-01-02-teaches"), "I have learned that the key to this is patience."),
    ])
    result = runner.invoke(cli.app, ["tier", "--root", str(tmp_path), "--apply"])
    assert result.exit_code == 0
    by_id = {r.post_id: r for r in read_posts_jsonl(tmp_path / "raw" / "posts.jsonl")}
    assert by_id[1].tier == "daily_update" and by_id[1].ingested is True
    assert by_id[1].summary.startswith("[bulk-tiered]")
    # The teaching post is untouched — held, not classified.
    assert by_id[2].tier is None and by_id[2].ingested is False


def test_already_ingested_posts_are_not_revisited(tmp_path: Path):
    _corpus(tmp_path, [
        (_rec(1, "2020-01-01-done", ingested=True, tier="teaching", summary="hand written"),
         "GMI = 6. T2108 61%."),
    ])
    runner.invoke(cli.app, ["tier", "--root", str(tmp_path), "--apply"])
    rec = read_posts_jsonl(tmp_path / "raw" / "posts.jsonl")[0]
    assert rec.tier == "teaching"
    assert rec.summary == "hand written"


def test_long_form_is_held_even_when_it_looks_routine(tmp_path: Path):
    _corpus(tmp_path, [
        (_rec(1, "2020-01-01-essay", kind_guess="long_form", word_count=900), "GMI = 6."),
    ])
    result = runner.invoke(cli.app, ["tier", "--root", str(tmp_path), "--apply"])
    assert "0 -> daily_update, 1 held" in result.stdout
    assert read_posts_jsonl(tmp_path / "raw" / "posts.jsonl")[0].tier is None


def test_missing_body_file_does_not_crash(tmp_path: Path):
    """raw/posts/ can be sparse in a partial checkout; screen on metadata alone."""
    (tmp_path / "raw").mkdir(parents=True)
    write_posts_jsonl(tmp_path / "raw" / "posts.jsonl", [_rec(1, "2020-01-01-gone")])
    result = runner.invoke(cli.app, ["tier", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "1 -> daily_update" in result.stdout
