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
  - raw/posts/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md
  - raw/posts/2016-01-10-all-world-stock-markets-entering-bwr-down-trends-i-am-in-cash-and-scared-and-monitoring-t2108.md
  - raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md
  - raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md
  - raw/posts/2018-11-25-im-back-daily-bwr-pattern-for-qqq-weekly-rwb-pattern-gone-content-to-be-on-sidelines.md
  - raw/posts/2020-12-27-blog-post-buying-ipos-with-green-line-break-outs-glb-and-a-weekly-green-bar-wgb-signal-pgny-tsla.md
  - raw/posts/2021-02-28-blog-post-twtr-to-take-off-an-example-of-how-i-use-tc2000-and-my-glb-and-wgb-indicators-to-find-promising-sto.md
  - raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md
  - raw/posts/2025-03-30-blog-post-day-24-of-qqq-short-term-down-trend-iwm-looks-like-it-is-at-the-beginning-of-a-stage-4-down-trend-s.md
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

### The four stages

Stage analysis was introduced by Weinstein and adopted by Dr. Wish. The four stages are defined by price's relationship to the 30-week average:

- **Stage 1 — Basing.** The stock is consolidating near or below its 30-week average after a prior decline. The average is roughly flat. Dr. Wish does not buy in Stage 1.
- **Stage 2 — Advancing.** The stock is above its rising 30-week average. "I only buy long when the market is in a Stage 2 up-trend and if the stock or ETF I am buying is also in a Stage 2 up-trend." ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md)) This is the only stage in which he buys long.
- **Stage 3 — Topping.** The stock has stopped advancing and is consolidating near a peak while the 30-week average flattens or begins to turn down. He sells into Stage 3.
- **Stage 4 — Declining.** The stock (or index) is below its declining 30-week average. "If they remain below these averages and the averages turn down, the market could be at the beginning of a major Stage 4 decline." ([WW 2014-10-13](../../raw/posts/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md)) He transfers pension money out of mutual funds in stages when a Stage 4 threatens. The 10-week average crossing below the 30-week average confirms the Stage 4 onset. ([WW 2025-03-30](../../raw/posts/2025-03-30-blog-post-day-24-of-qqq-short-term-down-trend-iwm-looks-like-it-is-at-the-beginning-of-a-stage-4-down-trend-s.md))

**2025 example:** IWM's weekly chart in March 2025 showed the 10-week average crossing below the 30-week average while the weekly close (gray line) was leading everything lower — Dr. Wish called this "the BEGINNING of a Stage 4 down-trend," comparing it to a similar chart setup in 2022. ([WW 2025-03-30](../../raw/posts/2025-03-30-blog-post-day-24-of-qqq-short-term-down-trend-iwm-looks-like-it-is-at-the-beginning-of-a-stage-4-down-trend-s.md))

## The 30-day average — the short-term trend anchor

Dr. Wish calls the 30-day moving average "the most reliable indicator of the short term trend." The WishingWealth Pulse of the Market (WPM) tracks whether each major index is above its 30-day average, and what percentage of component stocks are above it. ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))

## The 10-week average — the holding rule for individual stocks

For individual stocks, a weekly close below the **rising 10-week average** is an exit signal. He is explicit about this with AAPL as an example: "I have found AAPL fine to own as long as it remained above its rising 10 week average." A weekly close below that level is a concern; he uses it to decide when to exit a position. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

## The RWB / BWR patterns — multiple MAs on a Guppy chart

For stock selection, Dr. Wish uses the weekly GMMA (Guppy Multiple Moving Average) chart. The chart overlays 12 exponential moving averages — a band of 6 shorter-term averages shown in red, and a band of 6 longer-term averages shown in blue. A gray dotted line shows the weekly closing price.

- **RWB (Red White Blue):** shorter-term red averages are above the longer-term blue averages, with white space between them; both sets are rising. This is the rocket/bull pattern. ([WW 2010-09-27](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md))
- **BWR (Blue White Red):** the reverse — red averages are below the blue averages; the gray dotted line (weekly close) is below all 12 averages; both bands declining. This is the submarine/bear pattern. ([WW 2018-11-25](../../raw/posts/2018-11-25-im-back-daily-bwr-pattern-for-qqq-weekly-rwb-pattern-gone-content-to-be-on-sidelines.md))

**Precision (2016):** a BWR is fully confirmed when the weekly close (gray dotted line) is below all 12 moving averages. A first sign of a new up-trend would be the gray dotted line closing back above all 12 averages — though Dr. Wish prefers to see the full RWB pattern develop before trading big on a trend change. ([WW 2016-01-10](../../raw/posts/2016-01-10-all-world-stock-markets-entering-bwr-down-trends-i-am-in-cash-and-scared-and-monitoring-t2108.md))

**Global applicability:** the RWB/BWR framework applies to index ETFs of any country, not just US stocks. In January 2016, Dr. Wish scanned 37 world market ETFs and found 35 of 37 in BWR down-trends. ([WW 2016-01-10](../../raw/posts/2016-01-10-all-world-stock-markets-entering-bwr-down-trends-i-am-in-cash-and-scared-and-monitoring-t2108.md))

