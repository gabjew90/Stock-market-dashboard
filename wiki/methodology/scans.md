---
title: The scans — how he finds candidates in TC2000 and IBD
type: concept
updated: 2026-08-18
sources:
  - raw/posts/2013-05-20-how-to-find-a-tsla-like-explosive-stock-before-its-huge-advance-more-green-line-break-outs.md
  - raw/posts/2014-09-28-this-market-is-not-out-of-the-woods-finding-bio-tech-stars-like-agio-and-vrtx.md
  - raw/posts/2016-11-27-new-tc2000-scan-yields-4-break-outs-from-consolidation-wb-sina-hpp-arcw.md
  - raw/posts/2017-01-29-on-david-ryan-and-my-new-tc2000-scan-for-glb-rockets-bouncing-off-up-of-support-play.md
  - raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md
  - raw/posts/2017-07-23-tc2000-scan-for-bounce-up-off-of-support-pets-unleashed-cboe-yellowband.md
  - raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md
  - raw/posts/2020-09-20-10-doublers-that-last-week-reached-an-ath-on-above-average-volume-and-how-i-found-them-apps-trup-dkng-fvrr-nv.md
  - raw/posts/2020-10-04-how-i-used-the-ibd-screener-to-identify-36-launched-rocket-stocks-even-so-the-market-remains-in-short-term-do.md
  - raw/posts/2022-04-17-blog-post-qqq-and-spy-closed-back-below-their-10-week-averages-gmi-remains-red-cash-is-king-but-there-are-25.md
  - raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md
  - raw/posts/2015-03-01-on-my-use-of-the-gmi-some-darvas-type-rwb-rocket-stocks-ambaleaf.md
  - raw/posts/2022-06-26-blog-post-qqq-short-term-down-trend-may-end-monday-69-of-nasdaq100-stocks-in-hourly-rwb-up-trends-scan-shows.md
  - raw/posts/2010-06-21-some-stocks-near-all-time-highs-since-june-4-ibd100-stocks-3x-more-likely-to-rise-10.md
  - raw/posts/2016-12-11-all-gmi-components-positive-qqq-near-all-time-peak-new-tc2000-scan-for-bounces-celg.md
  - raw/posts/2022-10-03-blog-post-day-25-of-qqq-short-term-down-trend-see-my-new-way-to-scan-for-stocks-near-their-recent-ath-and-glb.md
---

# The scans — how he finds candidates in TC2000 and IBD

Dr. Wish's candidate list is produced mechanically. Every few years he publishes a new TC2000 scan (and, from 2020, an IBD-screener workflow), each with its criteria stated well enough to reproduce — and several are posted to his TC2000 club by name. This page catalogues them in the order they appeared, with the criteria as published; the *philosophy* of what he is looking for (launched rockets, already-doubled, the fundamental overlay, the price-level rule) stays on [stock-selection](stock-selection.md), and the daily-chart bounce triggers that several of these scans feed (BOS, the dots, x8/x21/30) are on [entry-signals](entry-signals.md). Every scan runs against a hand-built all-time-high watchlist — see [building the ATH watchlist](stock-selection.md#building-the-ath-watchlist--and-tc2000s-survivorship-trap).

## The daily RWB scan — finding RWB-bounce entries (introduced 2017)

For timing entries, Dr. Wish uses a **daily** RWB chart with the Red Line Count (RLC) metric. An advancing stock will have RLC = 6 (above all six red lines). A stock that dips below all red lines (RLC = 0) and then recovers above all of them is a re-entry candidate — the "RWB bounce." He published a TC2000 scan (12162017DailyRWBBounce) that finds such stocks. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))

Filter condition: any stock in the scan that is **not above its last green line top** is disqualified because of overhead supply from prior buyers at higher prices. ([WW 2017-12-17](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))

For market-wide assessment using the same tool: monitor QQQ, SPY, and DIA RLCs. In March 2017, SPY had RLC = 0 and the Dow Jones Transportation Average had lost its entire RWB pattern — a warning he flagged as a potential Dow Theory caution. ([WW 2017-03-19](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))

## The weekly doubler-ATH scan (2020) — full syntax

