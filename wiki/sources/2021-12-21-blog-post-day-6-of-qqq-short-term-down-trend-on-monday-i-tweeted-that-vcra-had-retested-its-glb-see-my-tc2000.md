---
title: "WW 2021-12-21 — The intraday ATH scan, formula included"
type: source-summary
updated: 2026-08-26
sources: [raw/posts/2021-12-21-blog-post-day-6-of-qqq-short-term-down-trend-on-monday-i-tweeted-that-vcra-had-retested-its-glb-see-my-tc2000.md]
---

# WW 2021-12-21 — The intraday ATH scan, formula included

**Source:** [Blog post: Day 6 of $QQQ short term down-trend; On Monday, I tweeted that $VCRA had retested its GLB, see my TC2000 scan for finding such stocks](../../raw/posts/2021-12-21-blog-post-day-6-of-qqq-short-term-down-trend-on-monday-i-tweeted-that-vcra-had-retested-its-glb-see-my-tc2000.md) · [original](https://wishingwealthblog.com/2021/12/blog-post-day-6-of-qqq-short-term-down-trend-on-monday-i-tweeted-that-vcra-had-retested-its-glb-see-my-tc2000-scan-for-finding-such-stocks/) · tier: teaching

## What it covers

**The near-ATH scan written out, with the TC2000 syntax.** "I have a **simple formula I wrote for TC2000 that
finds any stock that reaches an ATH in the past 100 days** (use **price new high** built-in condition set to
**250 month high within past 5 months**) **and that is currently within 3% of its 100 day high (`C>.97*maxh100`).**
**TC2000 scans my watchlist of IBD50/MarketSmith stocks real time throughout the day.**" Two conditions doing
different jobs: the built-in condition establishes the stock has been at an *all-time* high recently (250 months
is roughly twenty years), and the price test keeps it *near* that high now — which is the proximity filter that
makes an entry's invalidation close by. **Then the manual steps**, which he does not automate: "I then look at
the stocks that come up and **look at the built-in volume buzz indicator to see if it has unusual volume for that
time of day** and if I like the set-up. I then check out its fundamentals on MarketSmith." So the scan runs
continuously and the judgement stays human — screen, then volume buzz, then fundamentals. He also notes the
intraday channel: "**I tweet intraday when I see something interesting — no guarantees! Do your own
research.**"

## Key claims

- **The formula**: an ATH within the past 100 days (via TC2000's *price new high*, 250-month high within 5 months) **and** `C > .97*maxh100` — currently within 3% of the 100-day high.
- **Proximity is the point** — near the high means the invalidation level is close, which is what keeps the risk small.
- **Run real-time against a curated watchlist**, not the whole universe, all through the session.
- The automated part ends at the list; volume buzz and fundamentals are checked by hand afterwards.
- Intraday tweets are the publication channel for what the scan surfaces, with an explicit no-guarantees disclaimer.

## Feeds wiki pages

- [scans.md](../methodology/scans.md) — the intraday near-ATH scan, with syntax

## Sources

- [Blog post: Day 6 of $QQQ short term down-trend; On Monday, I tweeted that $VCRA had retested its GLB, see my TC2000 scan for finding such stocks](../../raw/posts/2021-12-21-blog-post-day-6-of-qqq-short-term-down-trend-on-monday-i-tweeted-that-vcra-had-retested-its-glb-see-my-tc2000.md)
