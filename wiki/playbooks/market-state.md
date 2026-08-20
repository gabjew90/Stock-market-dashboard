---
title: Playbook — market state → stance
type: playbook
updated: 2026-08-20
sources:
  - raw/posts/2005-04-23-lets-talk-strategy.md
  - raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md
  - raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md
  - raw/posts/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md
  - raw/posts/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md
  - raw/posts/2010-07-12-new-up-trend-or-dead-cat-bounce.md
  - raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md
  - raw/posts/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2011-11-28-6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg.md
  - raw/posts/2012-04-16-thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld.md
  - raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md
  - raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md
  - raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md
  - raw/posts/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md
  - raw/posts/2014-04-27-i-do-not-want-to-be-long-in-this-market.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md
  - raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md
  - raw/posts/2022-01-30-blog-post-day-16-of-qqq-short-term-down-trend-some-end-of-decline-signs-i-am-looking-for-promising-stock-scan.md
  - raw/posts/2022-03-06-blog-post-investors-intelligence-poll-finds-more-bears-than-bulls-34-5-29-9-extreme-bearish-sentiment-in-news.md
  - raw/posts/2022-04-06-blog-post-jesse-livermore-said-finally-there-came-the-awful-day-of-reckoning-for-the-bulls-and-the-optimists.md
  - raw/posts/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md
  - raw/posts/2022-09-15-blog-post-day-13-of-qqq-short-term-down-trend-weekly-chart-of-dia-suggests-re-test-of-last-junes-lows-how-to.md
  - raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md
  - raw/posts/2016-09-11-september-swoon-weak-fridays-often-lead-to-ugly-mondays-indicators-i-watch-for-a-bottom.md
---

# Playbook — market state → stance

Given today's readings of the [GMI](../methodology/gmi.md), the [QQQ short-term count](../methodology/qqq-short-term-timing.md), [T2108](../methodology/t2108.md), the new-high/new-low counts and the weekly 30-week average, what posture do you take — and in *which account*? Procedure only; the definitions, evidence and history behind every rule are on the linked pages.

## Inputs

- [GMI](../methodology/gmi.md) — 0–6; GREEN ≥ 4, RED ≤ 3; signals at [gmi.md#the-signals](../methodology/gmi.md#the-signals--buy-sell-and-the-hold-state-at-3)
- [QQQ short-term timing](../methodology/qqq-short-term-timing.md) — up/down and the day count
- [T2108](../methodology/t2108.md) — % of NYSE stocks above their 40-day MA
- Daily US new highs / new lows ([gmi.md#new-highs](../methodology/gmi.md#new-highs--new-lows--a-breadth-supplement-to-the-gmi))
- [Moving-average rules](../methodology/moving-average-rules.md) — QQQ/SPY vs their 30-week average (Stage)

---

## Step 0 — Decide which account you are steering

- **Trading IRA:** follows every rule below — "when [the GMI] declines to 3 or below, I get defensive in my trading IRA." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- **University pension:** steered by the *weekly* trend and ignores GMI Sell signals since 2015 ([WW 2015-02-22](../../raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md)); it exits by Step 5, not by the GMI. Full treatment: [the two accounts](../methodology/pension-management.md).

---

## Step 1 — Read the GMI

| Reading | Stance (trading account) |
|---|---|
| **> 3 for two consecutive days** | **Buy signal** ([WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md); two-day rule adopted [WW 2011-11-28](../../raw/posts/2011-11-28-6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg.md)). First purchase is TQQQ ([WW 2013-11-24](../../raw/posts/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md)); then run the [GLB](buying-glb.md) and [OSB](buying-osb.md) playbooks. |
| **≥ 4 (GREEN)** | Long. "I like to be long if the GMI is 4 or more." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)) |
| **= 3** | Hold state — raise stops, no new buys. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)) |
| **< 3 for two consecutive days** | **Sell signal** ([WW 2012-04-16](../../raw/posts/2012-04-16-thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld.md), [WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)). Long side out; cash over shorting ([risk-and-cash](../methodology/risk-and-cash.md#cash-over-short--the-age-based-default)). |

Signals flip fast: "when the instruments tell me the market is reversing direction, I must act on it and not fight it." ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md)) The GMI confirms a turn, it does not predict one — see [gmi.md#how-he-uses-it](../methodology/gmi.md#how-he-uses-it).

---

## Step 2 — Read the QQQ short-term count

- **Day 1 of a new up-trend:** buy the leveraged ETF, then "wade in slowly and only buy more as the index climbs and confirms the trend." ([WW 2011-01-04](../../raw/posts/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md)) Sizing and the SQQQ mirror: [leveraged-etf-default](../methodology/leveraged-etf-default.md).
- **New down-trend, ≤ 5 days, GMI still GREEN:** not yet a verdict — ~40% end in under 5 days. A *small* SQQQ hedge is optional; add only at Day 5–6. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md), [WW 2010-05-09](../../raw/posts/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md))
- **GMI Buy but the QQQ down-trend persists for many days:** a warning, not a licence to trade through it. ([WW 2014-04-27](../../raw/posts/2014-04-27-i-do-not-want-to-be-long-in-this-market.md))
- **Short *and* long trends both down:** no longs "until *both* trends have signaled a new up-trend… such is the fate of the trend follower." ([WW 2010-07-12](../../raw/posts/2010-07-12-new-up-trend-or-dead-cat-bounce.md))

