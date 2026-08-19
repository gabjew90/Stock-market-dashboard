---
title: Playbook — buying a Green Line Breakout
type: playbook
updated: 2026-08-18
sources:
  - raw/posts/2021-01-24-blog-post-in-the-60s-i-used-to-receive-a-book-containing-monthly-charts-of-stocks-i-noticed-that-stocks-that.md
  - raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md
  - raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md
  - raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md
  - raw/posts/2010-02-22-how-to-use-ibd-100-and-new-america-stocks-and-tc2007-to-find-potential-rocket-stocks-market-rally-begun.md
  - raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md
  - raw/posts/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md
  - raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md
  - raw/posts/2005-04-30-my-trading-strategy-part-ii.md
  - raw/posts/2023-04-24-blog-post-day-26-of-qqq-short-term-up-trend-wing-flies-to-ath-how-i-missed-the-glb-true-confessions-and-see-m.md
  - raw/posts/2005-04-23-lets-talk-strategy.md
  - raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md
  - raw/posts/2010-04-19-how-i-buy-aapl-for-12-down-without-using-margin.md
  - raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md
  - raw/posts/2022-08-25-blog-post-day-28-of-qqq-short-term-up-trend-qqq-very-oversold-and-bounce-likely-glb-clh-how-i-buy-a-glb-autom.md
---

# Playbook — buying a Green Line Breakout

The mechanical checklist for entering a GLB. This playbook combines the GLB definition, the market-state gate, the stock-selection filter, and the specific entry and initial stop mechanics.

## Inputs

- [Green Line Breakouts (GLB)](../methodology/green-line-breakouts.md) — definition and identification
- [Stock selection](../methodology/stock-selection.md) criteria — RWB, fundamentals
- Market state ([GMI](../methodology/gmi.md) GREEN?)
- [Moving-average rules](../methodology/moving-average-rules.md) — Stage 2, 30-week, 10-week

---

## Step 1 — Confirm the market gate

Only enter GLBs when the market is in an uptrend. Specifically:

- [GMI](../methodology/gmi.md) ≥ 4 (GREEN). A GMI buy signal = GMI > 3 on two consecutive days. ([WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))
- QQQ/SPY is in Stage 2 (above its rising 30-week average). ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- Ideally a [QQQ Short-Term Timing](../methodology/qqq-short-term-timing.md) up-trend is also active.

"The best rules for picking stocks will fail in an adverse market environment." ([WW 2005-04-30](../../raw/posts/2005-04-30-my-trading-strategy-part-ii.md))

---

## Step 2 — Identify the GLB candidate

**Find the candidates:**
1. Run a scan for stocks at a new 52-week high.
2. Pull up the monthly chart for each; look for a horizontal green line at the prior all-time high level.
3. The stock must have held below that high for **≥ 3 months** (the green line is drawn there). ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
4. Today's price must be breaking above that green line — the first new all-time high after the base.

**Alternative scan approach (2010):**
Starting from the universe of 4,000+ stocks, sort by new 52-week high, then filter down to those near their 10-year all-time high. Apply fundamental filter: quarterly earnings ≥ 30% OR revenue growth ≥ 12%. Cross-check against the IBD 100 / IBD 50 / New America lists for further confidence. ([WW 2010-02-22](../../raw/posts/2010-02-22-how-to-use-ibd-100-and-new-america-stocks-and-tc2007-to-find-potential-rocket-stocks-market-rally-begun.md))

**Alternative scan approach (2017 — daily RWB bounce):**
Find stocks that (a) are in a daily RWB up-trend, (b) recently closed below all six red lines (a dip), and (c) have now recovered above all six red lines. This identifies RWB stocks resuming their advance after a pullback. The scan also requires the stock to be above its last green line top — any stock not above its last ATH has overhead supply and is filtered out. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))

---

## Step 3 — Check the stock's own trend (RWB / Stage 2)

The stock itself must be in an uptrend:

- **Weekly chart:** the stock should be in an RWB up-trend — shorter-term averages (red) above longer-term averages (blue) with white space between them, both rising. ([WW 2010-09-27](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md))
- **Stage 2:** the stock is above its rising 30-week average. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- **4wk > 10wk > 30wk alignment** on the weekly chart (the moving average ladder). ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
- **Weekly stochastic ≥ 80** (for the weekly green bar setup): the stock is closing near the top of its 10-week range, which is the desired condition — not overbought, just strong. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))

---

## Step 4 — Entry

Make a **pilot buy** (a small initial position) at or near the GLB level. ([WW 2005-04-23](../../raw/posts/2005-04-23-lets-talk-strategy.md)) ([WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))

"I make a small pilot buy of such a stock and place a stop loss below the break-out level. If the stock continues to rise, I will add to my position and raise my stop. I love to pay more for a stock that I have already bought. I never average down." ([WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))

