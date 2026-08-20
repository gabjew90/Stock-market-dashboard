---
title: Playbook — exits
type: playbook
updated: 2026-08-18
sources:
  - raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md
  - raw/posts/2005-05-26-cramer-and-limit-orders-orct-and-pnra-gmi-back-to-5.md
  - raw/posts/2019-03-15-how-i-avoid-getting-shaken-out-of-strong-growth-stocks.md
  - raw/posts/2020-09-20-10-doublers-that-last-week-reached-an-ath-on-above-average-volume-and-how-i-found-them-apps-trup-dkng-fvrr-nv.md
  - raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md
  - raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md
  - raw/posts/2009-03-08-how-i-use-put-options-as-investment-insurance.md
  - raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md
  - raw/posts/2016-11-20-short-and-long-term-trends-now-up-on-using-weekly-charts-to-stay-in-a-growth-stock-ntes.md
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md
  - raw/posts/2019-11-24-why-i-sold-inmd-at-57-following-the-tweets-of-some-smart-traders-markminervini-and-tmltrader.md
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

**As soon as the buy order fills:** place a GTC (good-til-cancelled) stop-loss order at the predetermined exit price. A day order expires at the close; a GTC order remains active until triggered or manually cancelled. ([WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md)) **Exception:** for a GLB he does not enter the stop as a resting order — the same level is checked on the *close*, to avoid intraday probes of the green line; see [buying-glb Step 5](buying-glb.md#step-5--set-the-initial-stop-immediately--but-for-a-glb-on-a-close-basis).

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

## Step 3 — Trail the stop as the position profits

Three published trailing systems, not interchangeable — [which one applies](#which-trailing-system-when) depends on horizon and how much profit is at risk.

| System | Trigger to exit | Detail |
|---|---|---|
| **Weekly 4/10/30 ladder** (2016, the default) | Weekly *close* under the **10-week** exits; a close under the 4-week warns | [moving-average-rules](../methodology/moving-average-rules.md#the-4-week--10-week--30-week-alignment--a-weekly-stock-rule) |
| **Daily RWB** (2017, for extended winners) | A *close* below all six red lines — two closes if the gain is large | [gmma-charts](../methodology/gmma-charts.md#the-daily-rwb-chart--a-finer-grained-tool) |
| **Weekly green bars** (2024) | 4wk crossing below 10wk, or a close under the last green bar's low | ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md)) |

Stop *levels* on the daily chart: the lowest red line (15-day EMA), or below the recent cluster of daily lows for a more conservative stop. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md), [WW 2017-03-19](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))

---

## Step 4 — Market-state exits (full position)

When the overall market turns against you, the individual-stock trailing rules may be too slow.

- **GMI ≤ 3:** he "like[s] to be long if the GMI is 4 or more" — below that, get defensive: raise stops, reduce exposure. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)) Full signal table on the [GMI page](../methodology/gmi.md#the-signals--buy-sell-and-the-hold-state-at-3).
- **GMI below 3 for two consecutive days = Sell signal:** exit the long side of the trading accounts. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))
- **30-week average of QQQ/SPY closes below and then turns down:** typically exit the market. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- **New lows surging while index at ATH (breadth divergence):** a signal to exit. Example: in November 2021, QQQ was at all-time highs (day U-26) while new lows reached 438. Dr. Wish exited and stayed out for over a year through the subsequent Stage 4 decline. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

---

## Step 5 — Before every sale, check the weekly

The standing veto on daily-chart sell signals: **look at the stock's weekly chart before every sale of a long position; if it is still holding its rising 10-week average, do not sell.** He buys on daily set-ups and sells only off the weekly. ([WW 2019-03-15](../../raw/posts/2019-03-15-how-i-avoid-getting-shaken-out-of-strong-growth-stocks.md)) The worked case (COUP, two daily sell signals overruled) and the note he keeps on his monitor are on [moving-average-rules](../methodology/moving-average-rules.md#the-10-week-average--the-holding-rule-for-individual-stocks).

---

## Step 6 — Use market orders

