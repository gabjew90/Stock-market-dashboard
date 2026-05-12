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
```

Re-running `ww scrape` is cheap — API pages are cached under `raw/api/` and posts
whose markdown file already exists are skipped (use `--force` to rewrite).

## Status

- **Plan 1** (raw-sources layer / scraper) — done. `ww scrape` mirrors the blog into `raw/`.
- **Plan 2** (wiki bootstrap) — done. `CLAUDE.md` schema + `wiki/` skeleton (stubs + templates) + `ww lint` + CI.
- **Plan 2.5** (timeline parser → `raw/timeline.parquet`) — not started.
- **Plan 3** (the Ingest loop) — machinery in place (`ww batch`, `update_records`); ingest is ongoing — the methodology pages fill in batch by batch. See `CLAUDE.md` §4 for the protocol.
- **Plans 4–5** (literate indicator code; search + Query loop) — not started.

The wiki structure and conventions live in [`CLAUDE.md`](CLAUDE.md).
