---
title: "WW 2023-06-19 — How I compute new US highs and lows; used it to exit in 11/2021"
type: source-summary
updated: 2026-05-11
sources: [raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md]
---

# WW 2023-06-19 — How I compute new US highs and lows; used it to exit in 11/2021

**Source:** [Blog Post: Here is an explanation of how I compute new US highs and lows each day and used it to exit in 11/2021; the GMI is 6 (of 6)](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md) · [original](https://wishingwealthblog.com/2023/06/blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-2021-the-gmi-is-6-of-6/) · tier: teaching

## What it covers

Dr. Wish explains the technical procedure for computing new 52-week (250-bar) highs and lows each day in TC2000, covering the filter conditions he uses (volume > 10,000; close > $10) and why a custom PCF formula cannot be used (null results for stocks without 250 days of history). He then narrates how tracking these numbers led him to exit the market in November 2021 — noticing that new lows were surging to 438 even while QQQ was at an all-time high (day U-26 of the up-trend). He stayed out of the market for over a year through the subsequent Stage 4 decline. He also notes the counts as of June 2023: 207 new highs, 10 new lows, 78 at an all-time high.

## Key claims

- He tracks new 52-week highs and lows daily against the full US stock universe (~6,486 stocks in TC2000's built-in list). He filters for volume > 10,000 and close > $10. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- Technical implementation: must use TC2000's built-in "Price New High" and "Price New Low" conditions, not custom PCF formulas, because PCFs return null for stocks without the required history. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- In **November 2021**, QQQ was still hitting all-time highs (up-trend day U-26) but new lows were surging — reaching **438 on 11/22/2021**, which was QQQ's peak. This divergence prompted Dr. Wish to exit the market. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- He stayed out of the market for over a year after this exit, through QQQ's subsequent Stage 4 decline. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- He calls this a "lucky call" but frames the signal as breadth deterioration: new lows surging while the index is at highs is a divergence he tracks as a warning. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- As of June 2023 (GMI=6): 207 new highs, 10 new lows, 78 at all-time highs — a healthy ratio. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

## Feeds wiki pages

- [General Market Index (GMI)](../methodology/gmi.md) — new-high/new-low tracking as a GMI input; how it confirmed the 11/2021 exit.
- [Risk & cash](../methodology/risk-and-cash.md) — the 11/2021 exit decision: new-low surge as breadth divergence signal.
- [Market-state playbook](../playbooks/market-state.md) — new-low surge as an exit trigger; breadth divergence from price.
- [Track record](../history/track-record.md) — documented call: exited 11/2021 at or near QQQ peak; stayed out for over a year.
- [Timeline](../history/timeline.md) — 2021: breadth divergence exit; 2023: explanation post.
- [Glossary](../methodology/glossary.md) — new highs, new lows (daily counts), Stage 4.

## Sources

- [WW 2023-06-19 — How I compute new US highs and lows; used it to exit in 11/2021](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md)
