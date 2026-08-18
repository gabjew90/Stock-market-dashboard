---
title: "WW 2005-06-08 — Put options as insurance: the original tutorial, four years before the 2009 post"
type: source-summary
updated: 2026-08-12
sources: [raw/posts/2005-06-08-using-put-options-to-limit-losses-on-cme-and-goog-gmi-back-to-5.md]
---

# WW 2005-06-08 — Put options as insurance: the original tutorial, four years before the 2009 post

**Source:** [Using put options to limit losses on CME and GOOG; GMI back to +5](../../raw/posts/2005-06-08-using-put-options-to-limit-losses-on-cme-and-goog-gmi-back-to-5.md) · [original](https://wishingwealthblog.com/2005/06/using-put-options-to-limit-losses-on-cme-and-goog-gmi-back-to-5/) · tier: teaching

## What it covers

The protective-put tutorial four years earlier than the March 2009 post the wiki had treated as
the origin — with the insurance framing already fully formed, and the specific trigger for
choosing a put over a stop: **shakeout avoidance in choppy tape**.

## Key claims

- **When a put beats a stop, precisely:** he'd been stopped out of BOOM that day and "did not
  want to get stopped out of GOOG and CME... **if we had a sudden decline I might get shaken out
  only to see the stock rebound** by the end of the month. So, I bought insurance instead." The
  put converts a whipsaw risk into a fixed premium.
- **The insurance framing, original form:** "Do you call your agent and complain about the home
  insurance premium you paid last year, because your house did not burn down?... you do not
  regret buying the insurance if you did not have to use it."
- **The walkthrough:** CME at 243.49, mental floor $230 → rather than a stop at 230, buy the
  230-strike put expiring *past* the window he cares about (skip June's third-Friday expiry,
  go to July) — strike = the price he'd have stopped at, expiry = the period he wants covered.
- **Options in an IRA** noted as available even in 2005 (his broker allowed it) — consistent
  with the later DITM-calls-in-IRA practice.
- Market context read via the GMI internals: Successful 10-Day fell to 76 (<100), 136 new highs
  (lowest in 8 days), minority of index components rising — the top-warning that motivated
  raising stops in the first place.

## Feeds wiki pages

- [risk-and-cash.md](../methodology/risk-and-cash.md) — protective puts back-dated to 2005; the put-vs-stop decision rule
- [exits.md](../playbooks/exits.md) — shakeout avoidance as the trigger for insurance over stops
- [timeline.md](../history/timeline.md) — June 2005

## Sources

- [Using put options to limit losses on CME and GOOG](../../raw/posts/2005-06-08-using-put-options-to-limit-losses-on-cme-and-goog-gmi-back-to-5.md)
