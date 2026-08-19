---
title: Playbook — market state → stance
type: playbook
updated: 2026-08-18
sources:
  - raw/posts/2005-04-23-lets-talk-strategy.md
  - raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md
  - raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md
  - raw/posts/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md
  - raw/posts/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md
  - raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md
  - raw/posts/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md
  - raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md
  - raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md
  - raw/posts/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md
  - raw/posts/2014-04-27-i-do-not-want-to-be-long-in-this-market.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md
  - raw/posts/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md
  - raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md
  - raw/posts/2011-11-28-6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg.md
  - raw/posts/2012-04-16-thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld.md
  - raw/posts/2010-07-12-new-up-trend-or-dead-cat-bounce.md
  - raw/posts/2022-01-30-blog-post-day-16-of-qqq-short-term-down-trend-some-end-of-decline-signs-i-am-looking-for-promising-stock-scan.md
  - raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md
---

# Playbook — market state → stance

Given today's readings of the [GMI](../methodology/gmi.md), the [QQQ short-term count](../methodology/qqq-short-term-timing.md), [T2108](../methodology/t2108.md), the new-high/new-low counts and the weekly 30-week average, what posture do you take — and in *which account*? This is a decision procedure, not a formula; the definitions, history and evidence for every rule below live on the linked methodology pages, and each step here restates a rule in one line with its citation.

## Inputs

- [GMI](../methodology/gmi.md) — 0–6; GREEN ≥ 4, RED ≤ 3; Buy/Sell signals defined at [gmi.md#the-signals](../methodology/gmi.md#the-signals--buy-sell-and-the-hold-state-at-3)
- [QQQ short-term timing](../methodology/qqq-short-term-timing.md) — up/down and the day count
- [T2108](../methodology/t2108.md) — % of NYSE stocks above their 40-day MA
- Daily US new highs / new lows ([gmi.md#new-highs](../methodology/gmi.md#new-highs--new-lows--a-breadth-supplement-to-the-gmi))
- [Moving-average rules](../methodology/moving-average-rules.md) — QQQ/SPY vs their 30-week average (Stage)

---

## Step 0 — Decide which account you are steering

He runs two speeds, and the rest of this page is for the fast one.

- **Trading IRA:** follows every rule below — "when [the GMI] declines to 3 or below, I get defensive in my trading IRA." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- **University pension:** stays invested while the *weekly* trend holds, and ignores GMI Sell signals — after seven Sell/Buy whipsaws in a year he concluded "a GMI Sell signal should only be used by me for short term trading decisions" and that he should "remain invested long term... as long as the RWB pattern is in place." ([WW 2015-02-22](../../raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md)) The pension exits by the [staged 30-week protocol](#step-5--weekly-stage-check-and-the-pension), not by the GMI. Full treatment: [the two accounts](../methodology/pension-management.md#university-pension-vs-trading-ira).

---

## Step 1 — Read the GMI

| Reading | Stance (trading account) |
|---|---|
| **> 3 for two consecutive days** | **Buy signal.** (Two-day rule adopted 2011-11-28 — ([WW 2011-11-28](../../raw/posts/2011-11-28-6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg.md)); stated as the criterion in [WW 2012-04-30](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md)) Default first purchase is the leveraged index ETF — TQQQ — accumulated as the trend confirms; his studies had TQQQ beating 90%+ of individual stocks during QQQ up-trends. ([WW 2013-11-24](../../raw/posts/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md)) Then run the [GLB](buying-glb.md) and [OSB](buying-osb.md) playbooks for stocks. |
| **≥ 4 (GREEN), signal already on** | Long. "I like to be long if the GMI is 4 or more." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)) |
| **= 3** | Hold state — defensive but not yet Sell. Raise stops; no new buys. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)) |
| **< 3 for two consecutive days** | **Sell signal.** (Stated April 2012 — ([WW 2012-04-16](../../raw/posts/2012-04-16-thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld.md)).) "The GMI is now at 1 (of 6) and if it registers below 3 on Monday, it will flash a Sell signal." ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)) Exit the long side of the trading account; cash is the default over shorting (see [risk-and-cash](../methodology/risk-and-cash.md#cash-over-short--the-age-based-default)). |

Signals flip fast — 3 → 6 in a day is documented — and "when the instruments tell me the market is reversing direction, I must act on it and not fight it." ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))

---

## Step 2 — Read the QQQ short-term count