Duration base rates: [qqq-short-term-timing.md](../methodology/qqq-short-term-timing.md#trend-duration-statistics--what-he-has-actually-published).

---

## Step 3 — Read T2108 (two bands, not one)

- **> 80%:** "market tops likely" — do not add; move stops up. ([WW 2013-01-07](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md), [WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md)) A high reading is "not as predictive as an extremely low reading below 10%." ([WW 2010-09-27](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md))
- **< 25–30%:** "bottoms likely" — the routine band. Not by itself a buy. ([WW 2013-01-07](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md))
- **< 10%:** the level he acts on — buy **SPY**, start small, accumulate **only on the way up** once a bottom forms. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md), [WW 2022-05-01](../../raw/posts/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md)) An index trade in a RED market — it does not re-open the stock playbooks.
- **Bottom-watch pair:** put/call **> 1.10** *and* T2108 **< 10%**. ([WW 2022-01-30](../../raw/posts/2022-01-30-blog-post-day-16-of-qqq-short-term-down-trend-some-end-of-decline-signs-i-am-looking-for-promising-stock-scan.md))
- **Sentiment does not overrule breadth:** bears > bulls with T2108 at 37% and put/call in the .80s ⇒ stay in cash. ([WW 2022-03-06](../../raw/posts/2022-03-06-blog-post-investors-intelligence-poll-finds-more-bears-than-bulls-34-5-29-9-extreme-bearish-sentiment-in-news.md))

