from pathlib import Path

import pytest

from ww.maintain.lint import lint_wiki


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _good_wiki(root: Path) -> None:
    """A minimal wiki that should pass lint cleanly."""
    (root / "raw" / "posts").mkdir(parents=True, exist_ok=True)
    (root / "raw" / "posts" / "2020-01-01-x.md").write_text("body", encoding="utf-8")
    (root / "raw" / "posts.jsonl").write_text("", encoding="utf-8")
    _write(root / "wiki" / "index.md",
           "# Wiki index\n\n## Overview\n- [Overview](overview.md) — start.\n\n## Methodology\n- [GMI](methodology/gmi.md) — composite.\n")
    _write(root / "wiki" / "log.md", "# Wiki log\n\n## [2026-05-11] note | bootstrap\n")
    _write(root / "wiki" / "overview.md",
           "---\ntitle: Overview\ntype: overview\nupdated: 2026-05-11\nsources: []\n---\n\n# Overview\n\n- [GMI](methodology/gmi.md)\n\n## Sources\n\n_None yet._\n")
    _write(root / "wiki" / "methodology" / "gmi.md",
           "---\ntitle: GMI\ntype: entity\nupdated: 2026-05-11\nsources: []\n---\n\n# GMI\n\nSee ([WW 2020-01-01](../../raw/posts/2020-01-01-x.md)).\n\n## Sources\n\n- [WW 2020-01-01](../../raw/posts/2020-01-01-x.md)\n"
           )
    _write(root / "wiki" / "_templates" / "entity-page.md", "---\ntitle: <x>\n---\n# <x>\n## Sources\n_None yet._\n")
    (root / "wiki" / "sources").mkdir(parents=True, exist_ok=True)
    (root / "wiki" / "sources" / ".gitkeep").write_text("", encoding="utf-8")


def test_clean_wiki_passes(tmp_path: Path):
    _good_wiki(tmp_path)
    report = lint_wiki(tmp_path)
    assert report.ok, report.errors
    assert report.errors == []


def test_broken_internal_link_is_an_error(tmp_path: Path):
    _good_wiki(tmp_path)
    # Point gmi.md's body link at a non-existent page.
    p = tmp_path / "wiki" / "methodology" / "gmi.md"
    p.write_text(p.read_text(encoding="utf-8").replace("../../raw/posts/2020-01-01-x.md", "nonexistent-page.md", 1), encoding="utf-8")
    report = lint_wiki(tmp_path)
    assert not report.ok
    assert any("nonexistent-page.md" in e for e in report.errors)


def test_missing_sources_section_is_an_error(tmp_path: Path):
    _good_wiki(tmp_path)
    p = tmp_path / "wiki" / "methodology" / "gmi.md"
    p.write_text("---\ntitle: GMI\ntype: entity\nupdated: 2026-05-11\nsources: []\n---\n\n# GMI\n\nNo sources block here.\n", encoding="utf-8")
    report = lint_wiki(tmp_path)
    assert not report.ok
    assert any("Sources" in e and "gmi.md" in e for e in report.errors)


def test_page_not_in_index_is_an_error(tmp_path: Path):
    _good_wiki(tmp_path)
    _write(tmp_path / "wiki" / "methodology" / "t2108.md",
           "---\ntitle: T2108\ntype: entity\nupdated: 2026-05-11\nsources: []\n---\n\n# T2108\n\n[GMI](gmi.md)\n\n## Sources\n\n_None yet._\n")
    # t2108.md is not listed in index.md
    report = lint_wiki(tmp_path)
    assert not report.ok
    assert any("t2108.md" in e and "index" in e.lower() for e in report.errors)


def test_templates_and_index_and_log_are_not_linted_as_pages(tmp_path: Path):
    _good_wiki(tmp_path)
    # _templates/entity-page.md has no front-matter & isn't in index — must NOT be flagged.
    report = lint_wiki(tmp_path)
    assert report.ok
    assert not any("_templates" in e for e in report.errors)
    assert not any("index.md" in e for e in report.errors)
    assert not any("log.md" in e for e in report.errors)


def test_real_bootstrapped_wiki_passes_lint():
    """The wiki/ skeleton committed in Plan 2 must lint clean (errors only; warnings allowed)."""
    repo_root = Path(__file__).resolve().parents[1]
    report = lint_wiki(repo_root)
    assert report.errors == [], "Bootstrapped wiki has lint errors:\n" + "\n".join(report.errors)


def test_orphan_page_is_a_warning_not_an_error(tmp_path: Path):
    _good_wiki(tmp_path)
    # Add a page that's in index.md but linked from no other *page*.
    _write(tmp_path / "wiki" / "methodology" / "lonely.md",
           "---\ntitle: Lonely\ntype: concept\nupdated: 2026-05-11\nsources: []\n---\n\n# Lonely\n\n[GMI](gmi.md)\n\n## Sources\n\n_None yet._\n")
    # Index it so it's not flagged "not catalogued":
    idx = tmp_path / "wiki" / "index.md"
    idx.write_text(idx.read_text(encoding="utf-8") + "- [Lonely](methodology/lonely.md) — lonely.\n", encoding="utf-8")
    report = lint_wiki(tmp_path)
    assert report.ok, report.errors          # no errors
    assert any("lonely.md" in w and "orphan" in w for w in report.warnings)


def test_bad_summary_page_in_posts_jsonl_is_an_error(tmp_path: Path):
    _good_wiki(tmp_path)
    import json
    (tmp_path / "raw" / "posts.jsonl").write_text(
        json.dumps({"post_id": 1, "url": "u", "date": "2020-01-01T00:00:00", "slug": "x",
                    "stem": "2020-01-01-x", "title": "X", "word_count": 1, "chart_count": 0,
                    "chart_image_urls": [], "kind_guess": "unknown", "summary_page": "wiki/sources/ghost.md"}) + "\n",
        encoding="utf-8")
    report = lint_wiki(tmp_path)
    assert not report.ok
    assert any("ghost.md" in e and "summary_page" in e for e in report.errors)


from typer.testing import CliRunner

from ww import cli

_runner = CliRunner()


def test_ww_lint_command_ok_on_clean_wiki(tmp_path: Path):
    _good_wiki(tmp_path)
    result = _runner.invoke(cli.app, ["lint", str(tmp_path)])
    assert result.exit_code == 0
    assert "OK" in result.stdout or "0 errors" in result.stdout


def test_ww_lint_command_nonzero_on_errors(tmp_path: Path):
    _good_wiki(tmp_path)
    p = tmp_path / "wiki" / "methodology" / "gmi.md"
    p.write_text(p.read_text(encoding="utf-8").replace("../../raw/posts/2020-01-01-x.md", "ghost.md"), encoding="utf-8")
    result = _runner.invoke(cli.app, ["lint", str(tmp_path)])
    assert result.exit_code == 1
    assert "ghost.md" in result.stdout