- **Day 1 of a new up-trend** is his preferred entry for the leveraged ETF: "I especially like to buy the bullish leveraged ETF on the *first* day of a new QQQQ short term up-trend"; then "wade in slowly and only buy more as the index climbs and confirms the trend." ([WW 2011-01-04](../../raw/posts/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md))
- **Early days of a new down-trend (≤ 5) with the GMI still GREEN:** not yet a verdict — about one quarter of new down-trends have ended in fewer than 6 days (2014; ~40% by the 2019 tabulation). Optionally a *small* SQQQ hedge; add only if the down-trend reaches Day 5–6. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)) "I will be more certain of this new down-trend if it lasts for 5 days." ([WW 2010-05-09](../../raw/posts/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md))
- **GMI Buy signal but the QQQ down-trend persists for many days:** treat as a warning, not a contradiction to trade through — with the GMI on a Buy and the QQQ "in its 24th day" of a down-trend he was making "a small bet on a continuation of this down-trend." ([WW 2014-04-27](../../raw/posts/2014-04-27-i-do-not-want-to-be-long-in-this-market.md))

---

- **Both trends down:** "when we are in short *and* long term down-trends… I do not go long until *both* trends have signaled a new up-trend. This means that if this rally is the start of a new up-trend, I will miss some of the gains, but such is the fate of the trend follower." ([WW 2010-07-12](../../raw/posts/2010-07-12-new-up-trend-or-dead-cat-bounce.md))

## Step 3 — Read T2108 (two bands, not one)

- **> 80%:** "market tops likely" (the routine band printed on the daily GMI table) — do not add; move stops up. ([WW 2013-01-07](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md), [WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md)) A high reading is "not as predictive as an extremely low reading below 10%." ([WW 2010-09-27](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md))
- **< 25–30%:** "bottoms likely" — the same routine band; a decline is *probably* near its low. Not by itself a buy. ([WW 2013-01-07](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md))
- **< 10%:** the level he *acts* on — "grit my teeth while the market gossip is terrible and buy a market index ETF." ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)) Method (2022): SPY, not stocks; start small; accumulate **only on the way up** once a bottom appears to form. ([WW 2022-05-01](../../raw/posts/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md)) This is an index trade in a RED market — it does not re-open the stock playbooks.

Thresholds and their history: [t2108.md#thresholds](../methodology/t2108.md#thresholds).

---

- **The bottom-watch pair (2022):** put/call **> 1.10** *and* T2108 **< 10%** as "early indicators of a possible bottom"; on a T2108 break below 10% he will "buy a little SPY and buy more only at *higher* levels after a bottom is in." The re-entry itself waits on the weekly: a close above the 30-week can whipsaw, so "I want to see the 30 week average curving up again. That is the definitive signal to get me back in." ([WW 2022-01-30](../../raw/posts/2022-01-30-blog-post-day-16-of-qqq-short-term-down-trend-some-end-of-decline-signs-i-am-looking-for-promising-stock-scan.md))

## Step 4 — Check breadth divergence (overrides a GREEN GMI)

New lows surging while the index is at a high is an exit signal *before* the GMI turns: in November 2021 QQQ was at all-time highs (day U-26) while new lows reached 438; he exited near the peak and stayed out for over a year of Stage 4. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md)) Counts are over the full US universe filtered for close > $10 and volume > 10,000. Raise stops or go to cash on the divergence, GMI colour notwithstanding.

---

## Step 5 — Weekly stage check, and the pension