Thresholds, history and the reading he admits he may not execute: [t2108.md](../methodology/t2108.md#thresholds).

---

## Step 4 — Check breadth divergence (overrides a GREEN GMI)

New lows surging while the index is at a high is an exit signal *before* the GMI turns — November 2021: QQQ at all-time highs (U-26) with 438 new lows; he exited near the peak. Counts run over the full US universe filtered for close > $10 and volume > 10,000. Raise stops or go to cash regardless of GMI colour. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

---

## Step 5 — Weekly stage check, and the pension

- **QQQ/SPY closes below its 30-week:** "very defensive" — no new buys, raise stops. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- **The 30-week itself turns down (Stage 4):** typically exit the market. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- **Pension, staged:** 25% out on the first close under the 30-week, another 25% on each further deterioration, toward 100% as it declines. ([WW 2010-07-06](../../raw/posts/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md)) **The rule is not the whole practice** — in November 2021 he moved pension money out on breadth divergence alone, five months before the trigger fired. ([WW 2022-04-06](../../raw/posts/2022-04-06-blog-post-jesse-livermore-said-finally-there-came-the-awful-day-of-reckoning-for-the-bulls-and-the-optimists.md)) Protocol and revision: [the two accounts](../methodology/pension-management.md#the-staged-pension-exit-protocol).
- **Confirming a bottom:** the weekly **10-week crossing back above the 30-week**; the same cross downward ends the trade. ([WW 2022-09-15](../../raw/posts/2022-09-15-blog-post-day-13-of-qqq-short-term-down-trend-weekly-chart-of-dia-suggests-re-test-of-last-junes-lows-how-to.md))
- **Window-dressing rallies** into quarter- and year-end are exit and stop-raising opportunities in a weakening tape, not entries. ([WW 2016-12-04](../../raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md))

- **Seasonals he has noted** (context, not triggers): September is historically the weakest month; **bottoms often come in October**, when third-quarter earnings revive stocks; the post-earnings lull "typically sets up the next earnings propelled rise"; and "**large declines on Fridays often lead to ugly Mondays**, when the public gets a chance to sell after pondering their portfolio losses over the weekend." ([WW 2016-09-11](../../raw/posts/2016-09-11-september-swoon-weak-fridays-often-lead-to-ugly-mondays-indicators-i-watch-for-a-bottom.md))

---

## Stance summary table (trading account)

| GMI | QQQ short-term | 30-wk MA | T2108 / breadth | Stance |
|---|---|---|---|---|
| Buy signal (>3 ×2 days) | Day 1 up | above, rising | < 80% | Buy TQQQ Day 1, wade in; open the GLB/OSB playbooks |
| ≥ 4 | up | above, rising | < 80% | Full bull — hold, buy GLBs/OSBs, add to winners |
| ≥ 4 | up | above, rising | > 80% | Cautious bull — hold, move stops up, no adds |
| ≥ 4 | down ≤ 5 days | above, rising | any | Hold; small SQQQ hedge optional; add only at Day 5–6 |
| ≥ 4 | down, many days | any | any | Warning — tighten; no new longs |
| ≥ 4 | any | any | new lows surging at index highs | Exit or near-exit, GMI notwithstanding |
| = 3 | any | any | any | Hold state — no new buys, raise stops |
| Sell signal (<3 ×2 days) | any | any | any | Long side out; cash by default |
| any | any | below 30-wk | any | Very defensive; pension starts staged exit |
| any | any | 30-wk turning down | any | Exit market; pension toward 100% cash |
| any | any | 10-wk crossing above 30-wk | any | Bottom confirmed — re-enter |
| any | any | any | T2108 < 10% + p/c > 1.10 | Contrarian SPY accumulation on the way up — index only |

---

## Notes / caveats

- The market gate comes first because more than 70% of stocks move with the major indexes. ([WW 2005-04-23](../../raw/posts/2005-04-23-lets-talk-strategy.md))
- Everything above is the *trading* stance. The pension follows the weekly trend (Step 0 and Step 5). The [backtest](../methodology/backtest-timing-overlay.md) measures the trading rule as if it were the pension rule — read its verdict with that in mind.

## See also

- [Risk & cash](../methodology/risk-and-cash.md) · [GMI](../methodology/gmi.md) · [T2108](../methodology/t2108.md) · [QQQ short-term timing](../methodology/qqq-short-term-timing.md) · [The two accounts](../methodology/pension-management.md)
- [Buying a GLB](buying-glb.md) · [Buying an OSB](buying-osb.md) · [Exits](exits.md)

## Sources

- [WW 2005-04-23 — Let's Talk Strategy](../../raw/posts/2005-04-23-lets-talk-strategy.md) ([summary](../sources/2005-04-23-lets-talk-strategy.md))
- [WW 2005-07-17 — GMI since inception; introducing the WPM](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md) ([summary](../sources/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))
- [WW 2010-03-15 — Jim Cramer on stop loss orders; how I trade the 3X ETFs](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md) ([summary](../sources/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))
- [WW 2010-05-09 — Worden seminar; market in short-term down-trend; mainly in cash](../../raw/posts/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md) ([summary](../sources/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md))
- [WW 2010-07-06 — At the beginning of a big market decline; staged pension exit](../../raw/posts/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md) ([summary](../sources/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md))
- [WW 2010-07-12 — New up-trend or dead cat bounce?](../../raw/posts/2010-07-12-new-up-trend-or-dead-cat-bounce.md) ([summary](../sources/2010-07-12-new-up-trend-or-dead-cat-bounce.md))
- [WW 2010-09-27 — Introducing Red White and Blue (RWB) Stocks](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md)
- [WW 2011-01-04 — 2010 ETF year-in-review; TQQQ default; Day-1 entry tactic](../../raw/posts/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md) ([summary](../sources/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md))
- [WW 2011-03-07 — Introducing the GMI2](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)
- [WW 2011-11-28 — GMI performance since April; the two-day rule adopted](../../raw/posts/2011-11-28-6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg.md) ([summary](../sources/2011-11-28-6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg.md))
- [WW 2012-04-16 — Worden DC seminar; how he uses the GMI signals](../../raw/posts/2012-04-16-thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld.md) ([summary](../sources/2012-04-16-thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld.md))
- [WW 2012-04-30 — GMI buy signal = >3 two consecutive days](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md) ([summary](../sources/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))
- [WW 2012-07-23 — Stage analysis and green line charts](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md)
- [WW 2013-01-07 — Day 3 of QQQ up-trend; T2108 = 82 (the daily-table band)](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md)
- [WW 2013-11-24 — GMI-based strategy using 3X ETFs beats IBD 50 stocks](../../raw/posts/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md) ([summary](../sources/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md))
- [WW 2014-04-27 — I do not want to be long in this market](../../raw/posts/2014-04-27-i-do-not-want-to-be-long-in-this-market.md) ([summary](../sources/2014-04-27-i-do-not-want-to-be-long-in-this-market.md))
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)
- [WW 2015-02-22 — An important limitation of the GMI signals](../../raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md) ([summary](../sources/2015-02-22-an-important-limitation-of-the-gmi-signals.md))
- [WW 2016-12-04 — New QQQ down-trend; ~40% end in under 5 days](../../raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md) ([summary](../sources/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md))
- [WW 2022-01-30 — End-of-decline signs; the 30-week must curve up](../../raw/posts/2022-01-30-blog-post-day-16-of-qqq-short-term-down-trend-some-end-of-decline-signs-i-am-looking-for-promising-stock-scan.md) ([summary](../sources/2022-01-30-blog-post-day-16-of-qqq-short-term-down-trend-some-end-of-decline-signs-i-am-looking-for-promising-stock-scan.md))
- [WW 2022-03-06 — Bears outnumber bulls, but T2108 says no bottom](../../raw/posts/2022-03-06-blog-post-investors-intelligence-poll-finds-more-bears-than-bulls-34-5-29-9-extreme-bearish-sentiment-in-news.md) ([summary](../sources/2022-03-06-blog-post-investors-intelligence-poll-finds-more-bears-than-bulls-34-5-29-9-extreme-bearish-sentiment-in-news.md))
- [WW 2022-04-06 — Livermore's day of reckoning; the pension rule revised](../../raw/posts/2022-04-06-blog-post-jesse-livermore-said-finally-there-came-the-awful-day-of-reckoning-for-the-bulls-and-the-optimists.md) ([summary](../sources/2022-04-06-blog-post-jesse-livermore-said-finally-there-came-the-awful-day-of-reckoning-for-the-bulls-and-the-optimists.md))
- [WW 2022-05-01 — Nowhere oversold enough to be near a bottom; T2108 monthly](../../raw/posts/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md) ([summary](../sources/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md))
- [WW 2022-09-15 — How to discern a bottom: the 10-week crossing above the 30-week](../../raw/posts/2022-09-15-blog-post-day-13-of-qqq-short-term-down-trend-weekly-chart-of-dia-suggests-re-test-of-last-junes-lows-how-to.md) ([summary](../sources/2022-09-15-blog-post-day-13-of-qqq-short-term-down-trend-weekly-chart-of-dia-suggests-re-test-of-last-junes-lows-how-to.md))
- [WW 2023-06-19 — How I compute new US highs and lows; 11/2021 exit](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md) ([summary](../sources/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- [WW 2016-09-11 — September swoon? Weak Fridays often lead to Ugly Mondays—Indicators I watch for a bottom](../../raw/posts/2016-09-11-september-swoon-weak-fridays-often-lead-to-ugly-mondays-indicators-i-watch-for-a-bottom.md) ([summary](../sources/2016-09-11-september-swoon-weak-fridays-often-lead-to-ugly-mondays-indicators-i-watch-for-a-bottom.md))
