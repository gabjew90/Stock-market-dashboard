---
title: Reader Q&A — rules clarified in the comment threads
type: concept
updated: 2026-08-18
sources: []
---

# Reader Q&A — rules clarified in the comment threads

The blog's 4,136 reader comments were captured for the first time on 2026-08-12 (`ww comments`
→ `raw/comments.jsonl`). **678 are Dr. Wish replying**, and 501 of those are direct answers to a
reader's question. They matter because a post is him explaining his method to a general
audience, whereas a comment is a specific reader pinning down an edge case — "does an intraday
dip count?" — and him answering in one line. Those answers exist nowhere in the post bodies.

**Citation convention.** A comment citation has the same shape as a post citation but reads
`WW comment <date>` and points at the live permalink rather than a `raw/posts/` path. Comments
are *not* listed in `## Sources` blocks, which catalogue posts. Search them with
`ww search "…" --source comments`.

**Status:** a first pass over the 128 substantive rule answers. Not exhaustive.

## Green lines — how they are actually drawn

The post pages define the green line as an all-time high held ≥3 months. Two comments make the
mechanics considerably more precise, and both differ from the naive reading.

- **The 3 months is measured in monthly closes, and the line is drawn only in retrospect:**
  "The green line is drawn only after a peak that is not followed by a **higher monthly close**
  for 3 months." ([WW comment 2013-03-13](https://wishingwealthblog.com/2013/03/#comment-11015))
