---
title: The GMI family — GMI-S, GMI-L, GMI-R, GMI2 and the rest of the daily table
type: concept
updated: 2026-08-18
sources:
  - raw/posts/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md
  - raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md
  - raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md
  - raw/posts/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md
  - raw/posts/2008-04-21-gmi-5-gmi-r-9-my-general-market-index-gmi-catches-trend-changes-again-more-judys-picks-itri-and-imax.md
  - raw/posts/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md
  - raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md
  - raw/posts/2020-01-05-my-pet-stocks-frpt-and-pawz.md
  - raw/posts/2026-01-04-blog-post-day-1-of-qqq-short-term-down-trend-gmi2-and-could-turn-red-on-monday-qqq-has-now-closed-below-its-1.md
---

# The GMI family — GMI-S, GMI-L, GMI-R, GMI2 and the rest of the daily table

The [GMI](gmi.md) proper is a fixed 0–6 count. Around it Dr. Wish has built and retired a set of companion indexes — **GMI-S** (a short-term 0–100 sub-index, 2005), **GMI-L** (a long-term weekly measure, 2006), **GMI-R** (a 10-component superset, 2007–2011), and **GMI2** (a companion count that has grown from 6 to 9 components since 2011) — plus the other columns the daily table has carried over the years. None of them has decision rules attached ("I do not have decision rules based in the GMI-R or the new GMI2"); they are the dashboard around the signal. This page holds all of them, in the order they appeared. The GMI itself — its six components, Buy/Sell rules, and code — stays on [gmi.md](gmi.md); the evidence trail for how the components were recovered is on [gmi-evidence](gmi-evidence.md).

## 2005-2006 — GMI-S (short-term sub-index, 0–100 scale)

Dr. Wish occasionally published a **GMI-S** alongside the GMI. The GMI-S measures short-term breadth on a 0–100 scale. A rapid fall from GMI-S=75 to GMI-S=31 in a single week (February 2006) signalled deterioration in the underlying breadth even when the overall GMI (at +4) had not yet dropped decisively. ([WW 2006-02-06](../../raw/posts/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md))

**Its construction is disclosed in 2007**, contrary to what this page previously said: "Only one of the **16 short term indicators for the IJR, DIA, SPY and QQQQ** is positive (GMI-S: 6%)" — 1/16 ≈ 6%. So the GMI-S is the percentage of sixteen short-term indicators, four applied to each of four index ETFs (small-cap IJR, Dow DIA, S&P SPY and Nasdaq QQQQ), that are currently positive. The individual sixteen are not named. ([WW 2007-08-20](../../raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md))

## GMI-S — construction fully visible in the table

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

## 2006-2007 — GMI-L (long-term measure of weekly trends, reported as a %)

A **GMI-L** appears throughout the 2007 posts and is absent from the wiki's earlier accounts. He defines it in passing as "my longer term measure of weekly trends," reported as a percentage positive, and reads it as the slow counterpart to the GMI-S. ([WW 2007-12-17](../../raw/posts/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md))

Its diagnostic value is in the comparison across episodes. In December 2007 it fell to **31%** — "the lowest since it hit 20% in August, **2006**, near the bottom of that four month decline" — and crucially, "in the two declines in 2007 (March and August), the GMI-L never fell below 50%." A GMI-L below 50% therefore separated a correction from what became the 2008 bear market. Six weeks earlier, days after the October 2007 top, it had still read **94%**. ([WW 2007-10-29](../../raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md), [WW 2007-12-17](../../raw/posts/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md))

Like the GMI-S, the component list is undisclosed, and like the GMI-S it disappears from the daily posts after the typepad era. Both are reported as percentages, as is the GMI-R (80% = 8 of 10).

## 2007 — threshold variation

The GMI's action thresholds are not stated identically across posts, and the wiki records the variation rather than picking one:

| Date | Stated rule |
|---|---|
| 2007-08-20 | "exit the long side... when the GMI falls below 4 and... buy once it climbs back above 3" ([WW 2007-08-20](../../raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md)) |
| 2007-10-29 | "I will trade long in the market as long as the GMI is **greater than 2**" ([WW 2007-10-29](../../raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md)) |
| 2011-03-07 | "I like to be long if the GMI is 4 or more... When it declines to 3 or below, I get defensive" ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)) |
| 2012-04-30 | Buy signal = GMI > 3 on two consecutive days ([WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md)) |

