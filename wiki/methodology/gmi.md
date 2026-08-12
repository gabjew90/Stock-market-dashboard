---
title: General Market Index (GMI)
type: entity
updated: 2026-08-12
sources:
  - raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md
  - raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md
  - raw/posts/2020-01-05-my-pet-stocks-frpt-and-pawz.md
  - raw/posts/2026-01-04-blog-post-day-1-of-qqq-short-term-down-trend-gmi2-and-could-turn-red-on-monday-qqq-has-now-closed-below-its-1.md
  - raw/posts/2007-05-22-gmi-6-no-longer-post-daily-but-when-gmi-changes-the-ideal-boomer-strategy-writing-covered-calls.md
  - raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md
  - raw/posts/2007-09-17-gmi-5-ibd100-stocks-not-good-for-buy-and-hold.md
  - raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md
  - raw/posts/2007-11-19-gmi1gmi-r1-qqqq-bounce-off-support-too-many-bears-new-leaders.md
  - raw/posts/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md
  - raw/posts/2005-04-26-general-market-index-gmi.md
  - raw/posts/2008-08-22-gmi-3-gmi-r-5-12th-day-of-qqqq-up-trend-still-cautious.md
  - raw/posts/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md
  - raw/posts/2023-08-09-blog-post-day-1-of-new-qqq-short-term-down-trend-and-gmi3-many-fallen-angels-smci-aapl-cmg-buying-sqqq-now-bu.md
  - raw/posts/2025-12-14-blog-post-day-11-of-qqq-short-term-up-trend-it-could-end-on-monday-ibd-50-type-growth-stocks-are-in-a-bwr-dow.md
  - raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md
  - raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md
  - raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md
  - raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md
  - raw/posts/2012-06-18-an-excerpt-from-my-trading-diary-from-the-90s-market-at-critical-juncture.md
  - raw/posts/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md
  - raw/posts/2005-12-03-gmi-6-wpm-shows-a-little-dow-30-deterioration-correlation-of-some-indicators-with-s-mcd-break-out-jnj-sick.md
  - raw/posts/2005-11-13-gmi6-my-favorite-posts-gmi-as-a-trend-indicator-wpm-shows-all-indexes-strong-jim-cramer-on-charts-some-big-ea.md
  - raw/posts/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md
---

# General Market Index (GMI)

The 0–6 composite indicator Dr. Wish uses to decide whether the market is GREEN (be invested) or RED (be cautious / in cash). It counts six binary conditions about the state of the market; each true condition adds 1 point.

## The six components (original 2005 definition)

Dr. Wish introduced the GMI on 2005-04-26 ([WW 2005-04-26](../../raw/posts/2005-04-26-general-market-index-gmi.md)). His "universe" is approximately 4,000 actively traded stocks priced $5 or above. The six components, each worth 1 point:

1. **Successful 10-Day New High count > 100.** Of the stocks in the universe that hit a 52-week high 10 days ago, at least 100 must have closed today higher than they closed 10 days ago. In a rising market traders let strong stocks keep climbing; in a bad market they take profits quickly and stocks gyrate. ([WW 2005-04-26](../../raw/posts/2005-04-26-general-market-index-gmi.md))

2. **At least 100 new 52-week highs today** in the universe. A healthy market should produce at least 100 new highs daily. When new lows exceed new highs, the odds are against buying growth stocks. ([WW 2005-04-26](../../raw/posts/2005-04-26-general-market-index-gmi.md))

3. **QQQQ daily trend positive.** Dr. Wish's technical indicators (not disclosed in 2005) must show the QQQQ (Nasdaq 100) in a rising daily trend. ([WW 2005-04-26](../../raw/posts/2005-04-26-general-market-index-gmi.md)) **The 2007 posts pin this to the 30-day average:** "I will look for support of the QQQQ at the 30 day average, currently at 47.90. Several closes below the 30 day would decrease the GMI." ([WW 2007-09-17](../../raw/posts/2007-09-17-gmi-5-ibd100-stocks-not-good-for-buy-and-hold.md)) The reconstruction in `src/ww/indicators/gmi.py` treats the 30-day SMA as a proxy for this component; that choice is better supported than "proxy" implies.

4. **SPY daily trend positive.** Same test applied to the SPY (S&P 500). ([WW 2005-04-26](../../raw/posts/2005-04-26-general-market-index-gmi.md))

5. **QQQQ weekly trend positive.** The same measure as #3 but on a weekly timeframe. A strong market has both daily and weekly trends positive; the daily flips first, then the weekly confirms. ([WW 2005-04-26](../../raw/posts/2005-04-26-general-market-index-gmi.md)) He calls this the **"Weekly QQQQ Index"** and singles it out: "This index is my primary indicator of a longer term up or down move" — illustrated with the QQQQ weekly against its 30-week average. ([WW 2007-11-19](../../raw/posts/2007-11-19-gmi1gmi-r1-qqqq-bounce-off-support-too-many-bears-new-leaders.md))

