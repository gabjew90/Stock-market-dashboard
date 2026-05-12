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
```

Re-running `ww scrape` is cheap — API pages are cached under `raw/api/` and posts
whose markdown file already exists are skipped (use `--force` to rewrite).

## Status

Plan 1 (raw-sources layer / scraper) — complete. 4,655 posts scraped (2005-04-17 to 2026-05-11).
Plans 2–5 build the wiki, the `CLAUDE.md` schema, the Ingest/Query/Lint loops, literate indicator code, and search.