He also watches the GLB for the highest weekly volume since the prior high (a sign of institutional demand). ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))

---

## Step 5 — Set the initial stop immediately — but for a GLB, on a *close* basis

Two rules that look contradictory and are not:

- **General rule (2010, all positions):** decide the exit level *before* buying, and as soon as the order fills place a **GTC stop-loss order** there — "once I have my stop loss order in place, I have taken my emotion out of the trade," and part-time traders who are not watching the screen are precisely the ones who need the automatic order. ([WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))
- **GLB-specific override (2021):** for a GLB he does **not** enter the stop as a resting order — "I do not set a stop loss for a GLB to avoid being sold out when a stock trades intraday below the green line only to close the day above it." The exit level is the same (just under the green line) but it is a **mental stop evaluated on the close**: if the stock *closes* below the green line, sell — "no hesitation or remorse." ([WW 2021-01-24](../../raw/posts/2021-01-24-blog-post-in-the-60s-i-used-to-receive-a-book-containing-monthly-charts-of-stocks-i-noticed-that-stocks-that.md), [WW 2018-05-20](../../raw/posts/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md))

So: the *level* is fixed before the buy in every case; whether it is a resting GTC order or a close-of-day check depends on the setup. Breakout levels attract intraday probes, which is why the GLB gets the close-basis exception; an [OSB](buying-osb.md) stop under the bounce low is placed as an order immediately. If the GLB fails on a close, exit with a small loss.

---

**Buying a GLB you cannot watch.** The entry problem has a Darvas answer he restates in 2022, with CLH approaching a GLB at $118.89: "how could I buy it if it traded through that price without being glued to my monitor? Nicolas Darvas had the answer… Once he had figured out a possible break-out price he had his broker enter a **good til cancelled buy stop order**. This meant that as soon as the stock traded at the price he specified his order to buy shares was entered as a market order. Darvas said that the buy stop order was a critical tool for him." ([WW 2022-08-25](../../raw/posts/2022-08-25-blog-post-day-28-of-qqq-short-term-up-trend-qqq-very-oversold-and-bounce-likely-glb-clh-how-i-buy-a-glb-autom.md))

## Step 6 — Monitor and add to the position

If the stock holds above the red lines on the daily RWB chart and continues advancing:

- Raise the stop as the stock advances.
- Add to the position only as it moves *in your favor* — average up, never down.
- For the weekly green bar system: add at the next bounce off the rising 4-week average with a green bar. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
- Re-entry at the 4-week or 10-week MA during the subsequent advance is acceptable after the initial GLB, provided a reasonable stop is set. ([WW 2018-05-20](../../raw/posts/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md))

### Exit rules for a GLB position

- **Initial stop:** as in Step 5 — sell if the stock *closes* below its green line (mental stop, close basis; no resting order for a GLB). "No hesitation or remorse" — the primary reason for the position has failed. ([WW 2018-05-20](../../raw/posts/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md))
- **Failed GLB, then buy-back:** after exiting a failed GLB, watching for a new confirmed GLB on the same stock is explicitly encouraged. No ego — a stock previously researched and evaluated can be bought back. ([WW 2018-05-20](../../raw/posts/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md))
- **Pyramided position hold rule:** if a GLB position is successfully pyramided (averaged up over multiple entries as the stock advances), Dr. Wish suggests holding until the stock "closes below its rising 30 week average." This is a longer, more patient exit than the green-line mental stop that applies at the initial entry level. ([WW 2018-05-20](../../raw/posts/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md))

---

## Dr. Wish's published GLB rules (student checklist)

Written and published in April 2023 after missing the WING breakout — these are his own words condensed into a six-step checklist for students, with the Turtle Traders behavioral principle appended. ([WW 2023-04-24](../../raw/posts/2023-04-24-blog-post-day-26-of-qqq-short-term-up-trend-wing-flies-to-ath-how-i-missed-the-glb-true-confessions-and-see-m.md))

1. Draw a green line at a stock's peak once it has not been surpassed for **at least 3 months**.
2. Set a **TC2000 price alert** (valid 1 year) to notify you when the stock trades back above the green line (delivered as a text message).
3. **Buy on the day of the GLB** (or watch for a re-test). You may buy a small piece and see if the stock continues.
4. **Hold** unless the stock *closes* back below the green line. Many times a stock trades below the green line intraday but closes back above — **do not exit on intraday dips**.
5. If it closes below the green line: **failed GLB, exit immediately.**
6. If it retakes the green line and closes back above it: **buy it back.**

**Turtle Traders discipline:** "They had to act on every buy signal. The one signal you do not take after several fails is often the one that works." After multiple failed GLBs on the same stock, the next alert is the one most worth acting on.

---

## Notes / caveats

