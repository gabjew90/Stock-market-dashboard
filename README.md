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
uv run ww index                       # build the local search index
uv run ww search "green line breakout" # ranked, cited passages from the wiki + posts
uv run ww breadth fetch        # build the common-stock universe + download the daily price panel (~20-40 min, once)
uv run ww breadth build        # compute data/breadth/breadth_series.parquet (T2108-equiv, new-highs, ...) + the growth-fund proxy
uv run ww breadth show         # print today's breadth snapshot
uv run ww breadth update       # incremental daily refresh (pull recent bars, recompute the tail)
uv run ww breadth validate     # cross-check the reconstructed T2108/GMI vs his reported numbers -> data/breadth/validate.json
uv run ww compute gmi 2026-05-11 --breadth   # a full 0-6 GMI from the local breadth series
uv run ww gmi today            # nightly: refresh the panel, then print today's full GMI breakdown
```

Re-running `ww scrape` is cheap — API pages are cached under `raw/api/` and posts
whose markdown file already exists are skipped (use `--force` to rewrite).

## Daily GMI

Once the breadth pipeline is built (`ww breadth fetch && ww breadth build` — done once, takes a while), a nightly cron of:

```bash
uv run ww breadth update && uv run ww gmi today
```

refreshes the breadth series and prints today's full 0–6 GMI (the three price-derived components from QQQ/SPY, the two breadth components from the reconstructed 52-week-high panel, the growth-fund-proxy component) with a GREEN/YELLOW/RED read. Re-run `ww breadth fetch --refresh-symbols` approximately monthly to pick up new listings / drop delisted ones. Fidelity caveats and the validation stats are in `wiki/methodology/gmi.md`.

## Reading & querying it

- Browse: open [`wiki/overview.md`](wiki/overview.md) and click through, or render the whole thing with `uv run --with markdown python scripts/build_wiki_html.py` (produces `wiki_site.html`).
- Search: `ww index` once, then `ww search "..."` for ranked, cited passages across the wiki and the raw posts. Paste the results into Claude (Code or a Desktop project that has this repo) to get a synthesised, cited answer — and if the answer is durably useful, Claude files it back into the wiki as a new page (see `CLAUDE.md` §4 "Query").

## Status

- **Breadth data** — done (Plans B1+B2): `ww breadth fetch/build/update/show/validate` → `data/breadth/breadth_series.parquet`; `BreadthProvider` → `ww compute gmi/t2108 --breadth` returns real numbers; `ww gmi today` gives a live daily reading; `ww breadth validate` records how well the reconstruction matches his reported T2108/GMI (see `data/breadth/validate.json` and `wiki/methodology/gmi.md`). Documented survivorship/universe/proxy limitations. Unblocks Plan 6 (the strategy backtest).
- **Status:** Plans 1–5 + B1 complete. Corpus fully tiered (31 teaching/example posts ingested with full wiki content; ~4,460 daily-update posts → raw/timeline.parquet; ~149 long_form teaching posts queued for future ingest passes). Remaining: Plan 6 (backtest harness — needs its own design).
- **Plan 1** (raw-sources layer / scraper) — done. `ww scrape` mirrors the blog into `raw/`.
- **Plan 2** (wiki bootstrap) — done. `CLAUDE.md` schema + `wiki/` skeleton (stubs + templates) + `ww lint` + CI.
- **Plan 2.5** (timeline parser) — done: `ww timeline` builds `raw/timeline.parquet` (his published GMI / GMI-state / QQQ-day-count / T2108 / stance, parsed from the ~daily posts; low-confidence rows flagged); backs `history/track-record.md` and stands alone for charting/backtesting his signals.
- **Plan 3** (the Ingest loop) — corpus fully tiered as of 2026-05-11 (every post has a tier). 31 teaching/trade_example posts fully ingested. ~149 long_form teaching posts queued for future passes. See `CLAUDE.md` §6 for the state and §4 for the protocol.
- **Plan 4** (literate indicator code) — done for the price-based indicators: `src/ww/indicators/` (green_line, ma_stages, wgb, guppy/RWB-BWR-RLC, qqq_timing-approx) + `ww compute`; embedded in the methodology pages.
- **Plan 4b** (GMI / T2108) — done: `src/ww/indicators/gmi.py` (the 6-component composite — QQQ/SPY/QQQ-weekly trend computed from free prices; the breadth/fund components flagged unavailable) + `src/ww/indicators/t2108.py` (provider-delegated + a `t2108_from_prices` helper) + `--demo` mode; embedded in the methodology pages. Reproducing real historical GMI/T2108 needs a bulk-equity / breadth data feed (a later phase) — also the prerequisite for the planned strategy backtest (Plan 6).
- **Plan 5** (search + Query loop) — done: `ww index` / `ww search` (local BM25 over wiki + posts, cited hits); the Query workflow is documented in `CLAUDE.md` §4.
- **Plan 6** (backtest harness — the end goal) — not started; needs its own design. A backtest of the GLB/WGB/Stage-2/GMI strategy with realistic costs, walk-forward validation, a buy-and-hold benchmark, and parameter-tuning hooks.

The wiki structure and conventions live in [`CLAUDE.md`](CLAUDE.md).
