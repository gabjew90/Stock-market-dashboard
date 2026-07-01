# Cloudflare deployment (`seraphsys.us`)

The dashboard publishes to **two** places from the same nightly build:

| Target | URL | Serves |
|---|---|---|
| GitHub Pages | `https://gabjew90.github.io/Stock-market-dashboard/` | the staged `_site/` as-built |
| Cloudflare Workers | `https://seraphsys.us/` | the same `_site/`, **scrubbed** (see below), behind a custom domain |

Same content, one deliberate difference: the Cloudflare copy is stripped of
every string that ties it back to this GitHub account. The custom domain and
the repo are meant to be **unlinkable from the visitor's side** — no
`gabjew90` in the HTML, no `github.io` nav links, and no browser fetches to
`raw.githubusercontent.com` (the pulse data is proxied server-side instead).

---

## How a deploy flows

Both deploys happen at the end of the
[`build-dashboard`](../../.github/workflows/build-dashboard.yml) workflow,
in this order:

1. `_site/` is staged as always (Market Regime → `index.html` + `gmi.html`,
   wiki → `wiki.html`, `web/pulse.html` → `pulse/index.html`, plus `assets/`).
2. **GitHub Pages** deploys first (`upload-pages-artifact` + `deploy-pages`)
   — it gets the unscrubbed copy.
3. **`scripts/scrub_site_for_cf.py _site`** then rewrites `_site/` in place:
   - absolute `https://gabjew90.github.io/Stock-market-dashboard/...` nav
     links → relative `./` paths;
   - the pulse page's hardcoded `raw.githubusercontent.com` archive/fragment
     URLs → same-origin `/pulse-data/...` paths (served by the Worker proxy);
   - comments naming the upstream repo/hosts → neutral wording.

   It ends with a **leak gate**: every file in `_site/` is scanned for
   `gabjew90`, `Institutional-report`, `github`, `githack`, `jsdelivr` — any
   hit exits non-zero and **fails the build** before anything reaches
   Cloudflare. A leak can annoy the build; it cannot ship.
4. **`wrangler deploy`** (via `cloudflare/wrangler-action`) runs from this
   directory. `wrangler.jsonc` points `assets.directory` at `../../_site`, so
   the scrubbed build is uploaded as the Worker's static assets and the
   custom domain binding is re-affirmed.

Scrub-then-deploy ordering matters: the Pages artifact is uploaded *before*
the scrub, so GitHub Pages is never affected by the rewrites.

## What the Worker does (`src/index.js`)

One Worker, `seraphsys-site`, two jobs:

- **Static assets** — anything that matches a file in `_site/` is served
  directly by the Workers assets layer (the Worker script isn't even
  invoked). Cloudflare's asset router serves `wiki.html` at `/wiki`
  (auto-prettified; `/wiki.html` 307s there — browsers follow silently).
- **`/pulse-data/*` proxy** — the pulse page's JS fetches
  `/pulse-data/archive.json` and `/pulse-data/fragments/<ts>.html`
  same-origin. The Worker fetches the real files from the pulse-data branch
  of the upstream repo **server-side**, caches them at the edge for 5
  minutes, and returns them with clean headers. Visitors' browsers never
  contact GitHub, so DevTools shows nothing to trace. Only those two path
  shapes are allowed; everything else under `/pulse-data/` 404s.

Because the pulse page fetches its content at request time (not build time),
the pulse on `seraphsys.us` is always the most recent one regardless of when
the last deploy ran — same behaviour as the Pages copy, minus the
cross-origin fetch.

## Cloudflare-side wiring

| Piece | Value |
|---|---|
| Cloudflare account | Seraphsystemsllc (`40dff3d5...` — see `wrangler.jsonc`) |
| Worker | `seraphsys-site` |
| Custom domain | `seraphsys.us` (apex) — managed as a Workers Custom Domain; Cloudflare owns the DNS record + cert |
| Also in the zone | `api.seraphsys.us` → a separate, unrelated Worker. **Never touch it** when editing DNS. |

The domain is registered through Cloudflare Registrar in the same account,
so its nameservers are fixed to that account — the site must live there.

## Credentials

One repository secret: **`CLOUDFLARE_API_TOKEN`** — created from the
"Edit Cloudflare Workers" template, scoped to the Seraphsystemsllc account
and the `seraphsys.us` zone only. No other permissions. If it's ever rotated,
create a new token the same way and overwrite the secret; nothing else
changes.

## Operating it

```bash
# Deploy by hand (from a machine with wrangler auth to the right account)
cd deploy/cloudflare
npx wrangler deploy          # uploads ../../_site as-is — scrub first if it matters:
python ../../scripts/scrub_site_for_cf.py ../../_site

# Watch logs
npx wrangler tail seraphsys-site

# Test the scrub + leak gate locally against any staged _site/
python scripts/scrub_site_for_cf.py _site
```

Troubleshooting:

- **Deploy step fails with an auth error** → the `CLOUDFLARE_API_TOKEN`
  secret is missing/expired, or it's an *environment* secret (it must be a
  **repository** secret — the job doesn't declare an environment).
- **"Scrub site copy" step fails** → the leak gate found an identifying
  string the rewrites didn't cover (usually a new absolute URL added to a
  build script). Read the `::error::leak gate:` lines in the log, extend
  `scripts/scrub_site_for_cf.py`, and re-run. This failing is the gate
  working as designed.
- **Custom-domain trigger fails on deploy** → something re-created a
  conflicting DNS record for the apex. In the Cloudflare dashboard delete
  the conflicting `seraphsys.us` record (leave `api` alone) and re-run.
- **Pulse page empty on seraphsys.us but fine on Pages** → the `/pulse-data/`
  proxy is failing; `wrangler tail` while loading the page and check the
  upstream fetch.