- **The line is not always the intraday high.** Asked why CMG's line sat below its all-time
  high: "I draw the green line on a monthly chart, **sometimes near its highest monthly close
  which may be below the highest price it traded at during the month if it did not hold**."
  ([WW comment 2013-10-01](https://wishingwealthblog.com/2013/10/#comment-14760)) A spike that
  the month did not close near is not automatically the line.
- **There is no GLB scan.** Asked to share one: "I do not have a single scan for this. I scan
  for new daily highs and then look at monthly charts and **manually draw in green lines** at
  all-time highs. Then I look for daily break-outs of the green line. I also use TC2000 to put
  in alerts for when a stock crosses the green line." ([WW comment 2013-09-28](https://wishingwealthblog.com/2013/09/#comment-14708))
  The GLB is a manual, chart-by-chart judgement with automation only on the alerting step.

See [green-line-breakouts.md](green-line-breakouts.md).

## What the GMI is *not*

- **It does not include the 10wk/30wk relationship:** "**GMI does not require 10 week to be
  above 30 week**, although this would be a major sign of strength." ([WW comment 2010-09-19](https://wishingwealthblog.com/2010/09/#comment-2670))
  A useful negative — the wiki's component list is complete, and the Stage-2 test sits outside it.
- **Publication cadence:** "I update the GMI each weekend and sooner if something major
  changes." ([WW comment 2010-04-17](https://wishingwealthblog.com/2010/04/#comment-1932))
  Weekly, not daily, in the 2010 era — worth knowing when reading the timeline dataset.
- **It is his own arbiter:** "While I may look at IBD's big picture, **I rely on the GMI** for my
  assessment of the market trend." ([WW comment 2009-12-20](https://wishingwealthblog.com/2009/12/#comment-1560))

## The two-speed design existed by 2010

[gmi.md](gmi.md) and the [2015 limitation](../sources/2015-02-22-an-important-limitation-of-the-gmi-signals.md)
present the GMI-for-trading / GMMA-for-pension split as originating in February 2015. **The
comments show it operating five years earlier**, stated as settled practice:

> "When the GMI weakens to below 4, I start to move up stops or reduce positions based on each
> stock's technicals. However, **as long as the longer term trends remain up, I stay invested in
> the mutual funds in my university pension.**" ([WW comment 2010-11-24](https://wishingwealthblog.com/2010/11/#comment-3072))

So 2015 is where he *published the evidence* (7 Sell/7 Buy signals inside one RWB up-trend) and
formalised the rule, not where the practice began.

**And the constraint that drives it is administrative, not just analytical:** "**I am limited as
to how often I can transfer funds in and out of equity funds** so I wait for a change in the
longer term before I go to cash." ([WW comment 2010-07-09](https://wishingwealthblog.com/2010/07/#comment-2405))
Mutual-fund market-timing restrictions are a real limit on the pension strategy — the moves are
signal-driven but paced by the fund families' switching rules.

## Stops and exits

- **Not percentage-based:** asked whether he uses a fixed 5% or a moving average — "I find a
  **recent support level or technical indicator that works with that stock**. It also depends
  upon how much I want to give back. Some people just use the prior day's low as a sell stop
  point." ([WW comment 2013-12-26](https://wishingwealthblog.com/2013/12/#comment-16234))
- **The 30-day rule for momentum stocks:** "I **never hold a momentum stock that closes below
  its 30 day** and I often buy off of a bounce and place my stop below the low of the bounce."
  ([WW comment 2009-02-19](https://wishingwealthblog.com/2009/02/#comment-262)) Note the bounce
  entry and bounce-low stop already in 2009 — earlier than [BOS](stock-selection.md) (2016).
- **The simplest version of the whole system**, given to a reader who had summarised it back to
  him: "I'll give you an even simpler rule — **I get out of the market whenever the QQQQ closes
  below its 30 week average!** This is Stan Weinstein's stage analysis approach. If one simply
  exits a stock or the market when it closes below its 30 week average one could avoid all melt
  downs!" ([WW comment 2009-08-04](https://wishingwealthblog.com/2009/08/#comment-1108))
- **Stage-2 preference, spelled out:** "I like the major indexes to be in a Stage 2 advance with
  the 30 week average rising... I prefer the QQQQ to also be above its 10 week average... **If
  the 10 week average closes below the 30 week I will become defensive.**" ([WW comment 2010-06-19](https://wishingwealthblog.com/2010/06/#comment-2286))
- **Defence of stop-losses after the 2010 flash crash**, when a reader argued they had been
  discredited: "We get one extreme whipsaw day unlike anything we have seen before and everyone
  wants to abandon stop losses. Stop losses, **if placed at technically accurate places**, save
  me a lot of money. Typically when my trigger price is hit, the stock keeps declining without a
  significant rebound." ([WW comment 2010-05-14](https://wishingwealthblog.com/2010/05/#comment-2140))

## Re-entry after being stopped out

A theme he returns to, and one the post pages under-weight:

- "It takes tremendous discipline to buy back a stock from which one has been stopped out of
  with a loss. But **such situations have often provided me with my best profits.** The Turtles
  were taught to go long at every buy signal because one never knew which signal would mark the
  beginning of a long trend." ([WW comment 2009-11-29](https://wishingwealthblog.com/2009/11/#comment-1489))
- "if I buy a stock and get stopped out with a small loss, **I can often make a good profit by
  buying it back** if it has given me a subsequent buy signal." ([WW comment 2013-04-13](https://wishingwealthblog.com/2013/04/#comment-11544))

## Timeframes — the hourly chart

The wiki's review flagged the hourly timeframe as undocumented. He names it in the research
chain: asked how he researches a scan hit — "First thing I do is check to see if it is a green
line stock on a **monthly** chart. I then look at the **weekly, daily and hourly** patterns. I
also see if it has been on the IBD 50 list." ([WW comment 2013-05-08](https://wishingwealthblog.com/2013/05/#comment-12122))
Four timeframes, monthly first. The hourly layer still has no page.

## Position sizing — asked repeatedly, answered once

Readers asked for sizing rules at least five times (2009, 2011, 2012 ×2, 2014). The answers, in full: "I have no specific rules for that" ([WW comment 2014-05-31](https://wishingwealthblog.com/2014/05/ignore-the-media-pundits-stage-analysis-shows-markets-remain-in-up-trend/comment-page-1/#comment-17827)); "I go in in phases. I am 95% in cash" ([WW comment 2012-11-13](https://wishingwealthblog.com/2012/11/gmi0-23rd-day-of-qqq-short-term-down-trend/comment-page-1/#comment-5365)); and a reading list — Weinstein, O'Neil, Lefèvre, and Covel's *Complete Turtle Trader* as "the best example I have found of a specific system for increasing one's position and managing risk" — with the instruction to "determine your own rules for averaging up and managing risk" ([WW comment 2011-01-06](https://wishingwealthblog.com/2011/01/2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs/comment-page-1/#comment-2656)). The habits that stand in for a rule are collected on [risk-and-cash — position sizing](risk-and-cash.md#position-sizing--what-he-has-said-and-what-he-has-not).

## On his own method

- **Trend-following is necessarily late, and he accepts it:** a reader complained the signal
  lagged the turn by five days — "I am not a day trader. **Trend followers only identify a trend
  after it has begun.** Before today, I would be much more likely to be whipsawed... I want to
  ride trends that last weeks, not a few days." ([WW comment 2010-05-05](https://wishingwealthblog.com/2010/05/#comment-2098))
- **Test it yourself and drop what fails**, said to a reader reporting that tighter stops hurt
  his results: "**If whatever techniques you are testing do not improve your trading results,
  then abandon them.** The key is to adopt only that which works better for you." ([WW comment 2013-04-13](https://wishingwealthblog.com/2013/04/#comment-11544))

## See also

- [Green Line Breakouts](green-line-breakouts.md) · [GMI](gmi.md) · [Trading philosophy](trading-philosophy.md)
- [Risk & cash](risk-and-cash.md) · [Exits](../playbooks/exits.md)

## Sources

_Comments, not posts — each claim is cited inline to its permalink. The underlying data is
`raw/comments.jsonl` (`ww comments`); search it with `ww search "…" --source comments`._