6. **IBD Mutual Fund Index above its 50-day MA.** When growth mutual funds (the IBD index) are rising, growth stocks tend to follow. ([WW 2005-04-26](../../raw/posts/2005-04-26-general-market-index-gmi.md)) **This component was never replaced** — see [Component 6: unchanged from 2005 to 2025](#component-6-unchanged-from-2005-to-2025) below.

### Component 6: unchanged from 2005 to 2025

An earlier version of this page flagged component 6 as "later replaced or modified." That was wrong, and the corpus resolves it: the component is the same in 2025 as at launch, and Dr. Wish names it in present tense at three widely separated points.

- **2008-08-22** — "one of the GMI components measures whether the IBD growth mutual fund index is above its 50 day average. Well, this index has been below its 50 day average since mid-June, and I have never consistently made money trading growth stocks when this indicator is negative." ([WW 2008-08-22](../../raw/posts/2008-08-22-gmi-3-gmi-r-5-12th-day-of-qqqq-up-trend-still-cautious.md))
- **2009-01-12** — the component belongs to both composites, and he discloses the symbol he reads it from after IBD stopped publishing the average: "IBD no longer publishes the 50 day average for the mutual fund index, but the chart with the average is available on their website's stock charting application (enter symbol: **0muti**)." ([WW 2009-01-12](../../raw/posts/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md))
- **2023-08-09** — still a live component with the power to flip the signal: "the GMI could fall to 2 and trigger a Red signal if the IBD Mutual Fund Index (0muti) closes below its 50 day average." ([WW 2023-08-09](../../raw/posts/2023-08-09-blog-post-day-1-of-new-qqq-short-term-down-trend-and-gmi3-many-fallen-angels-smci-aapl-cmg-buying-sqqq-now-bu.md))
- **2025-12-14** — the most recent verbal description of any GMI component in the corpus: "The component in my GMI table below that is positive if the IBD Growth Mutual Fund index (**0MUTI**) has closed above its 50 day average is now negative." ([WW 2025-12-14](../../raw/posts/2025-12-14-blog-post-day-11-of-qqq-short-term-up-trend-it-could-end-on-monday-ibd-50-type-growth-stocks-are-in-a-bwr-dow.md))

Two consequences. First, the reconstruction's use of **FFTY** as a component-6 proxy (see below) is a substitute for a series that is still live and still readable as `0muti` on IBD's charting application — not a replacement for a retired one. Second, `0muti` is a specific, identifiable series, so a faithful component 6 is in principle obtainable rather than permanently proxied.

### The published table — verbatim component labels (2007, 2013, 2020, 2026)

This page previously said the current component labels "have not been recovered because the
daily GMI table is published as an image." That was a failure of method, not a real limit:
the tables are ~2,547 dated images on a systematic `gmi<date>` filename convention, and
reading four of them across two decades resolves every open definitional question below.

**The GMI's six components, transcribed from the table of 2026-01-02** ([WW 2026-01-04](../../raw/posts/2026-01-04-blog-post-day-1-of-qqq-short-term-down-trend-gmi2-and-could-turn-red-on-monday-qqq-has-now-closed-below-its-1.md)) — identical in wording to the 2020 and 2013 tables:

1. `WISHING WEALTH 10 DAY SUCCESSFUL NEW HIGH INDEX GREATER THAN OR EQUAL TO 50%, min. 20`
2. `AT LEAST 100 NEW HIGHS TODAY OUT OF 6,000+ U.S. STOCKS`
3. `WISHING WEALTH DAILY QQQ INDEX POSITIVE`
4. `WISHING WEALTH DAILY SPY INDEX POSITIVE`
5. `WISHING WEALTH WEEKLY QQQ INDEX POSITIVE`
6. `IBD MUTUAL FUND INDEX GREATER THAN 50 DAY AVERAGE`

So the 2005 definition is intact after twenty years, with two amendments the prose never
mentioned:

- **Component 1 carries a `min. 20` floor.** The ≥50% rule is suspended when fewer than 20
  stocks made new highs ten days ago — a small-sample guard. The table prints the raw
  fraction beside it (e.g. `29%`, and in 2007 `62/128, 48%`), so the denominator is visible.
- **Component 2's universe grew with the data source**, and the table states it explicitly:
  `4,000 STOCKS` (2007) → `5,000+` (2013, 2020) → `6,000+ U.S. STOCKS` (2026). The *threshold*
  stayed at 100 throughout, so the component has quietly become easier to satisfy in
  breadth terms — worth knowing when comparing a 2007 GMI reading to a 2026 one.

Components 3–5 are named as Wishing-Wealth-branded sub-indices ("DAILY QQQ INDEX") rather
than defined in the table, so their internals remain undisclosed — but the 2007 prose pins
the daily ones to the 30-day average and the weekly one to the 30-week average (above).

The table footer also carries a standing note: **"For GMI definitions, click on 'my favorite
posts,' at bottom right of post"** — he points readers at his own [My Favorite Posts](../../raw/categories.json)
category as the definitional source, which is the same category the ingest queue should
now be working from.

**Later refinement of component 1:** By 2014, Dr. Wish had sharpened the Successful 10-Day New High component: the threshold is ≥50% of stocks that hit a new high 10 days ago closing higher today (not an absolute count of 100). "If at least 50% of all of the stocks that had hit a new high 10 days ago pass this criterion, then the indicator is positive." ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

**One GMI component confirmed:** The QQQ (or QQQQ) closing above its 30-week moving average is one of the six GMI components. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))