Darvas's doubled-in-a-year criterion operationalised as a weekly TC2000 column scan, syntax
published verbatim: `H=maxH50` (52-week high this week); `H>2*H50 or H>1.5*MinL50` (doubled
year-over-year, or 1.5× off the yearly low); `V>1.3*AvgV50` (breakout-week volume 130% of
average); `C>20` ("I don't buy cheap stocks"). Yield: 74 of 5,096 US stocks, 25 of his 948-stock
IBD/MS watchlist. The scan feeds the GLB step rather than replacing it — each survivor's
*monthly* chart is opened and the green line drawn by hand. Best example of the doubling logic:
"Taser went up 7x, consolidated, and then went up 7x again." ([WW 2020-09-20](../../raw/posts/2020-09-20-10-doublers-that-last-week-reached-an-ath-on-above-average-volume-and-how-i-found-them-apps-trup-dkng-fvrr-nv.md))

## The weekly consolidation-breakout scan (2016) — and short interest as fuel

A weekly-chart scan for growth stocks emerging from a **multi-week consolidation**: minimum
weekly volume, **above-average volume on the breakout week**, latest quarterly EPS **≥ +50%** —
4 survivors out of ~4,900. The annotated WB chart documents his chart-header legend: latest
quarterly EPS, price ÷ price-250-days-ago (WB at 2.64×, the doubled-in-a-year check), projected
earnings date, and the **short interest ratio read as breakout fuel**: at 3.6 days-to-cover,
"the higher the number, the greater the buying pressure from a break-out" — shorts as future
forced buyers. Epistemic tag attached even to his own hits: highest weekly volume since 2014
"could signify the resumption of the up-trend **or it could mean nothing**."
([WW 2016-11-27](../../raw/posts/2016-11-27-new-tc2000-scan-yields-4-break-outs-from-consolidation-wb-sina-hpp-arcw.md))

## The weekly green bar scan — a later entry filter (formalized 2022–2024)

Dr. Wish also runs a weekly scan for "green bar" setups — stocks bouncing off the rising 4-week average. An early version of the scan criteria (April 2022) required: (1) stock in 4wk>10wk>30wk alignment (Stage 2), (2) bounced off the rising 4-week average last week, (3) weekly close *higher than the prior week's close* (this is the "green bar" — a week that does not close higher is not green even if it bounced the 4wk avg), (4) RS vs S&P 500 at a 20-week high, (5) hit an ATH last week. Candidate pool: the IBD/MarketSmith watchlist. ([WW 2022-04-17](../../raw/posts/2022-04-17-blog-post-qqq-and-spy-closed-back-below-their-10-week-averages-gmi-remains-red-cash-is-king-but-there-are-25.md))

By 2024 the formalized scan added: weekly 10.4 stochastic above 80 for at least 5 weeks; stock up ≥ 50% from a year ago. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))

**Trailing stop rules for WGB positions (explicit):** "An advancing stock rides its rising 4 wk avg for many weeks." Stop logic: (1) initial stop: sell if stock trades back below last week's low; (2) trailing: lighten or sell when the stock ends a week *below its 4-week average*; (3) final exit: close below the 10-week average. Can also trail stop at each subsequent green bar's low. ([WW 2022-04-17](../../raw/posts/2022-04-17-blog-post-qqq-and-spy-closed-back-below-their-10-week-averages-gmi-remains-red-cash-is-king-but-there-are-25.md))

The weekly approach gives more entry opportunities than waiting for a bounce off the 10-week average: in ANF's 2023–2024 up-trend, the 4-week average generated 20+ green-bar entries vs. only 4 bounces off the 10-week average. ([WW 2024-05-27](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))

**The WGB scan works during GMI Red periods** if a subsector is in Stage 2. In April 2022, 25 stocks (commodities, oil/defense) passed the scan while the broader market was in Stage 4. ([WW 2022-04-17](../../raw/posts/2022-04-17-blog-post-qqq-and-spy-closed-back-below-their-10-week-averages-gmi-remains-red-cash-is-king-but-there-are-25.md))

## ATH-past-40-days + lower Bollinger Band pullback scan (introduced 2017)

