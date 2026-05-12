"""`ww` command-line interface."""
from __future__ import annotations

from pathlib import Path

import typer
import yaml

from ww.corpus.index import read_posts_jsonl
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


@app.command()
def batch(
    root: Path = typer.Option(Path("."), "--root", help="Repo root."),
    n: int = typer.Option(20, "-n", "--num", help="How many posts to list."),
    kind: str = typer.Option(None, "--kind", help="Filter by kind_guess (long_form / daily_update / unknown)."),
    oldest_first: bool = typer.Option(False, "--oldest-first", help="List oldest un-ingested first instead of newest."),
) -> None:
    """List the next un-ingested posts to feed the Ingest loop (see CLAUDE.md §4)."""
    records = [r for r in read_posts_jsonl(Path(root) / "raw" / "posts.jsonl") if not r.ingested]
    if kind:
        records = [r for r in records if r.kind_guess == kind]
    records.sort(key=lambda r: r.date, reverse=not oldest_first)
    for r in records[:n]:
        typer.echo(f"raw/posts/{r.stem}.md\t[{r.kind_guess}, {r.word_count}w]\t{r.title}")
    typer.echo(f"# {min(n, len(records))} of {len(records)} un-ingested" + (f" ({kind})" if kind else ""))


@app.command()
def compute(
    indicator: str = typer.Argument(..., help="green-line | stage | wgb | rwb | qqq-timing"),
    ticker: str = typer.Argument(..., help="Ticker symbol (or any label if using --csv)."),
    csv: Path = typer.Option(None, "--csv", help="Read OHLC from this CSV (date index + open,high,low,close) instead of yfinance."),
    weekly: bool = typer.Option(False, "--weekly", help="For 'rwb': use the weekly Guppy instead of the daily one."),
) -> None:
    """Run one of Dr. Wish's runnable price-based indicators on a ticker (see wiki/methodology/*.md)."""
    import pandas as pd
    from ww.indicators import (
        current_green_line, is_green_line_breakout, weekly_stage, ma_alignment_4_10_30,
        tenwk_below_thirtywk, weekly_green_bars, wgb_trailing_stop, rwb_state, red_line_count,
        short_term_trend, trend_day_count, YFinanceProvider,
    )

    # interval each indicator wants
    interval = {"green-line": "1mo", "stage": "1wk", "wgb": "1wk", "rwb": ("1wk" if weekly else "1d"), "qqq-timing": "1d"}.get(indicator)
    if interval is None:
        typer.echo(f"unknown indicator '{indicator}'. Choose: green-line, stage, wgb, rwb, qqq-timing")
        raise typer.Exit(code=2)

    if csv is not None:
        df = pd.read_csv(csv, index_col=0, parse_dates=True)
        df.columns = [c.lower() for c in df.columns]
    else:
        df = YFinanceProvider().prices(ticker, interval)

    if indicator == "green-line":
        gl = current_green_line(df)
        if gl is None:
            typer.echo(f"{ticker}: no green line yet (has never set an ATH that held >= 3 months).")
        else:
            last_close = float(df["close"].iloc[-1])
            brk = is_green_line_breakout(close=last_close, green_line=gl)
            typer.echo(f"{ticker}: current green line = {gl:.2f}; last close = {last_close:.2f}; breakout? {'YES' if brk else 'no'}")
    elif indicator == "stage":
        c = df["close"]
        typer.echo(f"{ticker}: Weinstein stage = {weekly_stage(c)}; 4>10>30 alignment? {'yes' if ma_alignment_4_10_30(c) else 'no'}; 10wk below 30wk? {'yes' if tenwk_below_thirtywk(c) else 'no'}")
    elif indicator == "wgb":
        wgbs = weekly_green_bars(df)
        stop = wgb_trailing_stop(df)
        last = wgbs.index[-1].date() if not wgbs.empty else None
        typer.echo(f"{ticker}: {len(wgbs)} weekly green bars; most recent = {last}; current WGB trailing stop = {stop}")
    elif indicator == "rwb":
        c = df["close"]
        typer.echo(f"{ticker}: {'weekly' if weekly else 'daily'} Guppy state = {rwb_state(c)}" + ("" if weekly else f"; Red Line Count = {red_line_count(c)}/6"))
    elif indicator == "qqq-timing":
        c = df["close"]
        typer.echo(f"{ticker}: short-term trend ≈ {short_term_trend(c)} (Day {trend_day_count(c)}) — APPROXIMATION via 30-day SMA; Dr. Wish's exact rule is unpublished.")


if __name__ == "__main__":  # pragma: no cover
    app()