## How he uses it

The GMI is read as GREEN or RED based on its score:

- **GMI ≥ 4:** be long. He says explicitly: "I like to be long if the GMI is 4 or more." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- **GMI ≤ 3:** get defensive. "When it declines to 3 or below, I get defensive in my trading IRA." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- In a severe down-trend, all indicators register zero (GMI = 0). ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))

The GMI can move between extremes very quickly — in one documented instance, it went from +3 to +6 in a single day. His lesson: "This is an example of how bad it is to marry a scenario. When the instruments tell me the market is reversing direction, I must act on it and not fight it." ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))

**GMI buy signal criterion (2012):** GMI > 3 on **two consecutive days**. At that point he closes all shorts and goes long. "I will be much more confident of the new up-trend once it lasts 5 days." ([WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md)) Confirmed independently: "Two consecutive days with the GMI above 3 would turn the GMI signal to buy." ([WW 2012-06-18](../../raw/posts/2012-06-18-an-excerpt-from-my-trading-diary-from-the-90s-market-at-critical-juncture.md))

He uses the GMI alongside the [QQQ Short-Term Timing](qqq-short-term-timing.md) count and [T2108](t2108.md). See the [market-state playbook](../playbooks/market-state.md) for how these combine.

## New highs / new lows — a breadth supplement to the GMI

Dr. Wish tracks the daily count of new 52-week highs and lows in TC2000 (filtered for close > $10 and volume > 10,000 against the full US stock universe of ~6,486 stocks). These are a leading breadth indicator that can diverge from the GMI and the index price, giving an early warning. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

The implementation requires the built-in "Price New High" and "Price New Low" TC2000 conditions, not custom PCF formulas (which fail for stocks without the full history window). ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

Documented example: in **November 2021**, QQQ was at all-time highs (day U-26 of the short-term up-trend) but new lows surged to **438 on 11/22/2021** — QQQ's exact peak. This divergence led Dr. Wish to exit the market. The subsequent Stage 4 decline lasted over a year. He describes it as a "lucky call" but attributes it to the breadth divergence signal. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

## Evolution

### 2005 — Original GMI (6 components)

The original six components described above; score range 0–6. At launch (April 2005), GMI = 0. ([WW 2005-04-26](../../raw/posts/2005-04-26-general-market-index-gmi.md))

### 2005 — GMI historical track record chart (first published)

In November 2005, Dr. Wish published his first chart of GMI values from inception, visually showing that GMI ≥ 5 periods coincided with profitable long conditions and GMI < 3 periods coincided with market weakness. The chart confirmed that GMI was +6 for all of July 2005 and had been 5 or higher since November 1, 2005. He left readers to judge its usefulness: "It is for me." ([WW 2005-11-13](../../raw/posts/2005-11-13-gmi6-my-favorite-posts-gmi-as-a-trend-indicator-wpm-shows-all-indexes-strong-jim-cramer-on-charts-some-big-ea.md))

### 2005-2006 — GMI-S (short-term sub-index, 0–100 scale)

Dr. Wish occasionally published a **GMI-S** alongside the GMI. The GMI-S measures short-term breadth on a 0–100 scale. A rapid fall from GMI-S=75 to GMI-S=31 in a single week (February 2006) signalled deterioration in the underlying breadth even when the overall GMI (at +4) had not yet dropped decisively. ([WW 2006-02-06](../../raw/posts/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md))

**Its construction is disclosed in 2007**, contrary to what this page previously said: "Only one of the **16 short term indicators for the IJR, DIA, SPY and QQQQ** is positive (GMI-S: 6%)" — 1/16 ≈ 6%. So the GMI-S is the percentage of sixteen short-term indicators, four applied to each of four index ETFs (small-cap IJR, Dow DIA, S&P SPY and Nasdaq QQQQ), that are currently positive. The individual sixteen are not named. ([WW 2007-08-20](../../raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md))

### 2006-2007 — GMI-L (long-term measure of weekly trends, reported as a %)

A **GMI-L** appears throughout the 2007 posts and is absent from the wiki's earlier accounts. He defines it in passing as "my longer term measure of weekly trends," reported as a percentage positive, and reads it as the slow counterpart to the GMI-S. ([WW 2007-12-17](../../raw/posts/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md))

