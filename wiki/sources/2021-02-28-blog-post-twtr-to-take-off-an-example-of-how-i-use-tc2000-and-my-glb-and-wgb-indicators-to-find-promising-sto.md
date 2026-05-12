---
title: "WW 2021-02-28 — $TWTR to take off? Using TC2000, GLB and WGB indicators"
type: source-summary
updated: 2026-05-11
sources: [raw/posts/2021-02-28-blog-post-twtr-to-take-off-an-example-of-how-i-use-tc2000-and-my-glb-and-wgb-indicators-to-find-promising-sto.md]
---

# WW 2021-02-28 — $TWTR to take off? Using TC2000, GLB and WGB indicators

**Source:** [Blog post: $TWTR to take off? –An example of how I use TC2000 and my GLB and WGB indicators to find promising stocks](../../raw/posts/2021-02-28-blog-post-twtr-to-take-off-an-example-of-how-i-use-tc2000-and-my-glb-and-wgb-indicators-to-find-promising-sto.md) · [original](https://wishingwealthblog.com/2021/02/blog-post-twtr-to-take-off-an-example-of-how-i-use-tc2000-and-my-glb-and-wgb-indicators-to-find-promising-stocks-gmi-could-turn-red-by-mondays-close/) · tier: trade_example

## What it covers

A detailed worked example showing how Dr. Wish integrates his WGB (weekly green bar) scan with GLB identification, using TWTR in February 2021. He provides the TC2000 formula for the WGB indicator explicitly. TWTR had just had a GLB after 8 years below its December 2013 IPO-era green line top of $74.73. He shows the monthly, weekly, and daily charts in sequence: monthly for GLB identification, weekly for WGB confirmation, daily for entry volume. He also explains how the WGB trailing stop works (stop just below the low of each successive WGB).

## Key claims

- WGB (weekly green bar) formula in TC2000: `avgc4>avgc10 and avgc10>avgc30; L<=avgc4 and C>avgc4; C>C1; avgc4>avgc4.1` — all on weekly timeframe. The bar must trade below the 4wk average intra-week but close above it, and the 4wk average must be rising.
- A WGB trailing stop rule: move the stop up to just below the low of each successive WGB; exit when the stock trades below the most recent WGB low.
- TWTR's GLB came 8 years after its December 2013 green line top ($74.73). The multi-year overhead supply was a feature, not a bug: overcoming it required huge buying pressure.
- He applied the WGB scan to 401 IBD/MarketSmith Growth 250 stocks; 47 passed; then he filtered to those above their last green line top. That left TWTR as the most impressive candidate.
- Failed GLB on Thursday (closed $0.14 below green line on QQQ down-3.5% day); successful GLB on Friday (closed $77.06 on above-average volume). He uses closing price, not intraday, to define GLB success or failure.
- Exit rule for GLB positions: sell if the stock *closes* below the green line. He uses a mental stop rather than a hard stop to avoid being shaken out on intraday dips.
- He will "always sell any stock I purchased after a GLB if it *closes* back below the green line."

## Feeds wiki pages

- [Green Line Breakouts](../methodology/green-line-breakouts.md) — failed-GLB day vs. confirmed GLB; closing-price rule; mental stop rationale
- [Moving-average rules](../methodology/moving-average-rules.md) — WGB formula spelled out explicitly; trailing stop with successive WGB lows
- [Playbook: Buying a GLB](../playbooks/buying-glb.md) — entry confirmation (closing price, volume, day 2 rule)

## Sources

- [Blog post: $TWTR to take off? – GLB and WGB indicators](../../raw/posts/2021-02-28-blog-post-twtr-to-take-off-an-example-of-how-i-use-tc2000-and-my-glb-and-wgb-indicators-to-find-promising-sto.md)