David Ryan (William O'Neil's protege), as quoted in _Momentum Masters_ (2015, p. 72): "I basically simplify it down to two, breakouts and pullbacks. Don't get confused by all the different formations. You just have to draw a line across the top of where most of the stock's trading has taken place. Then you buy as it moves through that line… Buying pullbacks are a bit more complicated but offer another entry point to get aboard a leading stock." ([WW 2017-01-29](../../raw/posts/2017-01-29-on-david-ryan-and-my-new-tc2000-scan-for-glb-rockets-bouncing-off-up-of-support-play.md))

In January 2017, Dr. Wish created a new TC2000 scan (name: `01292017ATHhipast40daysBLBB`) that embodies the pullback approach. Applied to his ~800-stock ATH watchlist, it finds:

1. Stock hit a new all-time high within the past 40 days
2. Stock is currently bouncing up from its lower Bollinger Band (15.2 setting)

This is distinct from the [BOS scan](stock-selection.md) (which uses a broader universe and a different trigger). The purpose is to find post-GLB pullback re-entries: stocks that already broke out, pulled back to oversold levels, and are resuming the advance. A pullback/bounce entry **does not require elevated volume** (unlike the GLB itself). Low volume on the pullback is a positive sign — selling has dried up. The stop is placed just below the recent bounce low. ([WW 2017-01-29](../../raw/posts/2017-01-29-on-david-ryan-and-my-new-tc2000-scan-for-glb-rockets-bouncing-off-up-of-support-play.md))

## The triple-support bounce scan (2017)

The strictest member of the bounce family: stocks that "bounced up off of **3 daily indicators
of support/over-sold** within the past few days," ≥50% above the 250-day low, above $15 — **8 of
4,800**. The PETS hit stacked everything at once: May GLB on high volume, consolidation, doubled
in a year, EPS +37%/Comp 96/RS 98, and a rising yellowband. And the earnings-date hazard handled
out loud: "PETS reports earnings on Monday morning... What to do? **Buy PETS a collar?!**"
([WW 2017-07-23](../../raw/posts/2017-07-23-tc2000-scan-for-bounce-up-off-of-support-pets-unleashed-cboe-yellowband.md))

## The biotech scan — volume plus news catalyst

In addition to the general RWB/GLB scans, Dr. Wish runs a specialized scan for biotech stocks. The combination: technical unusual-volume alert + fundamental news-catalyst reading.

**TC2000 scan:** each evening, scan for biotech stocks that advanced on **unusually high volume** that day. High volume in a biotech signals that someone knows something.

**News-catalyst reading:** read news reports about drug companies' scheduled clinical trial presentations or FDA review dates. "Being in the research field, I know that one schedules public presentations to highlight good research results." An upcoming major presentation is a likely positive-catalyst indicator.

**AGIO example (September 2014):** AGIO had a major presentation scheduled at a Leerink conference. The nightly scan had flagged it. The stock "took off" the next day. ([WW 2014-09-28](../../raw/posts/2014-09-28-this-market-is-not-out-of-the-woods-finding-bio-tech-stars-like-agio-and-vrtx.md))

**General rule:** the scan produces candidates; the news determines which are worth owning. Dr. Wish maintains a growing watchlist of stocks that have appeared in the scan and monitors them over time for further technical strength. He intentionally does not publish specific output because he wants people to do their own due diligence.

**3:45 PM intraday timing rule:** "I restrict most of my daily trading to around 3:45 PM when I can estimate where things will close. If I trade earlier in the day I am often whipsawed." ([WW 2014-09-28](../../raw/posts/2014-09-28-this-market-is-not-out-of-the-woods-finding-bio-tech-stars-like-agio-and-vrtx.md))

## The IBD screener workflow (2020)

A four-criterion screen on IBD's own tool: "**RS 90-99, ACC/DIS = A or B, Price >30, Next
Quarter EPS est >100%**" — 36 survivors out of 7,000+, exported to Excel and imported into
TC2000 for alerts on his set-ups. The survivors read like his existing watchlist (CRWD, DDOG,
ETSY, PTON, ZM, ZS), which is the point: the screen mechanises the sourcing. The engine behind
the criteria: "William O'Neil and David Ryan teach people to buy great stocks with proven or
expected large earnings increases. **Great earnings propel stocks higher**" — and the origin
credit, "I began to make money in the market after reading [O'Neil's book]." Tutorial video by
his student Richard Moglen. ([WW 2020-10-04](../../raw/posts/2020-10-04-how-i-used-the-ibd-screener-to-identify-36-launched-rocket-stocks-even-so-the-market-remains-in-short-term-do.md))

