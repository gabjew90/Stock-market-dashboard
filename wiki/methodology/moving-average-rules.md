---
title: Moving-average rules
type: entity
updated: 2026-05-11
sources:
  - raw/posts/2005-04-23-lets-talk-strategy.md
  - raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md
  - raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md
  - raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
---

# Moving-average rules

The moving-average logic Dr. Wish applies to market indices and individual stocks. The core framework comes from Stan Weinstein's stage analysis, applied principally with the 30-week (long-term) and 10-week (medium-term) simple moving averages.

## Three rules for any moving average

Dr. Wish lays out these principles explicitly, treating a moving average as a statistical sample of closes ([WW 2005-06-05](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md)):

1. **Pick the right period.** Choose the number of days/weeks that has actually worked for tracking that stock's or index's prior trends — not 50 or 200 days by tradition.
2. **Price must be above the MA.** A stock should be closing today above the average of its closes over the chosen window.
3. **The MA must be rising.** A rising MA means today's close is higher than the close being dropped from the window (the close N+1 days ago). A flat or declining MA is a warning sign.

He prefers **simple** (equal-weighted) moving averages; exponential weighting "contradicts the whole idea that we are just computing the average of a sample of closes." ([WW 2005-06-05](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md))

## The 30-week average — the long-term trend anchor

The most important moving average in Dr. Wish's toolkit. He credits Weinstein's classic book for alerting him to it. The 30-week average of a market index (QQQ, SPY, or the Dow) crossing from up to down signals a major bear market; reversing back up signals a bull market re-entry.

- The reversal of the QQQQ's 30-week average in **2000** signalled him to exit the market. Its reversal back up in **2003** signalled re-entry. ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))
- When the QQQ or SPY closes below the 30-week average, he becomes "very defensive": no new buys, raise stops. If the average eventually turns down, he typically exits the market. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- One of the six [GMI](gmi.md) components is whether the QQQ has closed above its 30-week average. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))

### Stage 2 (the only stage he buys)

Stage analysis was introduced by Weinstein and adopted by Dr. Wish. A stock (or index) in **Stage 2** is following along its **rising 30-week average** — the price is above it, the average is rising. This is the only condition under which Dr. Wish buys long: "I only buy long when the market is in a Stage 2 up-trend and if the stock or ETF I am buying is also in a Stage 2 up-trend." ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))

*Note: the other stages (1 = basing, 3 = topping, 4 = declining) are referenced but not defined in the posts ingested so far.*

## The 30-day average — the short-term trend anchor

Dr. Wish calls the 30-day moving average "the most reliable indicator of the short term trend." The WishingWealth Pulse of the Market (WPM) tracks whether each major index is above its 30-day average, and what percentage of component stocks are above it. ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))

## The 10-week average — the holding rule for individual stocks

For individual stocks, a weekly close below the **rising 10-week average** is an exit signal. He is explicit about this with AAPL as an example: "I have found AAPL fine to own as long as it remained above its rising 10 week average." A weekly close below that level is a concern; he uses it to decide when to exit a position. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

## The RWB pattern — multiple MAs on a weekly chart

For stock selection, Dr. Wish also uses the weekly GMMA (Guppy Multiple Moving Average) chart with the Red White Blue (RWB) pattern: shorter-term MAs (red) above longer-term MAs (blue) with white space between them. See [stock-selection.md](stock-selection.md) for the full description.

## See also

- [General Market Index (GMI)](gmi.md) — the 30-week average is one GMI component
- [QQQ Short-Term Timing](qqq-short-term-timing.md)
- [Green Line Breakouts (GLB)](green-line-breakouts.md) — Stage 2 is the prerequisite
- [Stock selection](stock-selection.md) — RWB pattern
- [Exits (playbook)](../playbooks/exits.md)

## Sources

- [WW 2005-04-23 — Let's Talk Strategy](../../raw/posts/2005-04-23-lets-talk-strategy.md)
- [WW 2005-06-05 — GMI back to +5; on moving averages](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md)
- [WW 2005-07-17 — GMI since inception; introducing the WPM](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md)
- [WW 2012-07-23 — Stage analysis and green line charts](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md)
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)
