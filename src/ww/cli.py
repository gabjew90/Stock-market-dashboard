"""`ww` command-line interface."""
from __future__ import annotations

from pathlib import Path

import typer
import yaml

from ww.maintain.lint import lint_wiki
from ww.scrape.ingest import scrape_blog
from ww.stats import corpus_stats

app = typer.Typer(help="Wishing Wealth Wiki tooling.", no_args_is_help=True)

DEFAULT_BASE_URL = "https://wishingwealthblog.com"


@app.command()
def scrape(
    root: Path = typer.Option(Path("."), "--root", help="Repo root (writes raw/posts/ and raw/posts.jsonl)."),
    base_url: str = typer.Option(DEFAULT_BASE_URL, "--base-url", help="Blog base URL."),
    delay: float = typer.Option(1.0, "--delay", help="Seconds between network requests (cache hits are free)."),
    force: bool = typer.Option(False, "--force", help="Rewrite post markdown files that already exist."),
) -> None:
    """Pull every public blog post into raw/posts/*.md and rebuild raw/posts.jsonl."""
    n = scrape_blog(base_url, root=root, delay=delay, force=force)
    typer.echo(f"Scraped {n} posts -> {root / 'raw' / 'posts'} (index: {root / 'raw' / 'posts.jsonl'})")


@app.command()
def stats(
    root: Path = typer.Option(Path("."), "--root", help="Repo root."),
) -> None:
    """Print corpus counts for the raw-sources index."""
    typer.echo(yaml.safe_dump(corpus_stats(root), sort_keys=False, allow_unicode=True).rstrip())


@app.command()
def lint(
    root: Path = typer.Argument(Path("."), help="Repo root (the directory containing wiki/)."),
) -> None:
    """Mechanical wiki integrity checks (broken links, missing Sources, uncatalogued/orphan pages, summary_page)."""
    report = lint_wiki(root)
    for w in report.warnings:
        typer.echo(f"warning: {w}")
    for e in report.errors:
        typer.echo(f"error: {e}")
    if report.errors:
        typer.echo(f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        raise typer.Exit(code=1)
    typer.echo(f"OK — 0 errors, {len(report.warnings)} warning(s)")


if __name__ == "__main__":  # pragma: no cover
    app()