Sell (and buy) **at the market**, not with limit orders — "it could be suicide to put a limit order in on a sell and not be able to sell because the stock never traded at my limit price." If you want back in after being stopped out, leave a **standing buy-stop** above the prior peak rather than deciding again later. ([WW 2005-05-26](../../raw/posts/2005-05-26-cramer-and-limit-orders-orct-and-pnra-gmi-back-to-5.md)) Reasoning: [risk-and-cash](../methodology/risk-and-cash.md#stop-loss-discipline--the-mechanics).

---

## Which trailing system when

The three systems above plus the weekly-first rule look contradictory read in isolation. Laid out by date and by the risk each one manages, they are one policy:

| Year | System | Manages | When it governs |
|---|---|---|---|
| 2016 | Weekly 4wk > 10wk > 30wk ladder — warn on a close under the 4wk, exit on a close under the 10wk ([WW 2016-11-20](../../raw/posts/2016-11-20-short-and-long-term-trends-now-up-on-using-weekly-charts-to-stay-in-a-growth-stock-ntes.md)) | Shakeout — being bounced out of a good stock by daily noise | The **default** for a strong growth stock in an ordinary advance |
| 2017 | Daily RWB — sell on a close under all six red lines (two closes if the gain is large); at the time stated as governing "both my buy and sell decisions" ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md)) | Profit give-back — waiting for a weekly close under the 10wk "could lose me a lot of the profit" | Dec 2017 – early 2019: his stated default. After 2019: an **extended winner** that has run far above its weekly averages |
| 2019–20 | "Look at the weekly chart before every sale... if the stock is still holding its rising 10 week average, do not sell" ([WW 2019-03-15](../../raw/posts/2019-03-15-how-i-avoid-getting-shaken-out-of-strong-growth-stocks.md), [WW 2020-09-20](../../raw/posts/2020-09-20-10-doublers-that-last-week-reached-an-ath-on-above-average-volume-and-how-i-found-them-apps-trup-dkng-fvrr-nv.md)) | Shakeout, again — an explicit veto on daily-chart sell signals | **Every** discretionary sale of a long; it reverses the 2017 sell-side shift and re-asserts 2016 as the default |
| 2024 | Weekly green-bar overlay — sell if 4wk < 10wk or on a close under the last green bar's low ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md)) | Same as 2016, restated visually | Interchangeable with the 2016 ladder |

So the operating rule *as of his most recent statements* is: **weekly first, always; the daily RWB exit is the exception he grants himself for a big winner where the 10-week close would cost too much.** The sequence is a genuine evolution, not a contradiction: weekly (2016) → daily for both buy and sell (Dec 2017) → sell only off the weekly, buy off the daily (2019, enforced with a note on his monitor in 2020) → weekly green bars (2024). Where a page elsewhere in this wiki calls the daily RWB exit his "primary" trailing signal, that is correct for 2017–18 and stale after March 2019.

## Notes / caveats

- He can buy back a stock at a higher price after being stopped out if the trend resumes. "If I am stopped out and the stock rises again I love to buy it back at a higher price than I sold it." ([WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))
- He distinguishes the trading IRA (active exits) from the university pension (stays invested long). Exit rules apply to the trading IRA. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- Evolution: the 2017 shift to daily RWB exits was real but was reversed on the sell side in 2019 — see [which trailing system when](#which-trailing-system-when). Dates on the [Timeline](../history/timeline.md).

- One discretionary exit sits above the mechanical ones: when a position goes vertical — outside its upper 15.2 daily Bollinger Band on very heavy volume — and "making money [feels] too easy," he sells (INMD, +40% in nine days, sold ~$57; it closed the week at $41.55). Stated as a rule on [trading psychology](../methodology/trading-psychology.md#7-when-it-feels-too-easy-sell). ([WW 2019-11-24](../../raw/posts/2019-11-24-why-i-sold-inmd-at-57-following-the-tweets-of-some-smart-traders-markminervini-and-tmltrader.md))

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
- [WW 2016-11-20 — Weekly 4wk/10wk hold discipline; NTES and NVDA](../../raw/posts/2016-11-20-short-and-long-term-trends-now-up-on-using-weekly-charts-to-stay-in-a-growth-stock-ntes.md) ([summary](../sources/2016-11-20-short-and-long-term-trends-now-up-on-using-weekly-charts-to-stay-in-a-growth-stock-ntes.md))
- [WW 2011-03-07 — Introducing the GMI2](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md) ([summary](../sources/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- [WW 2012-07-23 — Stage analysis and green line charts](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md) ([summary](../sources/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- [WW 2019-03-15 — Buy on the daily, sell only off the weekly (COUP)](../../raw/posts/2019-03-15-how-i-avoid-getting-shaken-out-of-strong-growth-stocks.md) ([summary](../sources/2019-03-15-how-i-avoid-getting-shaken-out-of-strong-growth-stocks.md))
- [WW 2020-09-20 — The weekly doubler-ATH scan, full syntax; the note on the monitor](../../raw/posts/2020-09-20-10-doublers-that-last-week-reached-an-ath-on-above-average-volume-and-how-i-found-them-apps-trup-dkng-fvrr-nv.md) ([summary](../sources/2020-09-20-10-doublers-that-last-week-reached-an-ath-on-above-average-volume-and-how-i-found-them-apps-trup-dkng-fvrr-nv.md))
- [WW 2005-05-26 — BUY AND SELL AT THE MARKET; the standing re-entry buy-stop; Lynch's method](../../raw/posts/2005-05-26-cramer-and-limit-orders-orct-and-pnra-gmi-back-to-5.md) ([summary](../sources/2005-05-26-cramer-and-limit-orders-orct-and-pnra-gmi-back-to-5.md))
- [WW 2019-11-24 — Why I sold INMD at $57; the too-easy voice](../../raw/posts/2019-11-24-why-i-sold-inmd-at-57-following-the-tweets-of-some-smart-traders-markminervini-and-tmltrader.md) ([summary](../sources/2019-11-24-why-i-sold-inmd-at-57-following-the-tweets-of-some-smart-traders-markminervini-and-tmltrader.md))