The ≥4 / ≤3 reading is the dominant and durable one; the October 2007 "greater than 2" appears to be a looser stance taken mid-up-trend rather than a redefinition. The [backtest](backtest-timing-overlay.md) uses ≥4 long / ≤3 cash.

## Intermediate — GMI-R (10 components), with its four extra indicators named

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

## The dashboard in live use — April 2008

The clearest snapshot of all four composites working together, during the April 2008 bear-market
rally: **GMI 5, GMI-R 9, GMI-S 100%, GMI-L 50%** — "all 16 short term indicators for four key
index ETF's are positive" while "the major longer term trend is still down" (the Weekly QQQQ
Index was the lone GMI holdout). Read with hindsight the slow indicators were right; the 2008
collapse followed. This is the fast/slow split that later became the formal GMI-vs-GMMA
two-speed design. ([WW 2008-04-21](../../raw/posts/2008-04-21-gmi-5-gmi-r-9-my-general-market-index-gmi-catches-trend-changes-again-more-judys-picks-itri-and-imax.md))

## 2011 → 2026 — GMI2: a *growing* companion index, not a fixed 6

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

## See also

- [General Market Index (GMI)](gmi.md) — the core index; the page this was split from
- [GMI evidence](gmi-evidence.md) — the published tables, the 2013 signal record, the 2016 audit, the image problem
- [T2108](t2108.md) · [QQQ short-term timing](qqq-short-term-timing.md) — the two table columns with their own pages
- [Glossary](glossary.md) — GMI-S, GMI-L, GMI-R, GMI2, GMI table, 0muti, MACD breadth

## Sources

- [WW 2006-02-06 — Darvas/Wyckoff noise isolation; GMI-S short-term sub-index](../../raw/posts/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md) ([summary](../sources/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md))
- [WW 2007-08-20 — GMI performance through the 2007 declines; exit/re-entry thresholds; GMI-S construction](../../raw/posts/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md) ([summary](../sources/2007-08-20-gmi-1-more-new-highs-than-lows-performance-of-gmi-strongest-ibd100-stocks.md))
- [WW 2007-10-29 — At the October 2007 top; GMI-L at 94%; "greater than 2" threshold](../../raw/posts/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md) ([summary](../sources/2007-10-29-gmi-4-gmi-r-8-gmi-performance-judys-pick-cytr.md))
- [WW 2007-12-17 — GMI-L at 31%: the pre-2008 warning](../../raw/posts/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md) ([summary](../sources/2007-12-17-gmi-0-gmi-r-0-gmi-l-31-why-fight-the-odds.md))
- [WW 2008-04-21 — The 2000 pension exit in dollars; GMI-S at 100% inside a bear](../../raw/posts/2008-04-21-gmi-5-gmi-r-9-my-general-market-index-gmi-catches-trend-changes-again-more-judys-picks-itri-and-imax.md) ([summary](../sources/2008-04-21-gmi-5-gmi-r-9-my-general-market-index-gmi-catches-trend-changes-again-more-judys-picks-itri-and-imax.md))
- [WW 2009-01-12 — GMI component 6 named and sourced (0muti); GMI-R "more sensitive"](../../raw/posts/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md) ([summary](../sources/2009-01-12-gmi-error-3-since-december-30-gmi-r-4-qqqq-back-near-support.md))
- [WW 2011-03-07 — Introducing the GMI2](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md) ([summary](../sources/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- [WW 2012-04-30 — How I find the next AAPL growth stock; new GMI buy signal](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md) ([summary](../sources/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))
- [WW 2013-01-07 — GMI table: GMI2 at 6 components; T2108 band 80/25](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md)
- [WW 2020-01-05 — GMI table: GMI2 grown to 8; MACD breadth row](../../raw/posts/2020-01-05-my-pet-stocks-frpt-and-pawz.md)
- [WW 2026-01-04 — GMI table: verbatim component labels; GMI2 at 9](../../raw/posts/2026-01-04-blog-post-day-1-of-qqq-short-term-down-trend-gmi2-and-could-turn-red-on-monday-qqq-has-now-closed-below-its-1.md)
