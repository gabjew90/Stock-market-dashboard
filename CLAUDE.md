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
  responses). **You read from `raw/`; you never edit it** — except for the curated
  fields on a post's `posts.jsonl` row during Ingest (§4). Re-fetch with `ww scrape`.
  **`raw/posts/` and `raw/posts.jsonl` are committed** (since 2026-08-12): the wiki's
  ~1,250 citations link into them, `ww lint` can only verify those links when the corpus
  is present, and a session on a network that cannot reach `wishingwealthblog.com` can
  still ingest. `raw/api/` stays gitignored — it is a redundant JSON cache, re-fetchable
  with `ww scrape`. Also committed: `raw/url_map.json` (the slug→URL catalogue) and
  `raw/ingest-ledger.jsonl` (the curated tier/summary/`ingested` state, see §5), which
  survives a re-scrape that rewrites every other field. **A fresh checkout now has the
  full corpus** — no scrape needed before you can ingest or lint.
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
  - `stock-selection.md` — what he is looking for: launched rockets, the fundamental
    overlay, the price-level rule, the ATH watchlist. Its scan definitions live on
    `scans.md`; its daily-chart entry triggers (BOS, the dots, x8/x21/30) on `entry-signals.md`.
  - `oversold-bounce.md` — the OSB / ATHOSB doctrine: the entry he prefers to the breakout.
  - `risk-and-cash.md` — the trading-account doctrine: when to be in cash, stops, cutting
    losses. Split out of it (2026-08-18): `pension-management.md` (the two accounts, staged
    pension exit), `short-side.md` (submarine scan, hedging, options), `leveraged-etf-default.md`
    (TQQQ on a Buy signal), and `history/defensive-episodes.md` (worked case studies).
  - `gmi-family.md` (GMI-S/L/R/2 and the rest of the daily table) and `gmi-evidence.md`
    (verbatim table labels, signal record, audits) — split out of `gmi.md` 2026-08-18.
  - `backtest-timing-overlay.md`, `trading-philosophy.md`, `reader-qa.md` — analysis pages.
  - `glossary.md` — every term he coins/uses, defined in one or two sentences, each
    with a first-appearance citation. Alphabetical.
- `wiki/playbooks/*.md` — decision procedures:
  - `market-state.md` — given GMI + QQQ-timing + T2108, what stance? (a decision tree).
  - `buying-glb.md` — the mechanical GLB entry checklist.
  - `buying-osb.md` — the mechanical OSB entry checklist (the dot triggers tabulated).
  - `exits.md` — how/when he sells; the three trailing systems reconciled by date.
  Playbooks hold **procedure only** (~1,200 words); doctrine lives on the concept page (§4).
