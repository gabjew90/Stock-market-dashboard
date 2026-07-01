# Stock market dashboard

Live site: **<https://seraphsys.us/>** (custom domain, Cloudflare) — also at
<https://gabjew90.github.io/Stock-market-dashboard/> (GitHub Pages).
Both are deployed from the same build; the Cloudflare copy is scrubbed of
anything linking it back to this repo — see
[`deploy/cloudflare/README.md`](deploy/cloudflare/README.md).

Three published pages, deployed nightly after the US close by the
[`build-dashboard`](.github/workflows/build-dashboard.yml) GitHub Actions workflow:

| Page | URL | Source |
|---|---|---|
| **Market Regime** | `/` | `scripts/build_market_regime.py` → `market_regime.html` |
| **Research** | `/pulse/` | static `web/pulse.html` (fetches a daily pulse from [Institutional-report-bot](https://github.com/gabjew90/Institutional-report-bot) at runtime — see [`PULSE-INTEGRATION.md`](PULSE-INTEGRATION.md)) |
| **About** | `/wiki.html` | `scripts/build_wiki_html.py` over `wiki/**` |

The repo doubles as the LLM-maintained wiki of Dr. Eric Wish's *Wishing Wealth Blog*
(`wishingwealthblog.com`) trading methodology — built on Andrej Karpathy's
[LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
The published "About" page is that wiki; the published "Market Regime" page is a
single-day deep-dive built from the same indicator code (`src/ww/indicators/`)
and a reconstructed breadth panel (`data/breadth/`).

The wiki structure and conventions live in [`CLAUDE.md`](CLAUDE.md).

## What "Market Regime" shows

The single-day deep-dive page renders, all referenced to a selectable date:

- A 6-month QQQ candle chart with volume bars (daily) or a 1-year weekly-Friday
  view, with the 30-day / 10-week / 30-week SMAs overlaid and a draggable
  selected-date marker. Value pills (price, MAs, volume) update live as the
  marker moves.
- "GMI" and "T2108" hero cards (Dr. Wish's headline market-health composite +
  the NYSE-breadth gauge), with a GREEN / YELLOW / RED gate state and the
  individual 6 GMI components broken out.
- "Day N of QQQ short-term trend" + Weinstein stage tag, plus the "Since
  Day 1" performance strip (QQQ, TQQQ, SQQQ) so the leveraged-ETF magnitudes
  are visible on the same row as the underlying.
- A jump menu of every past short-term trend that lasted ≥ 30 trading days,
  so historical regimes are one tap away.

Every chart, button, and label has a tooltip (`?` button) explaining what it
is and how it's computed.

## Setup

```bash
UV_LINK_MODE=copy uv sync   # UV_LINK_MODE=copy required on OneDrive; safe elsewhere too
```

## CLI

```bash
uv run ww scrape      # pull all public blog posts -> raw/posts/*.md + raw/posts.jsonl
uv run ww stats       # report corpus counts
uv run ww lint .      # mechanical wiki integrity checks
uv run ww timeline    # parse his daily GMI/T2108/stance posts into raw/timeline.parquet
uv run ww batch -n 20 --kind long_form   # next un-ingested posts to ingest into the wiki

uv run ww compute green-line MSFT     # run a price-based indicator on a ticker
uv run ww compute stage QQQ
uv run ww compute gmi 2026-05-01      # partial GMI from current prices (breadth components flagged unavailable)
uv run ww compute gmi 2026-05-01 --breadth   # full 0-6 GMI from the local breadth series

uv run ww breadth fetch        # build the common-stock universe + download the daily price panel (~20-40 min, once)
uv run ww breadth build        # compute data/breadth/breadth_series.parquet (T2108-equiv, new-highs, growth-fund proxy)
uv run ww breadth show         # print today's breadth snapshot
uv run ww breadth update       # incremental daily refresh
uv run ww breadth validate     # cross-check reconstructed T2108/GMI vs his reported numbers -> data/breadth/validate.json

uv run ww gmi today            # refresh the panel + print today's full GMI breakdown
uv run ww backtest timing-overlay   # backtest "long QQQ when GMI-GREEN / cash when RED" vs buy-and-hold QQQ

uv run ww index                       # build the local search index
uv run ww search "green line breakout"   # ranked, cited passages from the wiki + posts
```

Re-running `ww scrape` is cheap — API pages are cached under `raw/api/` and posts
whose markdown file already exists are skipped (use `--force` to rewrite).

## How the live site updates

The `build-dashboard` workflow fires:

- on every weekday at 22:00 UTC (≈ 5–6 PM ET, after the close), via cron
- on every push to `main` that touches the build script, wiki HTML
  builder, wiki content, raw posts, the pulse page, or the workflow itself
- on demand from the Actions tab

It restores a cached breadth + OHLC panel, runs `ww breadth update` for the
delta, rebuilds the Market Regime HTML and the wiki HTML, stages both plus
`web/pulse.html` into `_site/`, and deploys via Pages. First-run bootstrap
(`ww breadth fetch && ww breadth build`) only fires when the cache is empty.

After the Pages deploy, the same `_site/` is scrubbed by
`scripts/scrub_site_for_cf.py` (relative nav links, same-origin pulse URLs,
no identifying strings — enforced by a fail-the-build leak gate) and
deployed a second time to **`https://seraphsys.us/`** via Cloudflare Workers.
Requires the `CLOUDFLARE_API_TOKEN` repository secret. Architecture, wiring,
and troubleshooting: [`deploy/cloudflare/README.md`](deploy/cloudflare/README.md).

A companion [`monthly-breadth-refresh`](.github/workflows/monthly-breadth-refresh.yml)
workflow fires on the 1st of each month at 06:00 UTC. It runs the heavier
`ww breadth fetch --refresh-symbols` to re-download the Nasdaq Trader
symbol files, rebuild the common-stock universe (picks up new listings,
drops delistings), fetch full history for any new ticker, and recompute the
breadth series. The next build-dashboard run after the refresh picks up
the updated cache automatically.

The price cache (`data/backtest/prices.parquet`) self-validates: each ticker
must have ≥ 5 non-NaN values in its most recent 60 trading days, otherwise
`_ensure_prices` refetches via yfinance with a per-ticker fallback. This is
the safety net for transient yfinance hiccups that would otherwise pin a
broken column in the cache.

## Reading the wiki locally

Browse: open [`wiki/overview.md`](wiki/overview.md) and click through, or render
the whole thing with `uv run --with markdown python scripts/build_wiki_html.py`
(produces `wiki_site.html`).

Search: `ww index` once, then `ww search "..."` for ranked, cited passages
across the wiki and the raw posts. Paste the results into Claude (Code or a
Desktop project that has this repo) for a synthesised, cited answer — and if
the answer is durably useful, Claude files it back into the wiki as a new
page (see [`CLAUDE.md`](CLAUDE.md) §4 "Query").

## Status

Plans 1–5 + B1 + B2 complete. Corpus current state (from `ww stats` —
4,655 total posts spanning 2005-04 → 2026-05): 4,449 daily-update posts
parsed into `raw/timeline.parquet`; 86 teaching + 5 trade-example posts
tier-classified for wiki ingest; 18 meta + 97 unclassified. Remaining: Plan 6.

- **Plan 1** (raw-sources layer / scraper) — done. `ww scrape` mirrors the blog into `raw/`.
- **Plan 2** (wiki bootstrap) — done. Schema in `CLAUDE.md` + `wiki/` skeleton + `ww lint` + CI.
- **Plan 2.5** (timeline parser) — done. `ww timeline` → `raw/timeline.parquet`; low-confidence rows flagged.
- **Plan 3** (Ingest loop) — corpus tier-classified (see counts above). Queue and Ingest protocol documented in [`CLAUDE.md`](CLAUDE.md) §6.
- **Plan 4** (literate indicator code) — done. `src/ww/indicators/` (green_line, ma_stages, wgb, guppy/RWB-BWR-RLC, qqq_timing-approx) + `ww compute`, embedded in the methodology pages.
- **Plan 4b** (GMI / T2108) — done. `src/ww/indicators/gmi.py` (six-component composite) + `src/ww/indicators/t2108.py` + `--demo` mode; embedded in the methodology pages.
- **Plan 5** (search + Query loop) — done. `ww index` / `ww search` (local BM25 over wiki + posts); Query workflow in `CLAUDE.md` §4.
- **Plan B1 + B2** (breadth pipeline) — done. `ww breadth fetch/build/update/show/validate` → `data/breadth/breadth_series.parquet`; `BreadthProvider` → `ww compute gmi/t2108 --breadth` returns real numbers; `ww gmi today` gives a live daily reading. Validation lives in `data/breadth/validate.json` and is summarised in `wiki/methodology/gmi.md`. Documented survivorship / universe / proxy limitations.
- **Plan 6** (backtest harness — the end goal) — not started. Will need its own design: realistic costs, walk-forward validation, a buy-and-hold benchmark, and parameter-tuning hooks.

An early scaffolding pass at the market-state timing overlay
(`ww backtest timing-overlay`) exists and writes its result to
`wiki/methodology/backtest-timing-overlay.md`. That page is intentionally
**not** rendered on the live About page yet — `scripts/build_wiki_html.py`
skips it via `_SKIP_PAGES` until Plan 6's harness is in place. Re-publishing
the backtest is gated on Plan 6.
