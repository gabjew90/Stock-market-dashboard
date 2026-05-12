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
  - raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md
  - raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md
  - raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md
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

## The 4-week / 10-week / 30-week alignment — a weekly stock rule

In the weekly green bar system, the three-MA ladder must be aligned: **4wk > 10wk > 30wk** (4-week average above the 10-week, which is above the 30-week). This alignment began for ANF in mid-June 2023 and held through April 2024. During that period ANF never closed below its 10-week average. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))

The 4-week average (red dot on his weekly chart) is the closer trailing support — it gives more frequent bounce-entry opportunities than the 10-week average. He uses weekly green bars (price bars where the current close is above the 4-week average) as entry signals.

## The daily RWB chart — a finer-grained tool

Introduced / formalized by March 2017. In addition to the weekly GMMA, Dr. Wish uses a **daily** version of the 12-exponential-MA chart. The shorter-term averages (6 red EMAs) and longer-term averages (6 blue EMAs) are the same construction on a daily timeframe. He adds:

- **Red Line Count (RLC):** the count (0–6) of red lines that the daily close is above. Displayed on the chart header. RLC = 6 = full bullish; RLC = 0 = below all red lines (caution). ([WW 2017-03-19](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))
- **Purple dots:** a plot of each day's low price, shown as purple dots below the candles. These visualize where daily support has been and help identify where to place stops. ([WW 2017-03-19](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))
- The **lowest red line** (the 15-day EMA, shown in large digits on the chart) is the specific dollar-level stop. If the stock closes below that value, the red line signal is broken. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))

The weekly chart shows the longer-term trend but is too slow for timing entries and exits — that is the reason he shifted to daily RWB charts for timing. ([WW 2017-03-19](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))

## See also

- [General Market Index (GMI)](gmi.md) — the 30-week average is one GMI component
- [QQQ Short-Term Timing](qqq-short-term-timing.md)
- [Green Line Breakouts (GLB)](green-line-breakouts.md) — Stage 2 is the prerequisite
- [Stock selection](stock-selection.md) — RWB pattern; daily RWB scan; weekly green bar
- [Exits (playbook)](../playbooks/exits.md)

## Sources

- [WW 2005-04-23 — Let's Talk Strategy](../../raw/posts/2005-04-23-lets-talk-strategy.md) ([summary](../sources/2005-04-23-lets-talk-strategy.md))
- [WW 2005-06-05 — GMI back to +5; on moving averages](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md) ([summary](../sources/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md))
- [WW 2005-07-17 — GMI since inception; introducing the WPM](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md) ([summary](../sources/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))
- [WW 2012-07-23 — Stage analysis and green line charts](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md) ([summary](../sources/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md) ([summary](../sources/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))
- [WW 2017-03-19 — How I use daily RWB charts to size up the market and individual stocks](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md) ([summary](../sources/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))
- [WW 2017-12-17 — A strategy for deciding when to sell stocks; GDS, NVDA](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md) ([summary](../sources/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- [WW 2024-05-27 — ANF worked example (weekly green bar)](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md) ([summary](../sources/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