Its diagnostic value is in the comparison across episodes. In December 2007 it fell to **31%** — "the lowest since it hit 20% in August, **2006**, near the bottom of that four month decline" — and crucially, "in the two declines in 2007 (March and August), the GMI-L never fell below 50%." A GMI-L below 50% therefore separated a correction from what became the 2008 bear market. Six weeks earlier, days after the October 2007 top, it had still read **94%**. ([WW 2007-10-29](../../raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md), [WW 2007-12-17](../../raw/posts/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md))

Like the GMI-S, the component list is undisclosed, and like the GMI-S it disappears from the daily posts after the typepad era. Both are reported as percentages, as is the GMI-R (80% = 8 of 10).

### 2007 — threshold variation

The GMI's action thresholds are not stated identically across posts, and the wiki records the variation rather than picking one:

| Date | Stated rule |
|---|---|
| 2007-08-20 | "exit the long side... when the GMI falls below 4 and... buy once it climbs back above 3" ([WW 2007-08-20](../../raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md)) |
| 2007-10-29 | "I will trade long in the market as long as the GMI is **greater than 2**" ([WW 2007-10-29](../../raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md)) |
| 2011-03-07 | "I like to be long if the GMI is 4 or more... When it declines to 3 or below, I get defensive" ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)) |
| 2012-04-30 | Buy signal = GMI > 3 on two consecutive days ([WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md)) |

The ≥4 / ≤3 reading is the dominant and durable one; the October 2007 "greater than 2" appears to be a looser stance taken mid-up-trend rather than a redefinition. The [backtest](backtest-timing-overlay.md) uses ≥4 long / ≤3 cash.

### Intermediate — GMI-R (10 components), with its four extra indicators named

The GMI-R is the GMI plus four more indicators, giving a 0–10 composite, published alongside
the GMI but with no decision rules tied to it. He calls it "the **more sensitive** GMI-R" —
it moves before the GMI does, which is what made it useful as an early read. ([WW 2009-01-12](../../raw/posts/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md))

**The four extras are printed in the table.** The 2007-10-26 table lists items 7–10 with the
note *"Revised index requires additional indicators 7-10, with '*'"* ([WW 2007-10-29](../../raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md)):

7. `MORE NEW HIGHS THAN LOWS TODAY`
8. `QQQQ CLOSED ABOVE 10 WEEK AVERAGE`
9. `QQQQ CLOSED ABOVE 4 WEEK AVERAGE`
10. `QQQQ CLOSED ABOVE 10 DAY AVERAGE`

Note what these are: three plain moving-average tests on QQQQ at three horizons, plus a
breadth check. The GMI-R = slow structural GMI + a fast QQQQ trend ladder, which is exactly
why it flips first.

### 2011 → 2026 — GMI2: a *growing* companion index, not a fixed 6

The GMI-R was superseded by the GMI2, which inherits the GMI-R's four extra indicators as its
own first four. Decision rules still apply to the GMI only: "I do not have decision rules
based in the GMI-R or the new GMI2." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))

**This page previously described the GMI2 as a fixed 6-component composite. The tables show it
is not fixed — it grew from 6 to 9 components between 2013 and 2026:**

| # | 2013-01-04 (6) | 2020-01-03 (8) | 2026-01-02 (9) |
|---|---|---|---|
| 1 | MORE NEW HIGHS THAN LOWS TODAY | same | `MORE US NEW HIGHS THAN LOWS TODAY` |
| 2 | QQQ CLOSED ABOVE 10 WEEK AVERAGE | same | same |
| 3 | QQQ CLOSED ABOVE 4 WEEK AVERAGE | same | same |
| 4 | QQQ CLOSED ABOVE 10 DAY AVERAGE | same | same |
| 5 | QQQ: 4 WEEK AVERAGE >10WKAVG>30WKAVG | same | same |
| 6 | **QQQ CLOSED ABOVE 5 MONTH AVERAGE** | `QQQ DAILY 10.4 STOCHASTIC <20` | same as 2020 |
| 7 | — | `QQQ Daily 12/26/9 MACD HIST RISING L2DAYS OR BLACK (>0)` | same |
| 8 | — | `QQQ 10.4.4 DAILY STOCHASTIC—FAST>SLOW OR ABOVE 80` | same |
| 9 | — | — | `QQQ DAILY 10.1 STOCHASTIC<=20` |

Sources: [WW 2013-01-07](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md), [WW 2020-01-05](../../raw/posts/2020-01-05-my-pet-stocks-frpt-and-pawz.md), [WW 2026-01-04](../../raw/posts/2026-01-04-blog-post-day-1-of-qqq-short-term-down-trend-gmi2-and-could-turn-red-on-monday-qqq-has-now-closed-below-its-1.md).

