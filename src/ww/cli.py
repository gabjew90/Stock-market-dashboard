"""`ww` command-line interface."""
from __future__ import annotations

from pathlib import Path

import typer
import yaml

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


if __name__ == "__main__":  # pragma: no cover
    app()
