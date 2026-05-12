---
title: Playbook — exits
type: playbook
updated: 2026-05-11
sources:
  - raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md
  - raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md
  - raw/posts/2009-03-08-how-i-use-put-options-as-investment-insurance.md
  - raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md
---

# Playbook — exits

How and when Dr. Wish sells. He uses two timeframes for exit rules: the initial protective stop placed at entry, and trailing rules that evolve as the position profits.

## Inputs

- [Moving-average rules](../methodology/moving-average-rules.md) — 10-week average, 30-week average, daily RWB
- [GMI](../methodology/gmi.md) / [QQQ Short-Term Timing](../methodology/qqq-short-term-timing.md) flips — market-state exits
- [Risk & cash](../methodology/risk-and-cash.md) — defensive posture

---

## Step 1 — Set the initial stop before buying

Dr. Wish decides his exit price *before* placing a buy order. The stop is based on one of: a prior support level, a moving average, or a recent reaction low. "The best way to enter a trade is to assume it will go wrong, so that I can calmly prepare my risk control strategy in advance." ([WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))

**As soon as the buy order fills:** place a GTC (good-til-cancelled) stop-loss order at the predetermined exit price. A day order expires at the close; a GTC order remains active until triggered or manually cancelled. ([WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))

He does **not** use automatic trailing stops. He raises the stop manually after reviewing the stock's technicals. ([WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))

---

## Step 2 — Choose: stop-loss order or protective put?

Two tools accomplish the same goal (defining a floor on loss) with different trade-offs:

**Stop-loss order:**
- Simple, no premium cost.
- Risk: a gap-down open can execute the order far below the stop price.
- Risk: a whipsaw (stock briefly trades below stop, then recovers) forces a real sale.
- Best when: the stock's volatility is contained and a gap is unlikely.

**Protective put option:**
- Costs the put premium (an insurance cost), which raises the break-even price.
- Benefit: cannot be triggered by a gap-down or intraday whipsaw. If the stock recovers above the strike before expiration, you still hold your shares.
- Benefit: "I can sit back and relax, knowing that if GLD is selling below $89, I can call my broker and instruct her to exercise the put." ([WW 2009-03-08](../../raw/posts/2009-03-08-how-i-use-put-options-as-investment-insurance.md))
- Best when: the stock or market is highly volatile and whipsaw risk is high, or the position has a large unrealized profit to protect.

He can buy protective puts inside his IRA (requires option account approval). ([WW 2009-03-08](../../raw/posts/2009-03-08-how-i-use-put-options-as-investment-insurance.md))

---

## Step 3 — Trailing the stop as the position profits

As the stock advances, move the stop up to protect profits.

**Daily RWB chart — the primary trailing signal (post-2017):**

Dr. Wish shifted from the weekly yellowband 10-week rule to daily RWB charts as his primary tool, because the 10-week rule could give back too much profit. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))

The daily chart has 12 exponential moving averages plotted: 6 shorter-term (red) and 6 longer-term (blue). The price is shown as a dotted line. Exit rules:

- **Standard rule:** sell if the stock *closes below all six red lines*. Intraday dips below the red lines do not count — only closes. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- **Large-profit modification:** for positions with a large unrealized gain, wait for **two consecutive closes below all red lines** before selling, to reduce whipsaw risk. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- **Red-line convergence:** when the six red lines converge (compress together), the stock has stalled. Do not anticipate direction — wait for a breakout in either direction. "React, do not anticipate." ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- **White space disappears:** if the white gap between the red and blue averages closes entirely (the two sets converge), sell the position. ([WW 2017-03-19](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))

**Stop level from the daily chart:** the value of the *lowest red line* (the 15-day EMA, shown in large digits on the TC2000 chart after the word "optionable") is a specific dollar-level stop. If the stock looks like it will close below that value, exit. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))

Alternatively, the pattern of purple dots (daily lows) on the chart shows recent support levels — a more conservative stop can be placed below the most recent cluster of daily lows. ([WW 2017-03-19](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))

**Weekly chart trailing signals (earlier approach; still used in the weekly green bar system):**

- Sell if the stock **closes the week below the 10-week moving average**. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
- Sell if the **4-week average declines below the 10-week average**. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
- Also: sell (or tighten stop) if the stock trades below the low of the most recent green bar. This level can be used as a hard stop when entered off a green-bar signal. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))

The weekly approach has one advantage: decisions can be made on Friday evening or over the weekend with the complete weekly bar available — less time pressure than daily monitoring. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))

---

## Step 4 — Market-state exits (full position)

When the overall market turns against you, the individual-stock trailing rules may be too slow.

- **GMI ≤ 3 for two consecutive readings:** get defensive — begin raising stops and reducing exposure. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- **30-week average of QQQ/SPY closes below and then turns down:** typically exit the market. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- **New lows surging while index at ATH (breadth divergence):** a signal to exit. Example: in November 2021, QQQ was at all-time highs (day U-26) while new lows reached 438. Dr. Wish exited and stayed out for over a year through the subsequent Stage 4 decline. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

---

## Notes / caveats

- He can buy back a stock at a higher price after being stopped out if the trend resumes. "If I am stopped out and the stock rises again I love to buy it back at a higher price than I sold it." ([WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))
- He distinguishes the trading IRA (active exits) from the university pension (stays invested long). Exit rules apply to the trading IRA. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- Evolution: prior to 2017, he used the weekly 10-week average close as the primary trailing exit. After 2017 he shifted to daily RWB red-line closes as the primary signal, using the weekly approach for the weekly green bar system. See [Timeline](../history/timeline.md).

## See also

- [Buying a GLB](buying-glb.md)
- [Market state → stance](market-state.md)
- [Risk & cash](../methodology/risk-and-cash.md)
- [Moving-average rules](../methodology/moving-average-rules.md)
- [Green Line Breakouts (GLB)](../methodology/green-line-breakouts.md)

## Sources

- [WW 2017-12-17 — A strategy for deciding when to sell stocks; GDS, NVDA](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md) ([summary](../sources/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- [WW 2010-03-15 — Jim Cramer on stop loss orders; how I trade the 3X ETFs](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md) ([summary](../sources/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))
- [WW 2009-03-08 — How I use put options as investment insurance](../../raw/posts/2009-03-08-how-i-use-put-options-as-investment-insurance.md) ([summary](../sources/2009-03-08-how-i-use-put-options-as-investment-insurance.md))
- [WW 2024-05-27 — ANF worked example (weekly green bar)](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md) ([summary](../sources/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)
- [WW 2017-03-19 — How I use daily RWB charts to size up the market and individual stocks](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md) ([summary](../sources/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))
- [WW 2023-06-19 — How I compute new US highs and lows; 11/2021 exit](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md) ([summary](../sources/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
