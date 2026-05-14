# Pulse integration (`/pulse/`)

The `/pulse/` page on this site embeds the **Daily Market Pulse** from a separate
project at <https://github.com/gabjew90/Institutional-report-bot>.

If you're looking at `web/pulse.html` or the new "Daily Pulse" link in the
`.pages-nav` of `scripts/build_gmi_playground.py` and wondering "what is this,"
this doc is for you.

---

## Architecture in one paragraph

The pulse content is **fetched at runtime** by the browser, not at build time
here. `web/pulse.html` is a fully self-contained static page (inline CSS,
inline JS, hardcoded data URLs) that this site copies into
`_site/pulse/index.html` during the existing GitHub Pages workflow. When a
visitor loads the page, the inline JS issues a fetch to
`https://raw.githack.com/gabjew90/Institutional-report-bot/pulse-data/pulse-output/web/archive.json`,
filters to the current ISO week, and pulls each pulse's HTML fragment from
`https://raw.githack.com/gabjew90/Institutional-report-bot/pulse-data/pulse-output/web/fragments/<ts>.html`.
This site never builds the pulse HTML itself; the **pulse pipeline lives in the
other repo** and publishes per-pulse HTML fragments + an `archive.json` index
that the page consumes.

---

## What the integration actually changes here

Three files (plus this doc):

1. **`web/pulse.html`** *(new)*
   The daily-pulse page. Dark theme matching the GMI dashboard (same `--bg`,
   `--accent`, `--mono`, etc. CSS tokens). Uses the same `.pages-nav` sticky
   brand bar so the top of every page on the site is identical. Renders the
   **current ISO week** of pulses, newest on top, with `← Previous week` /
   `Next week →` buttons for pagination. Each rendered pulse comes from a
   per-`<ts>.html` fragment on the pulse-data branch.

2. **`scripts/build_gmi_playground.py`** *(modified — 1 line)*
   Added a `<a href="./pulse/">Daily Pulse</a>` link to the existing
   `.pages-nav` block, positioned between "GMI Daily" and "Methodology". No
   other change to the GMI rendering.

3. **`.github/workflows/daily-gmi.yml`** *(modified — 2 hunks)*
   - Added `web/pulse.html` to the `paths` filter so future edits to the pulse
     page also trigger a redeploy.
   - Added two new lines to the "Stage site" step that copy `web/pulse.html`
     to `_site/pulse/index.html` (the trailing-slash URL works because Pages
     serves `pulse/index.html` as `/pulse/`). Wiki/assets staging untouched.

---

## URLs in play

| URL | What | Owned by |
|---|---|---|
| `https://gabjew90.github.io/Stock-market-dashboard/` | GMI Components index | This repo |
| `https://gabjew90.github.io/Stock-market-dashboard/wiki.html` | Methodology wiki | This repo |
| `https://gabjew90.github.io/Stock-market-dashboard/pulse/` | Daily Pulse | This repo (static `web/pulse.html`) |
| `https://raw.githack.com/gabjew90/Institutional-report-bot/pulse-data/pulse-output/web/archive.json` | Index of available pulses (title, date, fragment_url per entry) | Other repo (auto-published by its bridge worker) |
| `https://raw.githack.com/gabjew90/Institutional-report-bot/pulse-data/pulse-output/web/fragments/<ts>.html` | Individual pulse content as headless HTML | Other repo |

`raw.githack.com` is a CDN proxy in front of `raw.githubusercontent.com` that
serves files with the correct `text/html` content-type and CDN-caches. Without
it, browsers would render the HTML files as `text/plain`.

---

## Backfill policy (only the latest pulse is renderable)

The other repo's pipeline only generates HTML fragments for the **newest**
pulse, not the full archive. Entries in `archive.json` for older pulses appear
as minimal stubs (`{ts, filename, archive_url}` only, no `fragment_url`). The
weekly view filters out stubs, so:

- **Day 1 of deploy:** the current week shows only the single most recent
  pulse. Other weekdays in the current week appear empty even if pulses fired
  before this integration was wired up.
- **Going forward:** every new weekday pulse adds a fragment, and the current
  week's view fills in day by day.
- **Previous week:** empty until enough new pulses accumulate to populate
  a full week of fragments. The "← Previous week" button stays disabled
  until there's history to navigate to.

To manually backfill historical fragments, run a one-shot script in the
Institutional-report-bot repo (none exists yet — ask if you want one).

---

## When you'd touch this

**Visual tweaks** (colors, fonts, layout of the pulse page) → edit the
`<style>` block at the top of `web/pulse.html`. The class names targeting the
fetched fragment content (`.pulse h2.recap`, `.pulse .cashtag`, etc.) are a
**stable contract** with the other repo's pulse pipeline — change the styles,
not the class names.

**Reorder or rename the top nav chips** → edit the `<nav class="pages-nav">`
block in `web/pulse.html` AND in the `TEMPLATE` string of
`scripts/build_gmi_playground.py`. They have to stay in sync visually — both
pages share the same brand bar.

**Change which pulse pipeline this points at** → edit the `REPO` / `BRANCH`
constants in the inline `<script>` block near the bottom of `web/pulse.html`.

**Pulse page broken / showing "Couldn't load archive"** → check
<https://github.com/gabjew90/Institutional-report-bot> bridge worker logs.
The pipeline publishes to the `pulse-data` branch via a Railway worker; if the
worker is down, no new fragments land.

---

## When you would NOT touch this

The pulse content itself is **not** generated by anything in this repo. The
Python files in `scripts/` are all GMI-related; none of them know about the
pulse. If you want to change the pulse's wording, voice, content selection,
QC criteria, etc., that all happens in the other repo
(`Institutional-report-bot`). This site just renders what the other pipeline
publishes.

---

## Coupling notes (for the agent / maintainer)

The integration is **loose at runtime**: this repo has no compile-time, build-
time, or workflow-time dependency on the other one. The two repos communicate
only via the public URL contract above. Practical implications:

- Either repo can deploy independently. A push here doesn't trigger anything
  there, and vice versa.
- If the other repo's URL pattern ever changes (rename the branch from
  `pulse-data`, restructure `pulse-output/web/`, etc.), this page breaks
  silently — the user sees "Couldn't load archive" on `/pulse/`. Don't break
  the contract on the other side without coordinating.
- Repo visibility matters. `raw.githack.com` only proxies public repos. If
  `Institutional-report-bot` is ever made private, the pulse page stops
  working until either (a) the other repo goes back to public, or (b) the
  embed switches to a host that supports authenticated fetch (Cloudflare
  Worker, Vercel function, etc.).
