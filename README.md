# Wishing Wealth Wiki

An LLM-maintained wiki of Dr. Eric Wish's *Wishing Wealth Blog* (`wishingwealthblog.com`)
trading methodology, built on Andrej Karpathy's
[LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Design: `docs/specs/2026-05-11-wishing-wealth-wiki-design.md`.

## Setup

```bash
UV_LINK_MODE=copy uv sync   # UV_LINK_MODE=copy required on OneDrive; safe elsewhere too
```

## Usage

```bash
uv run ww scrape      # pull all public blog posts -> raw/posts/*.md + raw/posts.jsonl
uv run ww stats       # report corpus counts
uv run ww lint .      # mechanical wiki integrity checks
uv run ww batch -n 20 --kind long_form   # next un-ingested posts to ingest into the wiki
uv run ww compute green-line MSFT     # run a price-based indicator on a ticker
uv run ww compute stage QQQ
uv run ww compute gmi 2026-05-01      # partial GMI from current prices (breadth components flagged unavailable)
uv run ww compute gmi 2014-08-01 --demo   # full GMI against illustrative fixtures
uv run ww timeline           # parse his daily GMI/T2108/stance posts into raw/timeline.parquet
```

Re-running `ww scrape` is cheap — API pages are cached under `raw/api/` and posts
whose markdown file already exists are skipped (use `--force` to rewrite).

## Status

- **Plan 1** (raw-sources layer / scraper) — done. `ww scrape` mirrors the blog into `raw/`.
- **Plan 2** (wiki bootstrap) — done. `CLAUDE.md` schema + `wiki/` skeleton (stubs + templates) + `ww lint` + CI.
- **Plan 2.5** (timeline parser) — done: `ww timeline` builds `raw/timeline.parquet` (his published GMI / GMI-state / QQQ-day-count / T2108 / stance, parsed from the ~daily posts; low-confidence rows flagged); backs `history/track-record.md` and stands alone for charting/backtesting his signals.
- **Plan 3** (the Ingest loop) — machinery in place (`ww batch`, `update_records`); ingest is ongoing — the methodology pages fill in batch by batch. See `CLAUDE.md` §4 for the protocol.
- **Plan 4** (literate indicator code) — done for the price-based indicators: `src/ww/indicators/` (green_line, ma_stages, wgb, guppy/RWB-BWR-RLC, qqq_timing-approx) + `ww compute`; embedded in the methodology pages.
- **Plan 4b** (GMI / T2108) — done: `src/ww/indicators/gmi.py` (the 6-component composite — QQQ/SPY/QQQ-weekly trend computed from free prices; the breadth/fund components flagged unavailable) + `src/ww/indicators/t2108.py` (provider-delegated + a `t2108_from_prices` helper) + `--demo` mode; embedded in the methodology pages. Reproducing real historical GMI/T2108 needs a bulk-equity / breadth data feed (a later phase) — also the prerequisite for the planned strategy backtest (Plan 6).
- **Plan 5** (search + Query loop) — not started.
- **Plan 6** (backtest harness — the end goal) — not started; needs its own design. A backtest of the GLB/WGB/Stage-2/GMI strategy with realistic costs, walk-forward validation, a buy-and-hold benchmark, and parameter-tuning hooks.

The wiki structure and conventions live in [`CLAUDE.md`](CLAUDE.md).