Two things follow. First, **the GMI2's character changed**: components 1–5 are trend-and-breadth
tests, but everything added after 2013 is an *oscillator* test (stochastics and MACD). The
2013 "5 month average" trend test was dropped to make room. The GMI2 has become an
overbought/oversold panel bolted onto a trend panel. Second, because the denominator moved,
**a GMI2 reading is not comparable across eras** — "GMI2: 6" means 6-of-6 in 2013 and 6-of-9
in 2026. The wiki should always cite the denominator; his own tables print it as `GMI2: 5/6`.

The oscillator components also tie the GMI2 directly to the entry signals: the 10.1 and 10.4
stochastics driving GMI2 components 6 and 9 are the same ones behind the black and blue dots
of the [oversold bounce](oversold-bounce.md) setup.

### GMI-S — construction fully visible in the table

The GMI-S is the average of four per-ETF short-term readings. The 2007-10-26 table prints it
as `GMI Short term index (GMI-S): 44 (SPY:50, QQQ:75, DIA:25, IJR:25)` — and (50+75+25+25)/4
= 43.75 ≈ 44. ([WW 2007-10-29](../../raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md))

Each ETF's reading moves in 25-point steps, so each is built from **four** short-term
indicators — which is exactly the sixteen he refers to in prose: "Only one of the 16 short
term indicators for the IJR, DIA, SPY and QQQQ is positive (GMI-S: 6%)." ([WW 2007-08-20](../../raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md)) The identity of
the four per-ETF indicators is still undisclosed, but the *shape* — 4 ETFs × 4 tests, averaged
to 0–100 — is now settled. The four are plausibly the GMI-R's ladder (10-day, 4-week, 10-week
averages plus one more) applied per ETF, though nothing states that.

The same table prints `GMI Long Term Index (GMI-L): 94`, confirming it is published as a
single percentage rather than a component count.

## A limitation he published himself (2015)

In February 2015 — with the GMI reading 6 of 6 — Dr. Wish published a limitation of his own
headline indicator and changed how he used it. Examining a GMMA chart of the QQQ he found that
**"since early 2014, the GMI has issued 7 separate Sell signals... followed by 7 Buy signals"**
while the QQQ "remained in a strong RWB up-trend" throughout. ([WW 2015-02-22](../../raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md))

His conclusion, and it is a demotion:

> "a GMI Sell signal should only be used by me for **short term trading decisions**... I should
> therefore probably remain invested long term in the market (at least in my university pension
> account) **as long as the RWB pattern is in place, even when the GMI signals Sell**."

This produces the two-speed design the rest of the wiki describes but had never justified:

| Horizon | Signal | Account |
|---|---|---|
| Short-term trading | **GMI** | Speculative / trading IRA |
| Long-term allocation | **Weekly GMMA / RWB** pattern | University pension |

Major tops, he restates, are signalled by the weekly RWB→BWR transition — "when the shorter
averages declined below the longer term averages" — not by the GMI.

**This matters for the [backtest](backtest-timing-overlay.md).** Our overlay of GMI ≥ 4 long /
≤ 3 cash on QQQ found the strategy marginal — a large cut in max drawdown bought at a cost in
Sharpe and CAGR, with the damage concentrated in whipsaws during sustained advances. That is
the same phenomenon he documented qualitatively in 2015, seven separate times in about a year.
The backtest is not contradicting him; it is measuring a limitation he had already published
and acted on.

## What else the daily table publishes

Below the two composites, every GMI table carries a standing block of context readings. These
are the numbers he quotes in prose all the time; having the table makes clear they are a fixed
panel, not ad-hoc mentions.

| Row | 2026-01-02 value | Notes |
|---|---|---|
| `QQQ SHORT TERM TREND COUNT` | `D-1` | The [day count](qqq-short-term-timing.md) in the post titles. `U-`/`D-` prefix = up/down-trend. |
| `# OF WEEKS QQQ HAS CLOSED Below ITS 10 WEEK AVERAGE` | 1 | Direction word flips Above/Below and is colour-coded. |
| `# OF WEEKS SPY HAS CLOSED Above ITS 10 WEEK AVERAGE` | 6 | |
| `# OF WEEKS QQQ 10 WEEK AVERAGE Above ITS 30 WEEK AVG` | 28 | The Stage-2 clock — added since 2020. |
| `WORDEN INDICATOR T2108` | 50% (−3) | With weekly change. See [T2108](t2108.md). |
| `Nasdaq 100 stocks above MACD signal line` | 35% (−25) | |
| `QQQ Weekly 10.4 Stochastics (>80 = strong up-trend)` | 64 (−6) | Added since 2020. |

**The MACD row settles a question from the 2026-08-12 coverage review**, which flagged 231
corpus mentions of MACD against 6 in the wiki and could not tell what role it played. It is a
**breadth gauge with a permanent slot in the table** — the percentage of Nasdaq 100 stocks
whose MACD is above its signal line — not a per-stock entry signal. He reads it as short-term
participation, and the weekly change is printed beside it. It is *not* a GMI or GMI2
component; it sits in the context block.

