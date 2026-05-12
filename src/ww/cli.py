"""`ww` command-line interface."""
from __future__ import annotations

from pathlib import Path

import typer
import yaml

from ww.corpus.index import read_posts_jsonl
from ww.corpus.timeline import build_timeline
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
def timeline(
    root: Path = typer.Option(Path("."), "--root", help="Repo root."),
) -> None:
    """Parse the daily-update posts into raw/timeline.parquet (his published GMI/T2108/stance signals over time)."""
    df = build_timeline(root)
    out = Path(root) / "raw" / "timeline.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    n = len(df)
    flagged = int((df["parse_confidence"] == "flagged").sum()) if n else 0
    span = f"{df['date'].min().date()}..{df['date'].max().date()}" if n else "(empty)"
    typer.echo(f"timeline: {n} daily-update rows {span} ({n - flagged} high-confidence, {flagged} flagged) -> {out}")


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
    indicator: str = typer.Argument(..., help="green-line | stage | wgb | rwb | qqq-timing | gmi | t2108"),
    ticker: str = typer.Argument(..., help="Ticker symbol — or a date (YYYY-MM-DD) for gmi/t2108."),
    csv: Path = typer.Option(None, "--csv", help="Read OHLC from this CSV (date index + open,high,low,close) instead of yfinance."),
    weekly: bool = typer.Option(False, "--weekly", help="For 'rwb': use the weekly Guppy instead of the daily one."),
    demo: bool = typer.Option(False, "--demo", help="For gmi/t2108: use illustrative built-in fixtures (not real data)."),
) -> None:
    """Run one of Dr. Wish's runnable price-based indicators on a ticker (see wiki/methodology/*.md)."""
    import pandas as pd
    from ww.indicators import (
        current_green_line, is_green_line_breakout, weekly_stage, ma_alignment_4_10_30,
        tenwk_below_thirtywk, weekly_green_bars, wgb_trailing_stop, rwb_state, red_line_count,
        short_term_trend, trend_day_count, YFinanceProvider,
    )

    if indicator in ("gmi", "t2108"):
        from ww.indicators import gmi as _gmi, t2108 as _t2108
        from ww.indicators.provider import DataUnavailable, YFinanceProvider as _YFP
        if indicator == "gmi":
            if demo:
                from ww.indicators._demo import DEMO_DATE, demo_provider
                r = _gmi(demo_provider(), DEMO_DATE)
                typer.echo(f"GMI (DEMO — illustrative fixtures, not real data): score = {r.score}/6")
                for k, v in r.components.items():
                    typer.echo(f"  {'+' if v else ('?' if v is None else '-')} {k}")
            else:
                prov = _YFP()
                r = _gmi(prov, ticker)
                avail = 6 - len(r.unavailable)
                typer.echo(f"GMI on {ticker}: partial score = {r.score} (of {avail} computable components; {len(r.unavailable)} need breadth/fund data — see wiki/methodology/gmi.md)")
                for k, v in r.components.items():
                    typer.echo(f"  {'+' if v is True else ('?' if v is None else '-')} {k}" + (" (unavailable)" if v is None else ""))
        else:  # t2108
            if demo:
                from ww.indicators._demo import DEMO_DATE, demo_provider
                val = _t2108(demo_provider(), DEMO_DATE, universe=("AAA", "BBB", "CCC"), window=40)
                typer.echo(f"T2108 (DEMO — illustrative fixtures, not real data) = {val:.2f}%")
            else:
                typer.echo("T2108 needs the full NYSE universe (% of stocks above their 40-day MA) — not available from free sources. "
                           "See wiki/methodology/t2108.md for the formula, or use ww.indicators.t2108_from_prices({ticker: ohlc_df, ...}, date) with your own data.")
        return

    # interval each indicator wants
    interval = {"green-line": "1mo", "stage": "1wk", "wgb": "1wk", "rwb": ("1wk" if weekly else "1d"), "qqq-timing": "1d"}.get(indicator)
    if interval is None:
        typer.echo(f"unknown indicator '{indicator}'. Choose: green-line, stage, wgb, rwb, qqq-timing, gmi, t2108")
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