## The TSLA GLB workflow — step by step

The clearest description of the full GLB detection workflow, using TSLA's April 2013 breakout as the teaching case ([WW 2013-05-20](../../raw/posts/2013-05-20-how-to-find-a-tsla-like-explosive-stock-before-its-huge-advance-more-green-line-break-outs.md)):

1. **Evening scan:** run a scan for stocks hitting new 52-week highs. TSLA appeared on the new-high list on April 1, 2013.
2. **Monthly GLB check:** immediately look at the monthly chart. TSLA closed at $43.93 on April 1 — well above its prior peak of $39.95 from March 2012. Draw the green line at $39.95.
3. **Weekly chart:** check for confirmation via volume. TSLA's weekly volume on the breakout week was "the highest weekly volume ever" — a sign of institutional accumulation.
4. **Daily chart:** look for a gap-up above the green line on high daily volume. TSLA gapped to a new all-time high on above-average volume on April 1.
5. **Re-test entry:** TSLA pulled back to the green line ($39.95) after the initial breakout, giving a lower-risk second entry. If the stock closes back below the green line after the re-test, exit with a small loss.

**IPO advantage:** TSLA was a recent IPO in a new growth industry (battery-powered cars). Most funds would not yet own it — therefore a large future buyer base existed. IPO stocks breaking to new ATHs often carry this advantage.

**General principle:** "Why are so many people averse to buying stocks that break from a multi-month base (green line top) to a new all-time high? In the stock market I do not want to buy bargains." ([WW 2013-05-20](../../raw/posts/2013-05-20-how-to-find-a-tsla-like-explosive-stock-before-its-huge-advance-more-green-line-break-outs.md))

## The new-high + EPS ≥ 50% scan (2010)

The 2010 form of the leader search: stocks that hit a new 52-week high on the day, are near their all-time high, and posted a most-recent-quarter EPS increase of at least +50%; the review table adds the prior quarter's EPS change, annual EPS, P/E, price ÷ price a year ago, last-quarter revenue change and P/S. On 2010-06-18 it produced 11 names, all with rising revenue and 64% already flagged from his IBD100/New America lists; "the next step is to research each stock's fundamentals and business concept before considering a purchase." ([WW 2010-06-21](../../raw/posts/2010-06-21-some-stocks-near-all-time-highs-since-june-4-ibd100-stocks-3x-more-likely-to-rise-10.md))

## The stochastic bounce scan (2016) — the green dot's ancestor

Posted to his TC2000 club in December 2016 and specified in full: **(1)** the fast daily 10.4 stochastic above the slow 10.4.4, the fast **< 20 within the past 2 days** (rising from oversold) and **≤ 50** (not extended), close above the 50-day average; **(2)** at least a **15% rise from the 50-day low** at some point in the past 50 days; **(3)** volume > 100,000. Five hits on 2016-12-09 (CELG, MMS, HELE, AVXS, FTV; HELE dropped for a Stage II decline). The trade as taught on CELG: buy, stop below the recent bounce just under $110, and sell "if/when the fast stochastics closes back below the slow stochastics"; a bounce off the lower 15.2 daily Bollinger Band is a bonus "not required by this scan." ([WW 2016-12-11](../../raw/posts/2016-12-11-all-gmi-components-positive-qqq-near-all-time-peak-new-tc2000-scan-for-bounces-celg.md)) Fifteen months later the same crossover became the [green dot](entry-signals.md).

## The relative-strength-at-a-50-week-high scan (2022)