**Transition phases:** when the prior RWB pattern has ended but BWR is not yet formed (the white separation is gone), Dr. Wish is on the sidelines, waiting for direction to emerge. The 2018 Q4 decline illustrates this: the weekly QQQ had lost its RWB pattern but not yet fully formed a BWR. ([WW 2018-11-25](../../raw/posts/2018-11-25-im-back-daily-bwr-pattern-for-qqq-weekly-rwb-pattern-gone-content-to-be-on-sidelines.md))

See [stock-selection.md](stock-selection.md) for the full description of how RWB is used in stock screening.

## The 4-week / 10-week / 30-week alignment — a weekly stock rule

In the weekly green bar system, the three-MA ladder must be aligned: **4wk > 10wk > 30wk** (4-week average above the 10-week, which is above the 30-week). This alignment began for ANF in mid-June 2023 and held through April 2024. During that period ANF never closed below its 10-week average. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))

The 4-week average (red dot on his weekly chart) is the closer trailing support — it gives more frequent bounce-entry opportunities than the 10-week average. He uses weekly green bars (WGBs) as entry signals.

### WGB (Weekly Green Bar) — the TC2000 formula

The precise TC2000 formula for the WGB scan, stated in the 2021-02-28 post ([WW 2021-02-28](../../raw/posts/2021-02-28-blog-post-twtr-to-take-off-an-example-of-how-i-use-tc2000-and-my-glb-and-wgb-indicators-to-find-promising-sto.md)):

```
avgc4>avgc10 and avgc10>avgc30
L<=avgc4 and C>avgc4
C>C1
avgc4>avgc4.1
```

All conditions are on the **weekly** timeframe. In plain terms: (1) 4wk>10wk>30wk alignment; (2) the low for the week traded at or below the 4wk average but the close is above it; (3) the close is higher than the prior week; (4) the 4wk average is rising (today's 4wk > last week's 4wk).

### WGB trailing stop rule

Dr. Wish uses successive WGBs as a trailing stop mechanism:

1. On the first WGB entry (or after a GLB), place the initial stop at the low of that WGB.
2. After each new WGB, raise the stop to the low of the new WGB.
3. Exit when the stock trades below the most recent WGB low.

This approach captured most of the advance in TSLA after its GLB: 6 of 8 WGBs were successful entry/hold points. ([WW 2020-12-27](../../raw/posts/2020-12-27-blog-post-buying-ipos-with-green-line-break-outs-glb-and-a-weekly-green-bar-wgb-signal-pgny-tsla.md))

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
- [WW 2014-10-13 — 11th day of QQQ down-trend; how long will this decline last?](../../raw/posts/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md) ([summary](../sources/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md))
- [WW 2016-01-10 — All world stock markets entering BWR down-trends](../../raw/posts/2016-01-10-all-world-stock-markets-entering-bwr-down-trends-i-am-in-cash-and-scared-and-monitoring-t2108.md) ([summary](../sources/2016-01-10-all-world-stock-markets-entering-bwr-down-trends-i-am-in-cash-and-scared-and-monitoring-t2108.md))
- [WW 2017-03-19 — How I use daily RWB charts to size up the market and individual stocks](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md) ([summary](../sources/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))
- [WW 2017-12-17 — A strategy for deciding when to sell stocks; GDS, NVDA](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md) ([summary](../sources/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- [WW 2018-11-25 — I'm back! Daily BWR pattern for $QQQ, weekly RWB pattern gone](../../raw/posts/2018-11-25-im-back-daily-bwr-pattern-for-qqq-weekly-rwb-pattern-gone-content-to-be-on-sidelines.md) ([summary](../sources/2018-11-25-im-back-daily-bwr-pattern-for-qqq-weekly-rwb-pattern-gone-content-to-be-on-sidelines.md))
- [WW 2020-12-27 — Buying IPOs with GLB and WGB signal; $PGNY $TSLA](../../raw/posts/2020-12-27-blog-post-buying-ipos-with-green-line-break-outs-glb-and-a-weekly-green-bar-wgb-signal-pgny-tsla.md) ([summary](../sources/2020-12-27-blog-post-buying-ipos-with-green-line-break-outs-glb-and-a-weekly-green-bar-wgb-signal-pgny-tsla.md))
- [WW 2021-02-28 — $TWTR: GLB and WGB indicators](../../raw/posts/2021-02-28-blog-post-twtr-to-take-off-an-example-of-how-i-use-tc2000-and-my-glb-and-wgb-indicators-to-find-promising-sto.md) ([summary](../sources/2021-02-28-blog-post-twtr-to-take-off-an-example-of-how-i-use-tc2000-and-my-glb-and-wgb-indicators-to-find-promising-sto.md))
- [WW 2024-05-27 — ANF worked example (weekly green bar)](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md) ([summary](../sources/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
- [WW 2025-03-30 — Day 24 of QQQ down-trend; IWM at beginning of Stage 4](../../raw/posts/2025-03-30-blog-post-day-24-of-qqq-short-term-down-trend-iwm-looks-like-it-is-at-the-beginning-of-a-stage-4-down-trend-s.md) ([summary](../sources/2025-03-30-blog-post-day-24-of-qqq-short-term-down-trend-iwm-looks-like-it-is-at-the-beginning-of-a-stage-4-down-trend-s.md))