- The GLB on the **daily RWB chart** (scan for stocks that dipped below all red lines and recovered) is a distinct entry point from the monthly-chart GLB. Both require the stock to be above its last all-time high. They can be used together.
- A stock appearing in the scan that is **not above its last green line top** should be filtered out; it has overhead supply from people who bought at higher prices. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- The IBD 50 outperforms the Nasdaq 100 and S&P 500 during bull markets (+20% vs +15% vs +10% median in 2011–2012). Starting from the IBD 50 list gives a higher-quality candidate pool. ([WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))
- Stay away from stocks reporting earnings imminently — earnings can break a setup. ([WW 2010-04-19](../../raw/posts/2010-04-19-how-i-buy-aapl-for-12-down-without-using-margin.md))

## See also

- [Exits](exits.md)
- [Buying an OSB](buying-osb.md) — the alternative entry if you missed the breakout day, or want the tighter, pre-definable stop
- [Green Line Breakouts (GLB)](../methodology/green-line-breakouts.md)
- [Stock selection](../methodology/stock-selection.md)
- [Market state → stance](market-state.md)
- [Moving-average rules](../methodology/moving-average-rules.md)

## Sources

- [WW 2012-07-23 — Stage analysis and green line charts](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md)
- [WW 2017-12-17 — A strategy for deciding when to sell stocks; GDS, NVDA](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md) ([summary](../sources/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- [WW 2017-03-19 — How I use daily RWB charts to size up the market and individual stocks](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md) ([summary](../sources/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))
- [WW 2010-02-22 — How to use IBD 100 and New America stocks to find rocket stocks](../../raw/posts/2010-02-22-how-to-use-ibd-100-and-new-america-stocks-and-tc2007-to-find-potential-rocket-stocks-market-rally-begun.md) ([summary](../sources/2010-02-22-how-to-use-ibd-100-and-new-america-stocks-and-tc2007-to-find-potential-rocket-stocks-market-rally-begun.md))
- [WW 2012-04-30 — How I find the next AAPL growth stock; new GMI buy signal](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md) ([summary](../sources/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))
- [WW 2018-05-20 — Green line breakout (GLB) explained; GMI remains Green](../../raw/posts/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md) ([summary](../sources/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md))
- [WW 2024-05-27 — ANF worked example (weekly green bar)](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md) ([summary](../sources/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
- [WW 2005-04-30 — My Trading Strategy, Part II](../../raw/posts/2005-04-30-my-trading-strategy-part-ii.md)
- [WW 2023-04-24 — WING missed GLB confessions; written GLB rules; TC2000 alert workflow](../../raw/posts/2023-04-24-blog-post-day-26-of-qqq-short-term-up-trend-wing-flies-to-ath-how-i-missed-the-glb-true-confessions-and-see-m.md) ([summary](../sources/2023-04-24-blog-post-day-26-of-qqq-short-term-up-trend-wing-flies-to-ath-how-i-missed-the-glb-true-confessions-and-see-m.md))
- [WW 2005-04-23 — Let's Talk Strategy](../../raw/posts/2005-04-23-lets-talk-strategy.md) ([summary](../sources/2005-04-23-lets-talk-strategy.md))
- [WW 2010-03-15 — Jim Cramer on stop loss orders; how I trade the 3X ETFs](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md) ([summary](../sources/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))
- [WW 2010-04-19 — How I buy AAPL for 12% down without using margin](../../raw/posts/2010-04-19-how-i-buy-aapl-for-12-down-without-using-margin.md) ([summary](../sources/2010-04-19-how-i-buy-aapl-for-12-down-without-using-margin.md))
- [WW 2010-09-27 — Introducing Red White and Blue (RWB) Stocks](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md) ([summary](../sources/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md))
- [WW 2021-01-24 — In the 60s I used to receive a book of monthly charts; GLB origin; no stop-loss order for a GLB](../../raw/posts/2021-01-24-blog-post-in-the-60s-i-used-to-receive-a-book-containing-monthly-charts-of-stocks-i-noticed-that-stocks-that.md) ([summary](../sources/2021-01-24-blog-post-in-the-60s-i-used-to-receive-a-book-containing-monthly-charts-of-stocks-i-noticed-that-stocks-that.md))
- [WW 2022-08-25 — Blog Post: Day 28 of $QQQ short term up-trend; $QQQ very oversold and bounce likely; GLB: $CLH, how I buy a GL](../../raw/posts/2022-08-25-blog-post-day-28-of-qqq-short-term-up-trend-qqq-very-oversold-and-bounce-likely-glb-clh-how-i-buy-a-glb-autom.md) ([summary](../sources/2022-08-25-blog-post-day-28-of-qqq-short-term-up-trend-qqq-very-oversold-and-bounce-likely-glb-clh-how-i-buy-a-glb-autom.md))