Run on his ~780-stock IBD/MarketSmith watchlist during the 2022 bear: stocks **near an all-time high** whose **weekly relative strength versus SPY is at a 50-week high**, sorted by change from 250 days ago (HRMY +76% topped the June 2022 list of 12). The logic is the same as the weak-tape watchlist on [stock-selection](stock-selection.md#building-the-ath-watchlist--and-tc2000s-survivorship-trap): "any stock that can come through the recent market down-trend near an ATH is worth monitoring," whereas fallen leaders "may never come back to an ATH, as many people who bought at higher prices and rode them down are grateful to sell as soon as they can get their original investments back." LLY was the worked example, with a successful retest of its March 2022 GLB. ([WW 2022-06-26](../../raw/posts/2022-06-26-blog-post-qqq-short-term-down-trend-may-end-monday-69-of-nasdaq100-stocks-in-hourly-rwb-up-trends-scan-shows.md))

## The <5%-below-a-recent-ATH column scan (2022)

Built after his TraderLion presentation, on the argument that "most of the stocks that Bill O'Neil graphed as among his greatest winners were stocks that had bases at or approaching their all-time-highs." The point is to catch both stocks that have already had a [GLB](green-line-breakouts.md) and those still just under one. The TC2000 column, as published:

- **Price New High**, set to **monthly, 500-bar high within the last 3 bars** — a 500-month (~41-year) high made within the last three months.
- Daily formula **`h > .95*maxh60`** — today's high within 5% of the highest high of the last 60 days.
- **`C > 30`** and **`V > 10000`** "to get rid of junk."

He then draws the green lines on the survivors by hand and looks for setups. ([WW 2022-10-03](../../raw/posts/2022-10-03-blog-post-day-25-of-qqq-short-term-down-trend-see-my-new-way-to-scan-for-stocks-near-their-recent-ath-and-glb.md))

## The Darvas EasyScan (2015)

A TC2000 EasyScan he designed to approximate Darvas's selection criteria, run against ~6,000 stocks; on 2015-02-27 it returned 46 names, of which AMBA — above its green-line top, in a weekly RWB pattern — was the example. The criteria are not listed in the post; he points to his 2012 Houston TC2000 webinar for the walk-through. ([WW 2015-03-01](../../raw/posts/2015-03-01-on-my-use-of-the-gmi-some-darvas-type-rwb-rocket-stocks-ambaleaf.md))

## See also

- [Stock selection](stock-selection.md) — what the scans are looking *for*; the page this was split from
- [Entry signals](entry-signals.md) — BOS, black/green/blue dots, x8/x21/30 — the daily triggers several scans feed
- [Green Line Breakouts](green-line-breakouts.md) · [The oversold bounce](oversold-bounce.md) — the two setups the scans serve
- [Playbook — buying a GLB](../playbooks/buying-glb.md) · [Playbook — buying an OSB](../playbooks/buying-osb.md)
- [Glossary](glossary.md) — ATH-past-40-days scan, gap-up scan, submarine scan, doubler

## Sources

- [WW 2013-05-20 — TSLA GLB worked example; full stock-selection workflow](../../raw/posts/2013-05-20-how-to-find-a-tsla-like-explosive-stock-before-its-huge-advance-more-green-line-break-outs.md) ([summary](../sources/2013-05-20-how-to-find-a-tsla-like-explosive-stock-before-its-huge-advance-more-green-line-break-outs.md))
- [WW 2014-09-28 — Biotech scan; news catalyst; AGIO and VRTX; 3:45 PM rule](../../raw/posts/2014-09-28-this-market-is-not-out-of-the-woods-finding-bio-tech-stars-like-agio-and-vrtx.md) ([summary](../sources/2014-09-28-this-market-is-not-out-of-the-woods-finding-bio-tech-stars-like-agio-and-vrtx.md))
- [WW 2016-11-27 — The weekly consolidation-breakout scan; short interest as fuel](../../raw/posts/2016-11-27-new-tc2000-scan-yields-4-break-outs-from-consolidation-wb-sina-hpp-arcw.md) ([summary](../sources/2016-11-27-new-tc2000-scan-yields-4-break-outs-from-consolidation-wb-sina-hpp-arcw.md))
- [WW 2017-01-29 — David Ryan quote; ATH-past-40-days + lower BB pullback scan; PLAY](../../raw/posts/2017-01-29-on-david-ryan-and-my-new-tc2000-scan-for-glb-rockets-bouncing-off-up-of-support-play.md) ([summary](../sources/2017-01-29-on-david-ryan-and-my-new-tc2000-scan-for-glb-rockets-bouncing-off-up-of-support-play.md))
- [WW 2017-03-19 — How I use daily RWB charts to size up the market and individual stocks](../../raw/posts/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md) ([summary](../sources/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md))
- [WW 2017-07-23 — The triple-support bounce scan; PETS](../../raw/posts/2017-07-23-tc2000-scan-for-bounce-up-off-of-support-pets-unleashed-cboe-yellowband.md) ([summary](../sources/2017-07-23-tc2000-scan-for-bounce-up-off-of-support-pets-unleashed-cboe-yellowband.md))
- [WW 2017-12-17 — A strategy for deciding when to sell stocks; GDS, NVDA](../../raw/posts/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md) ([summary](../sources/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md))
- [WW 2020-09-20 — The weekly doubler-ATH scan, full syntax; the note on the monitor](../../raw/posts/2020-09-20-10-doublers-that-last-week-reached-an-ath-on-above-average-volume-and-how-i-found-them-apps-trup-dkng-fvrr-nv.md) ([summary](../sources/2020-09-20-10-doublers-that-last-week-reached-an-ath-on-above-average-volume-and-how-i-found-them-apps-trup-dkng-fvrr-nv.md))
- [WW 2020-10-04 — The IBD screener workflow; the all-12-GMMA exit line](../../raw/posts/2020-10-04-how-i-used-the-ibd-screener-to-identify-36-launched-rocket-stocks-even-so-the-market-remains-in-short-term-do.md) ([summary](../sources/2020-10-04-how-i-used-the-ibd-screener-to-identify-36-launched-rocket-stocks-even-so-the-market-remains-in-short-term-do.md))
- [WW 2022-04-17 — WeeklyGreenBar scan full criteria; trailing stop rule](../../raw/posts/2022-04-17-blog-post-qqq-and-spy-closed-back-below-their-10-week-averages-gmi-remains-red-cash-is-king-but-there-are-25.md) ([summary](../sources/2022-04-17-blog-post-qqq-and-spy-closed-back-below-their-10-week-averages-gmi-remains-red-cash-is-king-but-there-are-25.md))
- [WW 2024-05-27 — ANF worked example (weekly green bar)](../../raw/posts/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md) ([summary](../sources/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md))
- [WW 2015-03-01 — On my use of the GMI; pension self-correction; Darvas scan; AMBA](../../raw/posts/2015-03-01-on-my-use-of-the-gmi-some-darvas-type-rwb-rocket-stocks-ambaleaf.md) ([summary](../sources/2015-03-01-on-my-use-of-the-gmi-some-darvas-type-rwb-rocket-stocks-ambaleaf.md))
- [WW 2022-06-26 — QQQ down-trend may end Monday; 69% of Nasdaq-100 in hourly RWB up-trends; RS-at-50-week-high scan; LLY](../../raw/posts/2022-06-26-blog-post-qqq-short-term-down-trend-may-end-monday-69-of-nasdaq100-stocks-in-hourly-rwb-up-trends-scan-shows.md) ([summary](../sources/2022-06-26-blog-post-qqq-short-term-down-trend-may-end-monday-69-of-nasdaq100-stocks-in-hourly-rwb-up-trends-scan-shows.md))
- [WW 2010-06-21 — Stocks near all-time highs; IBD100 stocks 3× more likely to rise 10%+](../../raw/posts/2010-06-21-some-stocks-near-all-time-highs-since-june-4-ibd100-stocks-3x-more-likely-to-rise-10.md) ([summary](../sources/2010-06-21-some-stocks-near-all-time-highs-since-june-4-ibd100-stocks-3x-more-likely-to-rise-10.md))
- [WW 2016-12-11 — All GMI components positive; QQQ near ATH; new TC2000 scan for bounces: CELG](../../raw/posts/2016-12-11-all-gmi-components-positive-qqq-near-all-time-peak-new-tc2000-scan-for-bounces-celg.md) ([summary](../sources/2016-12-11-all-gmi-components-positive-qqq-near-all-time-peak-new-tc2000-scan-for-bounces-celg.md))
- [WW 2022-10-03 — Blog Post: Day 25 of $QQQ short term down-trend; See my new way to scan for stocks near their recent ATH and G](../../raw/posts/2022-10-03-blog-post-day-25-of-qqq-short-term-down-trend-see-my-new-way-to-scan-for-stocks-near-their-recent-ath-and-glb.md) ([summary](../sources/2022-10-03-blog-post-day-25-of-qqq-short-term-down-trend-see-my-new-way-to-scan-for-stocks-near-their-recent-ath-and-glb.md))
