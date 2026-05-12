# CLAUDE.md — Wishing Wealth Wiki schema

This repo is an **LLM-maintained wiki** of Dr. Eric Wish's *Wishing Wealth Blog*
(`wishingwealthblog.com`) trading methodology, built on Andrej Karpathy's
[LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
This file is the **schema**: it tells you (Claude) how the wiki is structured and
exactly how to run the Ingest, Query, and Lint workflows. Read it at the start of
every session. Co-evolve it — when a convention changes, update this file.

Design rationale: `docs/specs/2026-05-11-wishing-wealth-wiki-design.md`.

## 1. The three layers — and the contract

- **Layer 1 — `raw/`** (source of truth, IMMUTABLE). Scraped blog posts as
  markdown (`raw/posts/<YYYY-MM-DD>-<slug>.md`, each with YAML front-matter
  `url`/`date`/`post_id`/`title`), plus `raw/posts.jsonl` (one `PostRecord` per
  post — see `src/ww/corpus/index.py`) and `raw/api/page-NNNN.json` (cached API
  responses). **You read from `raw/`; you never edit it.** Re-fetch with `ww scrape`.
- **Layer 2 — `wiki/`** (you own this entirely). Markdown pages — `overview.md`,
  `methodology/`, `playbooks/`, `history/`, `sources/`, plus `index.md` and
  `log.md`. You create pages, update them when new sources are processed, maintain
  cross-references, and keep everything consistent. A human reads `wiki/`; you write it.
- **Layer 3 — this file**. The schema/workflows. Disciplined maintainer, not chatbot.

## 2. Directory map & page taxonomy

- `wiki/index.md` — content catalog. Every wiki page listed, grouped by category
  (Overview / Methodology / Playbooks / History / Sources), each line:
  `- [Title](relative/path.md) — one-line summary` (optionally with metadata like
  `(updated 2026-05-11, 12 sources)`). **Read this FIRST when answering a query.**
  Update it on every Ingest and every filed Query answer.
- `wiki/log.md` — append-only, chronological. Every entry starts
  `## [YYYY-MM-DD] <ingest|query|lint|note> | <title>` so
  `grep "^## \[" wiki/log.md | tail` shows recent activity. This *is* the resume
  state — a fresh session reads the log tail + scans `raw/posts.jsonl` for
  `ingested == false` to know where things stand. Never rewrite history; only append.
- `wiki/overview.md` — the whole system on one page, links out to every component.
- `wiki/methodology/*.md` — **entity & concept pages**, one job each, ~200–800 words:
  - `gmi.md` — the General Market Index: its components, scoring (0–6), what each
    component signals, the GREEN/RED interpretation. Will embed literate code from
    `src/ww/indicators/gmi.py` once Plan 4 lands.
  - `t2108.md` — T2108 (% of stocks above their 40-day MA): definition, how he
    reads it, thresholds (overbought/oversold), how he uses it for timing.
  - `green-line-breakouts.md` — GLB: the all-time-high-held-≥3-months definition,
    why he trades them, the entry/stop mechanics, the "5-day EMA post-GLB" idea.
  - `qqq-short-term-timing.md` — the QQQ Short-Term Timing signal: the rule, what
    "Day N of QQQ short-term up/down-trend" means, how he counts days, how it ties
    to the GMI.
  - `moving-average-rules.md` — the 10-week / 30-week (and 4-week) MA stage rules;
    "the 10-week rule"; the 4wk>10wk>30wk alignment; weekly-close extension above MAs.
  - `stock-selection.md` — the fundamental + relative-strength overlay; the scans
    he runs; how he picks GLB candidates.
  - `risk-and-cash.md` — when to be in cash, drawdown discipline, "modified
    buy-and-hold", how the indicators tell him to exit before big declines.
  - `glossary.md` — every term he coins/uses, defined in one or two sentences, each
    with a first-appearance citation. Alphabetical.
- `wiki/playbooks/*.md` — decision procedures:
  - `market-state.md` — given GMI + QQQ-timing + T2108, what stance? (a decision tree).
  - `buying-glb.md` — the mechanical GLB entry checklist.
  - `exits.md` — how/when he sells; trailing rules.
- `wiki/history/*.md`:
  - `timeline.md` — how the methodology evolved year by year; inflection points
    (new indicators introduced, rules changed, lessons from 2008/2020/2022/etc.).
  - `track-record.md` — notable market calls + outcomes (built largely from the
    timeline dataset once Plan 2.5 produces `raw/timeline.parquet`).
- `wiki/sources/<YYYY-MM-DD>-<slug>.md` — one **summary page per ingested
  `teaching` or `trade_example` post**: what it teaches/demonstrates, the key
  claims, cited. (`daily_update` posts get no summary page — they feed
  `raw/timeline.parquet` and `history/`. `meta` posts are skipped.)
- `wiki/_templates/*.md` — page templates. **Not wiki pages** — `ww lint` ignores
  them. Copy from these when creating a new page.

When a page grows past ~800 words or starts doing two jobs, split it and link.

## 3. Page conventions

Every wiki page (NOT `index.md`, `log.md`, or `_templates/`) has:

1. **YAML front-matter:**
   ```yaml
   ---
   title: <page title>
   type: overview | entity | concept | playbook | history | source-summary
   updated: YYYY-MM-DD
   sources: [raw/posts/2014-03-12-....md, raw/posts/2015-08-01-....md]   # the posts this page draws from
   ---
   ```
   For a brand-new not-yet-populated page, add a status line right after the
   front-matter: `> **Status:** stub — populated during Ingest.` and leave `sources: []`.
2. **House style:** first-principles, plain language, no hype, no padding. Short.
   Heavily internally linked (`[T2108](t2108.md)`, `[market-state playbook](../playbooks/market-state.md)`).
   Define terms on first use or link to `glossary.md`. Prefer concrete rules and
   numbers over vibes — this is a methodology reference, not a fan post.
3. **Every non-obvious claim is cited.** Inline citation: `([WW 2014-03-12](../../raw/posts/2014-03-12-<slug>.md))`
   — the link text is `WW <post date>`, the target is the `raw/posts/...md` file
   (use the right number of `../` for the page's depth: methodology/playbooks/history
   pages are 2 deep → `../../raw/posts/...`; `sources/` pages are also 2 deep;
   `overview.md` is 1 deep → `../raw/posts/...`).
4. **Sources block** at the bottom — a `## Sources` heading followed by a bullet
   list of the posts the page draws from (each `- [WW YYYY-MM-DD — short title](../../raw/posts/...md)`),
   or the single line `_None yet._` if the page is a stub. `ww lint` requires the
   `## Sources` heading on every page. When a cited post has a `wiki/sources/<stem>.md`
   summary page, append a `([summary](../sources/<stem>.md))` link after the raw-post
   link on that same bullet — this is the **only** inbound link that prevents the
   source-summary page from being flagged as an orphan by `ww lint`.
5. **Literate-code pages** (the four indicator entity pages, once Plan 4 lands)
   embed runnable snippets from `src/ww/indicators/` in fenced ```python blocks and
   walk through them — code and prose together.

## 4. Operations

### Ingest
Posts are processed in **batches across many sessions** (there are ~4,655). Pick a
batch (work both oldest→newest and newest→oldest passes so methodology *evolution*
is visible); prefer `kind_guess == "long_form"` and `unknown` posts first (the
`daily_update` ones rarely teach anything new). For each post in the batch:
1. Read `raw/posts/<stem>.md`. Decide its `tier` (`teaching` / `trade_example` /
   `daily_update` / `meta`), write a one-line `summary`, list `indicators` and
   `tickers` referenced. Update that post's row in `raw/posts.jsonl` (use the
   helpers in `src/ww/corpus/index.py`; preserve all other rows).
2. If `tier` is `teaching` or `trade_example`: create `wiki/sources/<stem>.md` from
   `_templates/source-summary.md` — what it teaches/shows, key claims, cited; set
   that post's `summary_page` to `wiki/sources/<stem>.md`.
3. Update the affected `methodology/`, `playbooks/`, `history/timeline.md` pages —
   integrate the new information, revise summaries, **flag where it contradicts or
   refines an earlier claim** (don't silently overwrite — note "Earlier (2009) he
   said X; by 2015 this became Y"). Bump each touched page's `updated:` and add the
   post to its `sources:` front-matter and `## Sources` block.
4. Update `wiki/index.md` for any new/changed pages.
5. Append to `wiki/log.md`:
   `## [YYYY-MM-DD] ingest | <post date> <post title> — tier=<tier>; touched: <pages>`.
6. Set `ingested: true` on that post's row in `raw/posts.jsonl`.
For a batch of `daily_update` posts you needn't narrate each — set their tiers,
mark them ingested, and log the batch (`## [date] ingest | daily-updates <date1>..<dateN> — N posts, no new teaching`).
A human can also drop a brand-new post into `raw/` (the blog keeps publishing) and
ask for a single-source ingest — same steps.

### Query
1. Read `wiki/index.md`, open the relevant pages, and if needed run `ww search "..."`
   (Plan 5) to pull supporting passages from `wiki/sources/` and `raw/posts/`.
2. Answer **with citations** (links to wiki pages and `raw/posts/...md`). Pick the
   answer form that fits — paragraph, comparison table, checklist, chart.
3. **If the answer is durably useful** (a comparison, an analysis, a synthesised
   connection), file it into the wiki as a new page (usually under `methodology/` or
   `playbooks/`), update `index.md`, and append
   `## [YYYY-MM-DD] query | <question> — filed: <page>` to `wiki/log.md`.

### Lint
Run `ww lint .` (mechanical) and periodically do a **semantic** pass yourself:
- Mechanical (`ww lint`): broken internal links; pages missing a `## Sources`
  section; pages not catalogued in `index.md`; orphan pages (no inbound link from
  any other wiki page; `overview.md`/`index.md`/`log.md` exempt); `posts.jsonl`
  rows whose `summary_page` points at a missing file. Non-zero exit on errors. CI runs it.
- Semantic (you): contradictions between pages; stale claims a later post supersedes;
  important concepts referenced but lacking their own page; missing cross-references;
  thin pages that should merge or expand; follow-up questions/sources worth chasing.
  Produce a short report and append `## [YYYY-MM-DD] lint | <summary>` to `wiki/log.md`.

## 5. CLI quick reference

`ww scrape` — (re)build `raw/` from the blog's WordPress API.
`ww stats` — corpus + (later) wiki counts.
`ww lint .` — mechanical wiki integrity checks.
`ww timeline` — (Plan 2.5) build `raw/timeline.parquet` from `daily_update` posts.
`ww compute <indicator> <ticker>` — (Plan 4) run a literate indicator.
`ww search "..."` / `ww index` — (Plan 5) search the wiki + posts.

## 6. Resuming a session

1. `git log --oneline | head` and `grep "^## \[" wiki/log.md | tail -10` — what happened recently.
2. `ww stats` — how many posts, how many `ingested`.
3. Pick up the next Ingest batch (or whatever the human asks). Read THIS file again
   if it's been a while.