- **QQQ/SPY closes below its 30-week average:** "very defensive" — no new buys, raise stops on everything. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- **The 30-week average itself turns down (Stage 4):** typically exit the market. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- **Pension, staged:** first close under the 30-week → move ~25% to money market; another 25% on each further deterioration; toward 100% when the 30-week is declining. At GMI = 0 he has moved 60% at once, timing penalties accepted — "if the market were to turn up in the next few months I would have no regrets as I would simply hop back on at a higher level." ([WW 2010-07-06](../../raw/posts/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md)) Protocol in full: [the two accounts](../methodology/pension-management.md#the-staged-pension-exit-protocol).

---

- **Window-dressing rallies** into quarter- and year-end are exit and stop-raising opportunities in a weakening tape, not entries: such a rally "may be a great time to exit positions or raise stops." ([WW 2016-12-04](../../raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md))

## Stance summary table (trading account)

| GMI | QQQ short-term | 30-wk MA | T2108 / breadth | Stance |
|---|---|---|---|---|
| Buy signal (>3 ×2 days) | Day 1 up | above, rising | < 80% | Buy TQQQ Day 1, wade in; open the GLB/OSB playbooks |
| ≥ 4 | up | above, rising | < 80% | Full bull — hold, buy GLBs/OSBs, add to winners |
| ≥ 4 | up | above, rising | > 80% | Cautious bull — hold, move stops up, no adds |
| ≥ 4 | down ≤ 5 days | above, rising | any | Hold; small SQQQ hedge optional; add to it only at Day 5–6 |
| ≥ 4 | down, many days | any | any | Warning — small bet on continuation; tighten |
| ≥ 4 | any | any | new lows surging at index highs | Exit or near-exit, GMI notwithstanding |
| = 3 | any | any | any | Hold state — no new buys, raise stops |
| Sell signal (<3 ×2 days) | any | any | any | Long side out; cash by default |
| any | any | below 30-wk | any | Very defensive; pension starts staged exit |
| any | any | 30-wk turning down | any | Exit market; pension toward 100% cash |
| any | any | any | T2108 < 10% | Contrarian SPY accumulation on the way up — index only |

---

## Notes / caveats

- The 70% rule is why the market gate comes first: more than 70% of stocks move with the major indexes, so buying growth stocks in a down-trend puts the odds against you. ([WW 2005-04-23](../../raw/posts/2005-04-23-lets-talk-strategy.md))
- Everything above is the *trading* stance. The pension's rule is the weekly RWB/30-week trend, and it deliberately ignores GMI Sell signals since 2015 (Step 0). The [backtest of the GMI overlay](../methodology/backtest-timing-overlay.md) measures the trading rule as if it were the pension rule — read its verdict with that in mind.

## See also

- [Risk & cash](../methodology/risk-and-cash.md) · [GMI](../methodology/gmi.md) · [T2108](../methodology/t2108.md) · [QQQ short-term timing](../methodology/qqq-short-term-timing.md)
- [Buying a GLB](buying-glb.md) · [Buying an OSB](buying-osb.md) · [Exits](exits.md)

## Sources

- [WW 2005-04-23 — Let's Talk Strategy](../../raw/posts/2005-04-23-lets-talk-strategy.md) ([summary](../sources/2005-04-23-lets-talk-strategy.md))
- [WW 2005-07-17 — GMI since inception; introducing the WPM](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md) ([summary](../sources/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))
- [WW 2010-03-15 — Jim Cramer on stop loss orders; how I trade the 3X ETFs](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md) ([summary](../sources/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))
- [WW 2010-05-09 — Worden seminar; market in short-term down-trend; mainly in cash](../../raw/posts/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md) ([summary](../sources/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md))
- [WW 2010-07-06 — At the beginning of a big market decline; staged pension exit](../../raw/posts/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md) ([summary](../sources/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md))
- [WW 2010-09-27 — Introducing Red White and Blue (RWB) Stocks](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md)
- [WW 2011-01-04 — 2010 ETF year-in-review; TQQQ default; Day-1 entry tactic](../../raw/posts/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md) ([summary](../sources/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md))
- [WW 2011-03-07 — Introducing the GMI2](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)
- [WW 2012-04-30 — GMI buy signal = >3 two consecutive days](../../raw/posts/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md) ([summary](../sources/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md))
- [WW 2012-07-23 — Stage analysis and green line charts](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md)
- [WW 2013-01-07 — Day 3 of QQQ up-trend; T2108 = 82 (the daily-table band)](../../raw/posts/2013-01-07-3rd-day-of-qqq-short-term-up-trend-t2108-82.md)
- [WW 2013-11-24 — GMI-based strategy using 3X ETFs beats IBD 50 stocks](../../raw/posts/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md) ([summary](../sources/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md))
- [WW 2014-04-27 — I do not want to be long in this market](../../raw/posts/2014-04-27-i-do-not-want-to-be-long-in-this-market.md) ([summary](../sources/2014-04-27-i-do-not-want-to-be-long-in-this-market.md))
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)
- [WW 2015-02-22 — An important limitation of the GMI signals](../../raw/posts/2015-02-22-an-important-limitation-of-the-gmi-signals.md) ([summary](../sources/2015-02-22-an-important-limitation-of-the-gmi-signals.md))
- [WW 2022-05-01 — Nowhere oversold enough to be near a bottom; T2108 monthly](../../raw/posts/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md) ([summary](../sources/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md))
- [WW 2023-06-19 — How I compute new US highs and lows; 11/2021 exit](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md) ([summary](../sources/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- [WW 2011-11-28 — 6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg](../../raw/posts/2011-11-28-6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg.md) ([summary](../sources/2011-11-28-6th-day-of-qqq-short-term-down-trend-gmi-performance-since-april-stage-4-cmg.md))
- [WW 2012-04-16 — thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld](../../raw/posts/2012-04-16-thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld.md) ([summary](../sources/2012-04-16-thoughts-about-the-worden-dc-seminar-gmi-2-in-cash-and-short-gld.md))
- [WW 2010-07-12 — New up-trend or dead cat bounce?](../../raw/posts/2010-07-12-new-up-trend-or-dead-cat-bounce.md) ([summary](../sources/2010-07-12-new-up-trend-or-dead-cat-bounce.md))
- [WW 2022-01-30 — Blog post: Day 16 of $QQQ short term down-trend; Some end of decline signs I am looking for; Promising stock s](../../raw/posts/2022-01-30-blog-post-day-16-of-qqq-short-term-down-trend-some-end-of-decline-signs-i-am-looking-for-promising-stock-scan.md) ([summary](../sources/2022-01-30-blog-post-day-16-of-qqq-short-term-down-trend-some-end-of-decline-signs-i-am-looking-for-promising-stock-scan.md))
- [WW 2016-12-04 — New $QQQ short term down-trend; $NFLX breaking out? TC2000 scan results: 7 rocket stocks](../../raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md) ([summary](../sources/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md))
