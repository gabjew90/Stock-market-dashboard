from pathlib import Path

import pytest

from ww.corpus.index import PostRecord, read_posts_jsonl, write_posts_jsonl
from ww.corpus.ledger import (
    LedgerEntry,
    apply_ledger,
    apply_to_posts,
    export_from_posts,
    export_ledger,
    read_ledger,
    reconstruct_from_wiki,
    write_ledger,
)


def _post(stem: str, **kw) -> PostRecord:
    defaults = dict(
        post_id=abs(hash(stem)) % 10_000,
        url=f"https://example.test/{stem}",
        date=f"{stem[:10]}T12:00:00",
        slug=stem[11:],
        stem=stem,
        title=stem[11:].replace("-", " "),
        word_count=800,
        chart_count=0,
    )
    defaults.update(kw)
    return PostRecord(**defaults)


def test_export_skips_untouched_posts():
    posts = [
        _post("2005-04-23-lets-talk-strategy", tier="teaching", ingested=True),
        _post("2005-04-24-nothing-here"),
    ]
    entries = export_from_posts(posts)
    assert [e.stem for e in entries] == ["2005-04-23-lets-talk-strategy"]
    assert entries[0].tier == "teaching" and entries[0].ingested is True


def test_ledger_round_trip_restores_state(tmp_path: Path):
    posts_jsonl = tmp_path / "posts.jsonl"
    ledger_path = tmp_path / "ingest-ledger.jsonl"
    curated = _post(
        "2012-07-23-stage-analysis",
        tier="teaching",
        summary="GLB formally defined",
        indicators=["glb", "gmi"],
        tickers=["QQQ"],
        ingested=True,
        summary_page="wiki/sources/2012-07-23-stage-analysis.md",
    )
    write_posts_jsonl(posts_jsonl, [curated, _post("2012-07-24-daily")])

    assert export_ledger(posts_jsonl, ledger_path) == 1

    # Simulate a fresh `ww scrape`: same posts, all curated state lost.
    write_posts_jsonl(posts_jsonl, [_post("2012-07-23-stage-analysis"), _post("2012-07-24-daily")])
    applied, unmatched, _reverted = apply_ledger(ledger_path, posts_jsonl)

    assert (applied, unmatched) == (1, [])
    restored = {p.stem: p for p in read_posts_jsonl(posts_jsonl)}
    assert restored["2012-07-23-stage-analysis"].tier == "teaching"
    assert restored["2012-07-23-stage-analysis"].indicators == ["glb", "gmi"]
    assert restored["2012-07-23-stage-analysis"].ingested is True
    # untouched rows stay untouched
    assert restored["2012-07-24-daily"].tier is None


def test_apply_reports_stems_missing_from_the_corpus():
    posts = [_post("2020-01-01-present")]
    applied, unmatched, _reverted = apply_to_posts(
        [LedgerEntry(stem="2020-01-01-present", tier="teaching"), LedgerEntry(stem="1999-01-01-gone")],
        posts,
    )
    assert applied == 1
    assert unmatched == ["1999-01-01-gone"]
    assert posts[0].tier == "teaching"


def test_apply_without_a_corpus_is_an_error(tmp_path: Path):
    write_ledger(tmp_path / "l.jsonl", [LedgerEntry(stem="x", tier="teaching")])
    with pytest.raises(FileNotFoundError):
        apply_ledger(tmp_path / "l.jsonl", tmp_path / "missing.jsonl")


def test_write_ledger_sorts_by_stem(tmp_path: Path):
    path = tmp_path / "l.jsonl"
    write_ledger(path, [LedgerEntry(stem="2020-01-01-b"), LedgerEntry(stem="2005-01-01-a")])
    assert [e.stem for e in read_ledger(path)] == ["2005-01-01-a", "2020-01-01-b"]


def test_reconstruct_from_wiki_recovers_tier_and_index_summary(tmp_path: Path):
    wiki = tmp_path / "wiki"
    (wiki / "sources").mkdir(parents=True)
    stem = "2018-05-20-glb-explained"
    (wiki / "sources" / f"{stem}.md").write_text(
        "---\ntype: source-summary\n---\n\n"
        "# WW 2018-05-20 — Green line breakout explained\n\n"
        f"**Source:** [GLB explained](../../raw/posts/{stem}.md) · [original](https://x.test) · tier: trade_example\n",
        encoding="utf-8",
    )
    (wiki / "index.md").write_text(
        f"## Sources\n\n- [WW 2018-05-20 — GLB explained](sources/{stem}.md) — already-doubled attribute; strict sell rule.\n",
        encoding="utf-8",
    )
    (entry,) = reconstruct_from_wiki(wiki)
    assert entry.stem == stem
    assert entry.tier == "trade_example"
    assert entry.ingested is True
    assert entry.summary_page == f"wiki/sources/{stem}.md"
    assert entry.summary == "already-doubled attribute; strict sell rule."


def test_reconstruct_falls_back_to_the_h1_when_the_index_has_no_entry(tmp_path: Path):
    wiki = tmp_path / "wiki"
    (wiki / "sources").mkdir(parents=True)
    (wiki / "sources" / "2005-04-23-lets-talk.md").write_text(
        "# WW 2005-04-23 — Let's Talk Strategy\n\n**Source:** x · tier: teaching\n", encoding="utf-8"
    )
    (entry,) = reconstruct_from_wiki(wiki)
    assert entry.summary == "WW 2005-04-23 — Let's Talk Strategy"


def test_apply_reports_rows_it_would_revert(tmp_path):
    """If a session ingested posts but forgot `ww ledger export`, `apply` silently
    overwrites the newer state in posts.jsonl with the older ledger. It must at least
    report which rows carry newer curated state than the ledger."""
    from ww.corpus.index import PostRecord, write_posts_jsonl
    from ww.corpus.ledger import LedgerEntry, write_ledger, apply_ledger

    posts_p = tmp_path / "posts.jsonl"; ledger_p = tmp_path / "ledger.jsonl"
    # posts.jsonl: stem A already curated locally (newer), stem B untouched.
    write_posts_jsonl(posts_p, [
        PostRecord(post_id=1, url="u", date="2020-01-01T00:00:00", slug="a", stem="2020-01-01-a", title="A",
                   word_count=1, chart_count=0, tier="teaching", summary="local newer", ingested=True,
                   summary_page="wiki/sources/2020-01-01-a.md"),
        PostRecord(post_id=2, url="u", date="2020-01-02T00:00:00", slug="b", stem="2020-01-02-b", title="B",
                   word_count=1, chart_count=0),
    ])
    # ledger: stem A with OLDER, different state.
    write_ledger(ledger_p, [LedgerEntry(stem="2020-01-01-a", tier="teaching", summary="ledger older", ingested=True,
                                        summary_page="wiki/sources/2020-01-01-a.md")])
    applied, unmatched, reverted = apply_ledger(ledger_p, posts_p)
    assert applied == 1 and unmatched == []
    assert reverted == ["2020-01-01-a"]