**The table also carries its own T2108 annotation, and it differs from the number this wiki
teaches.** The 2013 and 2020 tables print "*Market tops likely above 80, bottoms likely below
25*"; the 2007 table says "*below 30*." The [T2108 page](t2108.md) documents a **<10%**
contrarian buy zone, sourced from the prose. Both are his — they serve different purposes:
80/25–30 is the routine top/bottom band printed daily, while <10% is the rare
back-up-the-truck extreme he writes about in crisis posts. The page should carry both bands
rather than only the extreme.

## Code — computing the GMI

The GMI is six binary checks ([`src/ww/indicators/gmi.py`](../../src/ww/indicators/gmi.py)). Three of them — QQQ daily trend, SPY daily trend, QQQ weekly trend (close above its 30-week average) — are computable from ordinary price data, so the code returns those even with a free data provider. The other three — the "Successful 10-Day New High" share, ≥100 new 52-week highs today, and the IBD Mutual Fund Index above its 50-day average — need a daily market-breadth panel and the IBD fund series, which aren't freely available; those come back as `None` (listed in `.unavailable`) until you plug in a provider that has them.

```python
@dataclass
class GMIResult:
    score: int                          # number of components that are True (0..6)
    components: dict[str, bool | None]   # per-component verdict; None = data unavailable
    unavailable: list[str]

def gmi(provider, date, *, original_rule=False) -> GMIResult:
    verdicts = {
        "successful_10day_new_high": _successful_10day(provider, date, original_rule=original_rule),  # 2014: higher >= 50% of total; 2005: higher >= 100
        "new_highs_ge_100":          _new_highs_ge_100(provider, date),                                 # >= 100 new 52-wk highs today
        "qqq_daily_trend":           _daily_trend_up(provider, "QQQ", date),                            # QQQ close above its 30-day SMA (proxy), as of `date`
        "spy_daily_trend":           _daily_trend_up(provider, "SPY", date),
        "qqq_weekly_trend":          _qqq_weekly_above_30wk(provider, date),                            # QQQ weekly close above its 30-week SMA, as of `date`
        "ibd_fund_above_50d":        _ibd_fund_above_50d(provider, date),                               # IBD Mutual Fund Index above its 50-day SMA
    }
    unavailable = [k for k, v in verdicts.items() if v is None]
    return GMIResult(score=sum(v is True for v in verdicts.values()), components=verdicts, unavailable=unavailable)
```

The `DataProvider` interface ([`provider.py`](../../src/ww/indicators/provider.py)) defines the breadth/fund hooks (`successful_10day_new_high`, `nasdaq_new_highs_lows`, `ibd_mutual_fund_index`); `YFinanceProvider` raises `DataUnavailable` for them, `StubProvider` lets you supply fixtures.

Try it: `ww compute gmi 2026-05-01` prints the partial GMI from current QQQ/SPY prices and flags the three components that need breadth/fund data. `ww compute gmi 2014-08-01 --demo` runs it against built-in *illustrative* fixtures (made-up numbers — not real history) so you can see a full 6/6 result and the per-component breakdown. Acquiring the real breadth/fund data so a true historical GMI can be reproduced is a later phase — and a prerequisite for the planned backtest of his strategy.

## Reconstructing the GMI from free data

The `gmi()` code can be driven by a [`BreadthProvider`](../../src/ww/indicators/breadth_provider.py) that reads a locally-built market-breadth series (`data/breadth/breadth_series.parquet`, produced by `ww breadth fetch` + `ww breadth build` from the free Nasdaq Trader symbol files + yfinance). With it, all six components are computed: components 3/4/5 from QQQ/SPY prices, components 1/2 from the reconstructed 52-week-high panel, and component 6 from the **Innovator IBD® 50 ETF (FFTY)** — IBD's own growth-leaders index, the closest tradeable thing to "IBD anything" — above its 50-day MA, spliced onto an equal-weight large-growth-mutual-fund basket (AGTHX/FCNTX/TRBCX/VWUSX, rescaled for continuity) for dates before FFTY's April-2015 inception. This is a *proxy* for the GMI's actual component 6, the proprietary **IBD Mutual Fund Index** — which has no public market ticker, though Dr. Wish reads it as symbol `0muti` inside IBD's own charting application ([WW 2009-01-12](../../raw/posts/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md)), so the series is identifiable and a faithful component 6 is obtainable by anyone with IBD access — and arguably a better one than a generic fund basket, though as the validation below shows it barely moves the GMI fit either way.

**How faithful is it?** `ww breadth validate` cross-checks the reconstruction against the GMI values Dr. Wish actually reported in his daily posts (the `gmi_value` column of `raw/timeline.parquet`, 890 overlapping dates).