- `wiki/history/*.md`:
  - `timeline.md` — how the methodology evolved year by year; inflection points
    (new indicators introduced, rules changed, lessons from 2008/2020/2022/etc.).
    **Kept in strict chronological order by section heading** — insert new sections in place.
  - `defensive-episodes.md` — worked case studies of the defensive doctrine applied.
  - `trend-flip-log.md` — every documented QQQ short-term trend flip.
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
3b. **Reader comments** are cited differently. They are primary material but not posts, so they
   use the form `[WW comment YYYY-MM-DD]` + the live permalink, and are **not** listed in `## Sources` blocks
   (which catalogue posts only). Data: `raw/comments.jsonl` via `ww comments`; search with
   `ww search "..." --source comments`. Curated findings live in `wiki/methodology/reader-qa.md`.
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
3. Integrate the new information into the wiki — **one canonical page per fact, then
   links**. The 2026-08-18 audit found the same claim written out in full on 3–5 pages
   (GMI signal rules on gmi.md, market-state.md, exits.md, risk-and-cash.md, timeline.md),
   which is how the "two consecutive readings" fabrication and the "one quarter" drift
   propagated. So, for each new fact:
   - **Pick the one page that owns it** (the entity/concept page for a definition or rule;
     `history/timeline.md` for *when* it changed; a playbook only for the *procedure*).
     Write it there, cited, and **flag where it contradicts or refines an earlier claim**
     (don't silently overwrite — note "Earlier (2009) he said X; by 2015 this became Y").
   - Every other page that needs it gets a one-line pointer (`see [GMI signals](gmi.md#signals)`),
     not a re-statement. A playbook step may restate a rule in ≤1 sentence *with the same
     citation* — never a paraphrase from memory.
   - **Playbooks have a word budget (~1,200)** and hold procedure only. Doctrine, history,
     worked examples and quotes belong on the concept page the playbook links to. If a
     playbook step needs more than a sentence of justification, that justification lives
     on the concept page.
   Bump each touched page's `updated:` and add the post to its `sources:` front-matter
   **and** its `## Sources` block (`ww lint` errors if the two disagree).
4. Update `wiki/index.md` for any new/changed pages.
5. Append to `wiki/log.md`:
   `## [YYYY-MM-DD] ingest | <post date> <post title> — tier=<tier>; touched: <pages>`.
6. Set `ingested: true` on that post's row in `raw/posts.jsonl`.
7. At the end of the batch, run `ww ledger export` and commit `raw/ingest-ledger.jsonl`
   alongside `raw/posts.jsonl` and the wiki changes. Both are committed, but the ledger
   diffs readably and survives a re-scrape that rewrites every other field.
For a batch of `daily_update` posts you needn't narrate each — set their tiers,
mark them ingested, and log the batch (`## [date] ingest | daily-updates <date1>..<dateN> — N posts, no new teaching`).
A human can also drop a brand-new post into `raw/` (the blog keeps publishing) and
ask for a single-source ingest — same steps.

### Query
1. Read `wiki/index.md`, open the relevant pages, and if needed run `ww search "..."`
   to pull supporting passages from `wiki/sources/` and `raw/posts/`.
2. Answer **with citations** (links to wiki pages and `raw/posts/...md`). Pick the
   answer form that fits — paragraph, comparison table, checklist, chart.
3. **If the answer is durably useful** (a comparison, an analysis, a synthesised
   connection), file it into the wiki as a new page (usually under `methodology/` or
   `playbooks/`), update `index.md`, and append
   `## [YYYY-MM-DD] query | <question> — filed: <page>` to `wiki/log.md`.

### Lint
Run `ww lint .` (mechanical) and periodically do a **semantic** pass yourself:
- Mechanical (`ww lint`): broken internal links — including the ~1,250 citations into
  `raw/posts/`, which are verified now that the corpus is committed (a checkout missing
  `raw/posts/` skips them with a warning instead); pages missing a `## Sources`
  section; **posts cited in a page's body but not listed in that page's `## Sources` block**;
  pages not catalogued in `index.md`; orphan pages (no inbound link from
  any other wiki page; `overview.md`/`index.md`/`log.md` exempt); `posts.jsonl` **and
  `ingest-ledger.jsonl`** rows whose `summary_page` points at a missing file;
  **front-matter present with `title`/`type`/`updated` (ISO date)/`sources`, and the
  front-matter `sources:` list agreeing both ways with the `## Sources` block**;
  **leaked tool markup** (a bare `</content>`-style closing tag on its own line) in any
  wiki page or `.py` file under `src/`/`tests/`.
  Non-zero exit on errors. CI runs it.
- Semantic (you): contradictions between pages; stale claims a later post supersedes;
  important concepts referenced but lacking their own page; missing cross-references;
  thin pages that should merge or expand; follow-up questions/sources worth chasing.
  Produce a short report and append `## [YYYY-MM-DD] lint | <summary>` to `wiki/log.md`.

## 5. CLI quick reference

`ww scrape` — (re)build `raw/` from the blog's WordPress API. Captures his own
`categories`/`tags` onto each `PostRecord` (see `raw/categories.json`).
`ww comments` — pull all 4,136 reader comments into `raw/comments.jsonl` (committed;
the page cache `raw/api-comments/` is not). The threads carry rule clarifications that
appear nowhere in the post bodies — 678 of the comments are Dr. Wish replying.
`ww batch --category "My Favorite Posts"` — **the primary ingest queue**: his own curation
of what matters most (145 posts). Also `Tutorial`, `UMDSMC Education Posts`, `Nicolas Darvas`.
`ww ledger export` — write the curated post state (tier/summary/ingested/summary_page) to `raw/ingest-ledger.jsonl`. **Run this after every Ingest batch and commit the result** alongside `raw/posts.jsonl`.
`ww ledger apply` — restore that state onto a freshly-scraped `raw/posts.jsonl`.
`ww ledger rebuild` — recovery path: reconstruct the ledger from `wiki/sources/*.md` if the ledger is lost too (recovers ingested teaching/trade_example rows only).
`ww tier` — bulk-tier un-ingested **routine** market notes as `daily_update`, *holding* anything that
might teach (a first-person rule statement in the body, a long body, or `kind_guess == long_form`).
Held posts are left untiered and un-ingested so the queue stays a real prioritised list. Dry-run by
default; `--apply` writes, then run `ww ledger export`. Logic and thresholds: `src/ww/corpus/tiering.py`.
`ww stats` — corpus + (later) wiki counts.
`ww lint .` — mechanical wiki integrity checks.
`ww timeline` — (Plan 2.5) build `raw/timeline.parquet` from `daily_update` posts.
`ww compute <indicator> <ticker>` — (Plan 4) run a literate indicator.
`ww index` — (re)build the local BM25 search index (wiki + posts -> `data/index/wiki.pkl`).
`ww search "..."` — ranked, cited passages from the wiki + posts (use these when answering a query — see §4 Query).

## 6. Resuming a session

0. **Check the corpus is there.** `ls raw/posts | wc -l` should print ~4,700 — the corpus
   is committed, so a normal checkout already has it and no scrape is needed. Only re-scrape
   to pull posts published since the last one (`ww scrape && ww ledger apply`, then commit
   both `raw/posts/` and the ledger). That needs outbound access to `wishingwealthblog.com`;
   some sandboxes (Claude Code on the web, CI) allow GitHub only, and there the blog is
   unreachable — say so rather than working around it. Everything else still works.
1. `git log --oneline | head` and `grep "^## \[" wiki/log.md | tail -10` — what happened recently.
2. `ww stats` — how many posts, how many `ingested`. `ls wiki/sources | wc -l` and
   `wc -l raw/ingest-ledger.jsonl` should agree with the `ingested` count.
3. Pick up the next Ingest batch (or whatever the human asks). Read THIS file again
   if it's been a while.

**Corpus state as of 2026-08-26:** 4,700 posts (2005-04-17 → 2026-08-23), re-scraped and
**committed** — `raw/posts/` and `raw/posts.jsonl` are in version control (see §1).
`raw/url_map.json` still catalogues slug→URL.

**A scraper bug that silently dropped posts — fixed 2026-08-26, worth knowing about.** `ww scrape`
paginated the WordPress API **newest-first** while caching pages 2+ to `raw/api/`. Publishing K new
posts shifted every offset by K, so the K posts that had been at the tail of a cached page slid
across the boundary and were never re-fetched — they vanished from `raw/posts.jsonl` while their
`raw/posts/*.md` files stayed on disk (which is why `ww lint` never noticed: citations resolve to
files). Six posts from 2025-11-27 → 2025-12-07 were lost this way, one of them a `teaching` post
cited on three wiki pages. `wp_api.py` now paginates **oldest-first** (`order=asc`), so new posts
append and every earlier offset is stable; only the final short page is left uncached. Three tests
in `tests/test_wp_api.py` pin this, including a scrape → publish → re-scrape regression.
**If you ever see `ls raw/posts | wc -l` exceed the `posts.jsonl` row count, that is this class of
bug** — compare the two sets before assuming a post was deleted upstream, and check the live URL.

**The corpus is fully ingested as of 2026-08-26: 4,700 / 4,700, queue empty.** By tier:
**477 `teaching` / `trade_example`** posts (455 + 22), each with a summary page under
`wiki/sources/`; **4,222 `daily_update`**; **1 `meta`**. Of the daily updates, ~3,900 were screened by `ww tier`
(each carrying a `[bulk-tiered]` summary saying why) and ~300 were **read individually** during the
2026-08-26 tail sweep and judged routine — those carry a `[read in the … tail sweep]` summary
distinguishing "read and found routine" from "screened without reading". Run
`uv run ww ledger export` after any future batch and commit the ledger alongside `posts.jsonl`.

**Nothing is queued.** The 448 posts `ww tier` had held were worked through in fifteen batches
between 2026-08-18 and 2026-08-26 (see `wiki/log.md`), in descending order of body length. The
teaching yield fell monotonically as the queue drained — ~60% in the long-body tier, ~30% in the
first half of the single-marker tail, 15% in the next chunk, ~10% in the last — which is the
expected shape and is why the final chunks produced more `daily_update` rows than pages. **Not every
post earns a source page**: a routine note that corroborates documented doctrine is tiered
`daily_update` with a summary saying so (CLAUDE.md §4 provides for this), and manufacturing a page
for it would be padding.

**If new posts arrive** (the blog is still publishing), `ww scrape && ww ledger apply` picks them up
and they will appear as `ingested == false`; ingest them singly per §4. Two tooling notes for that
work: `scratchpad/tl.py` in a session's scratchpad resolves timeline insertion **by date** rather
than by a hand-picked anchor heading — anchor-not-found was the failure that broke nearly every
batch before it existed — and it wires the page's `## Sources` block itself. Write batch scripts with
the Write tool rather than shell heredocs; heredocs mangle escapes and quote characters repeatedly.

**Known coverage gaps** (full list in the 2026-08-12 lint entry in `wiki/log.md`). *Closed
2026-08-12:* **OSB / ATHOSB** (now `methodology/oversold-bounce.md`), the **2021 $200 revision**
(flagged as a supersession in `stock-selection.md`), **2007** (7 source pages + a consolidated
timeline section), and the **GMI component 6** question — it was never replaced; it is still the
IBD Growth Mutual Fund index (`0muti`) above its 50-day average, confirmed 2008/2009/2023/2025.
2007 also yielded two previously undocumented indicators, **GMI-L** and the **GMI-S construction**.
*Closed 2026-08-18:* the **short-side** page (`methodology/short-side.md`); the GMI component
*labels* (read off four table images 2007/2013/2020/2026 — see `methodology/gmi-evidence.md`).
*Closed 2026-08-18 (evening):* **2015** and **2019** (now 7 source pages each — the pension
self-correction, the GMMA top signature, the flash-crash ETF lesson, the green-dot procedure, the
successful-10-day-new-low mirror, the too-easy sell) and **trading psychology**
(`methodology/trading-psychology.md`); the **hourly GMMA** (three 2022 posts folded into
`moving-average-rules.md#the-hourly-layer`); **position sizing** — closed as a documented *absence*:
he told readers "I have no specific rules for that" (comment 2014-05-31) and the stand-in habits are
collected on `risk-and-cash.md#position-sizing`. *Still open:* the **off-blog teaching corpus**
(~63 posts pointing at Worden webinars, AAII, TraderLion, TASC, YouTube); the **Twitter alert
channel** (touched only via 2019-11-24). Historically, components 1, 2 and 6 were
confirmed verbally at multiple dates, and 3–5 rested on the 2005 definition plus 2007/2012
corroboration.