*(Stats re-run 2026-07-02, after fixing a look-ahead bug found in a code review: `gmi()`'s price components 3/4/5 previously ignored the requested `date` and evaluated at the end of the price series, crediting every historical date with the present-day trend. The fix improved every fidelity metric — exact-match 20%→24%, correlation 0.60→0.66 — and eliminated the old "when he said 0–1 we computed 3–4" pathology, which turned out to be mostly that bug, not survivorship bias.)*

- **Exact-match rate: ≈ 24%** — our score equals his reported score on about 1 in 4 dates. (Swapping component 6's proxy to FFTY changed this by under 1 percentage point — the reconstruction's gap is driven by the *breadth* components, not component 6.)
- **Within ±1 rate: ≈ 73%** — within one point on almost three-quarters of dates.
- **Correlation: ≈ 0.66** — the reconstruction tracks the regime well, the precise level moderately.
- **Per-value breakdown** (when he said N, our score was): when he said 6, we computed 5 on ~208 dates and 6 on ~22; when he said 0, we now compute 0 on 11 of 15 dates (0–1 on 14 of 15). The remaining bias is *one notch low at the top* — his 5s and 6s often read 4–5 in the reconstruction, from one marginal component (e.g. the 50%-Successful-10-Day threshold or a daily-trend rule) sitting a hair on the wrong side of its cutoff, plus the survivorship-biased universe muting breadth extremes.
- **Representative side-by-sides**: 2005-09-28 his 2 / ours 1; 2007-01-18 his 5 / ours 5; 2007-06-04 his 6 / ours 5; 2007-10-17 his 5 / ours 5; 2007-12-13 his 4 / ours 3; 2008-03-26 his 3 / ours 3; 2008-04-21 his 5 / ours 4; 2008-12-03 his 6 / ours 1 (an outlier miss — a thin-panel day in the crash).

For T2108: the **nyse** universe flavor tracked his reported T2108 readings best — Pearson correlation ≈ 0.932, RMSE ≈ 10.7 percentage points, mean bias ≈ +4.4 (ours − his, reconstruction reads high). The broad-universe flavor has lower RMSE (≈ 9.9) but slightly lower correlation (≈ 0.930); both flavors read optimistically in past crashes.

**Documented limitations:** the universe is *not* Worden's TC2000 universe (it is the current Nasdaq+NYSE+AMEX common-stock listing from the Nasdaq Trader files, so it carries **survivorship bias** — stocks that delisted before today are largely absent, which makes the breadth series read systematically high in past crashes); component 6 is a proxy (FFTY since 2015, a growth-fund basket before); early-year coverage is thin. The key signal (GREEN vs RED regime) is captured reasonably: on 2008-10-10, the reconstruction computes T2108-equiv ≈ 1.7% (NYSE) / 2.9% (broad); on 2020-03-23 ≈ 1.1% / 2.8% — correctly flagging both as extreme-low regime, matching his documented single-digit readings. The validation numbers above are the honest measure of how close the reconstruction gets at the component level.

Run it: `ww compute gmi 2026-05-11 --breadth` for a full 0–6 GMI on any date the series covers; `ww gmi today` for a live daily reading (it runs `ww breadth update` first, then prints the breakdown).

## See also

- [QQQ Short-Term Timing](qqq-short-term-timing.md)
- [T2108](t2108.md)
- [Moving-average rules](moving-average-rules.md)
- [Market-state playbook](../playbooks/market-state.md)

## Sources

- [WW 2005-04-26 — About the General Market Index (GMI)](../../raw/posts/2005-04-26-general-market-index-gmi.md) ([summary](../sources/2005-04-26-general-market-index-gmi.md))
- [WW 2005-06-05 — GMI back to +5; on moving averages](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md) ([summary](../sources/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md))
- [WW 2005-07-17 — GMI since inception; introducing the WPM](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md) ([summary](../sources/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))
- [WW 2010-09-27 — Introducing Red White and Blue (RWB) Stocks](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md) ([summary](../sources/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md))
- [WW 2011-03-07 — Introducing the GMI2](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md) ([summary](../sources/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- [WW 2012-07-23 — Stage analysis and green line charts](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md) ([summary](../sources/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md) ([summary](../sources/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))
- [WW 2012-04-30 — How I find the next AAPL growth stock; new GMI buy signal](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md) ([summary](../sources/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))
- [WW 2023-06-19 — How I compute new US highs and lows; 11/2021 exit](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md) ([summary](../sources/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- [WW 2012-06-18 — 1990s trading diary; GMI buy-signal trigger confirmed](../../raw/posts/2012-06-18-an-excerpt-from-my-trading-diary-from-the-90s-market-at-critical-juncture.md) ([summary](../sources/2012-06-18-an-excerpt-from-my-trading-diary-from-the-90s-market-at-critical-juncture.md))
- [WW 2010-07-06 — Pension exit; topping-pattern scan; GMI=0](../../raw/posts/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md) ([summary](../sources/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md))
- [WW 2005-12-03 — Early GMI breadth details; breadth divergence signal; MCD trade](../../raw/posts/2005-12-03-gmi-6-wpm-shows-a-little-dow-30-deterioration-correlation-of-some-indicators-with-s-mcd-break-out-jnj-sick.md) ([summary](../sources/2005-12-03-gmi-6-wpm-shows-a-little-dow-30-deterioration-correlation-of-some-indicators-with-s-mcd-break-out-jnj-sick.md))
- [WW 2005-11-13 — GMI historical track record chart; Cramer vs charts argument](../../raw/posts/2005-11-13-gmi6-my-favorite-posts-gmi-as-a-trend-indicator-wpm-shows-all-indexes-strong-jim-cramer-on-charts-some-big-ea.md) ([summary](../sources/2005-11-13-gmi6-my-favorite-posts-gmi-as-a-trend-indicator-wpm-shows-all-indexes-strong-jim-cramer-on-charts-some-big-ea.md))
- [WW 2006-02-06 — Darvas/Wyckoff noise isolation; GMI-S short-term sub-index](../../raw/posts/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md) ([summary](../sources/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md))
- [WW 2008-08-22 — Component 6 negative since mid-June; QQQQ up-trend distrusted](../../raw/posts/2008-08-22-gmi-3-gmi-r-5-12th-day-of-qqqq-up-trend-still-cautious.md)
- [WW 2009-01-12 — GMI component 6 named and sourced (0muti); GMI-R "more sensitive"](../../raw/posts/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md) ([summary](../sources/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md))
- [WW 2023-08-09 — Component 6 could flip the GMI to Red; SQQQ accumulation](../../raw/posts/2023-08-09-blog-post-day-1-of-new-qqq-short-term-down-trend-and-gmi3-many-fallen-angels-smci-aapl-cmg-buying-sqqq-now-bu.md)
- [WW 2025-12-14 — Component 6 (0MUTI) still live and now negative; FFTY daily BWR](../../raw/posts/2025-12-14-blog-post-day-11-of-qqq-short-term-up-trend-it-could-end-on-monday-ibd-50-type-growth-stocks-are-in-a-bwr-dow.md) ([summary](../sources/2025-12-14-blog-post-day-11-of-qqq-short-term-up-trend-it-could-end-on-monday-ibd-50-type-growth-stocks-are-in-a-bwr-dow.md))
- [WW 2007-08-20 — GMI performance through the 2007 declines; exit/re-entry thresholds; GMI-S construction](../../raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md) ([summary](../sources/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md))
- [WW 2007-09-17 — IBD100 survivorship bias; 30-day average as a GMI input](../../raw/posts/2007-09-17-gmi-5-ibd100-stocks-not-good-for-buy-and-hold.md) ([summary](../sources/2007-09-17-gmi-5-ibd100-stocks-not-good-for-buy-and-hold.md))
- [WW 2007-10-29 — At the October 2007 top; GMI-L at 94%; "greater than 2" threshold](../../raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md) ([summary](../sources/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md))
- [WW 2007-11-19 — Weekly QQQQ Index as primary long-term indicator; 2000 exit attributed](../../raw/posts/2007-11-19-gmi1gmi-r1-qqqq-bounce-off-support-too-many-bears-new-leaders.md) ([summary](../sources/2007-11-19-gmi1gmi-r1-qqqq-bounce-off-support-too-many-bears-new-leaders.md))
- [WW 2007-12-17 — GMI-L at 31%: the pre-2008 warning](../../raw/posts/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md) ([summary](../sources/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md))
- [WW 2007-05-22 — Covered calls; QLD over stock-picking; posting cadence](../../raw/posts/2007-05-22-gmi-6-no-longer-post-daily-but-when-gmi-changes-the-ideal-boomer-strategy-writing-covered-calls.md) ([summary](../sources/2007-05-22-gmi-6-no-longer-post-daily-but-when-gmi-changes-the-ideal-boomer-strategy-writing-covered-calls.md))
- [WW 2013-01-07 — GMI table: GMI2 at 6 components; T2108 band 80/25](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md)
- [WW 2020-01-05 — GMI table: GMI2 grown to 8; MACD breadth row](../../raw/posts/2020-01-05-my-pet-stocks-frpt-and-pawz.md)
- [WW 2026-01-04 — GMI table: verbatim component labels; GMI2 at 9](../../raw/posts/2026-01-04-blog-post-day-1-of-qqq-short-term-down-trend-gmi2-and-could-turn-red-on-monday-qqq-has-now-closed-below-its-1.md)
- [WW 2015-02-22 — An important limitation of the GMI signals](../../raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md) ([summary](../sources/2015-02-22-an-important-limitation-of-the-gmi-signals.md))
