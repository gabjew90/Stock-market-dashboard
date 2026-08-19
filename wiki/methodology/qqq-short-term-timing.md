---
title: QQQ Short-Term Timing
type: entity
updated: 2026-08-18
sources:
  - raw/posts/2008-10-22-gmi-0-gmi-r-0-t2108-3-36th-day-of-qqqq-short-term-down-trend-lphi-my-ta-course.md
  - raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md
  - raw/posts/2021-06-13-follow-on-to-traderlion-conference-this-wednesdays-long-island-talk-examples-of-black-dot-signals-gmi6-of-6.md
  - raw/posts/2013-10-20-can-ta-protect-ourselves-from-a-1987-type-of-market-crash-speculative-bull-market-phase-beginning-tplm-green.md
  - raw/posts/2011-08-07-crash-coming-only-3rd-day-of-new-qqq-short-term-down-trend.md
  - raw/posts/2019-04-07-trading-ipos-with-a-glb-and-a-green-dot-signal-iipr-qqq-short-term-up-trend-is-in-61st-day.md
  - raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md
  - raw/posts/2022-07-10-blog-post-day-1-of-new-qqq-short-term-up-trend-closes-above-10-week-average-9-stocks-near-ath-with-rs-at-50-w.md
  - raw/posts/2005-06-02-gmi-goes-to-the-max-6-cme-qsii-cmn.md
  - raw/posts/2005-06-07-a-strange-day-gmi-back-to-6.md
  - raw/posts/2005-07-28-another-strong-day-gmi-6-and-its-track-record-benefits-of-naked-charts-some-darvas-type-stocks.md
  - raw/posts/2013-06-24-sell-in-may-worked-my-confession-d-9-of-current-short-term-down-trend.md
  - raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md
---

# QQQ Short-Term Timing

Dr. Wish's faster on/off signal for the Nasdaq-100 (QQQ). He tracks whether the QQQ is in a short-term up-trend or down-trend, and counts the number of days it has been in the current trend. Blog post titles routinely read "Day N of QQQ short-term up/down-trend."

## What it is

Dr. Wish tracks a day-count for the QQQ's short-term trend. Each day he notes whether the QQQ is in an up-trend (U) or down-trend (D) and increments the count. Examples from the posts:

- "We are in day 20 (U-20) of the QQQQ up trend." ([WW 2005-06-05](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md))
- "My short term trend count for the QQQQ is up again, at U-1. Since the large short term up-trend ended at U-64, there have been 3 small trends (D-3, U-2, D-2), and now the new up-trend." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- An up-trend of 56 days ended, then the count switched to down: "My QQQ short term trend count has now changed to down, after 56 days of a QQQ short term up-trend." ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

The exact published rule that flips the signal has never been spelled out in a single definitional post. However, two strong lines of evidence converge on the **30-day moving average of closing prices** as the flip criterion:

1. In his 2013 retrospective on the 1987 crash, Dr. Wish applies his "current techniques" to historical daily Dow charts and explicitly states: "The 30 day moving average of closing prices (red line) had already curved down… Using my current techniques, by this time, I would have already declared the Dow to be in a short term down-trend." The 1987 crash came on what he identifies as Day 9 of the resulting down-trend. ([WW 2013-10-20](../../raw/posts/2013-10-20-can-ta-protect-ourselves-from-a-1987-type-of-market-crash-speculative-bull-market-phase-beginning-tplm-green.md))

2. A 2022 post title reads "Day 1 of new QQQ short-term up-trend, **closes above 10 week average**" — indicating the 10-week (≈50-day) average may also be involved. The post body says "My QQQ short term indicator has turned up, U-1." ([WW 2022-07-10](../../raw/posts/2022-07-10-blog-post-day-1-of-new-qqq-short-term-up-trend-closes-above-10-week-average-9-stocks-near-ath-with-rs-at-50-w.md))

3. He has also said the 30-day moving average is "the most reliable indicator of the short term trend." ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))

The best current reading: **the QQQ short-term trend is up when QQQ closes above its 30-day moving average; the day count flips when price crosses the 30-day MA on a closing basis.** The 10-week average appears to function as a secondary confirmation rather than the primary signal. This is consistent with the code's approximation in `src/ww/indicators/qqq_timing.py`, which uses the 30-day SMA. The "technical indicators not disclosed" language in the original 2005 GMI post may refer to a combination (MACD, stochastic, etc.) rather than just the moving average — but the closing price vs 30-day MA is the best single proxy confirmed in text.

Note: Dr. Wish has *never* published a complete rule specification. The above is inferred from multiple posts; treat it as a well-supported approximation, not a verbatim disclosure.

## How he uses it

The QQQ short-term trend count is used alongside the [GMI](gmi.md):

- **New up-trend:** a buy signal (used in combination with GMI ≥ 4 and both the market and stock in Stage 2).
- **New down-trend:** he often makes a small purchase of the 3X bearish QQQ ETF (SQQQ) as a hedge; he adds to it only if the down-trend lasts 5–6 days. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

### Down-trend duration statistics

Most QQQ short-term down-trends since 2006 are short: "about one quarter of new short term down-trends have lasted less than 6 days." He does not automatically go fully defensive — he waits to see if the down-trend persists before adding to his short position. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

An April 2019 post included the most detailed published tabulation of QQQ trend duration statistics, updated through March 2019 (data going back to 2006): about **40% of new QQQ short-term down-trends end in fewer than 6 days**; 60% of both up-trends and down-trends last 6–47 days; the longest recorded up-trend in the dataset was 88 days; the longest down-trend was 69 days. Dr. Wish was in Day 61 of an up-trend when writing the post. These statistics explain his discipline of taking a small SQQQ position on Day 1 of a down-trend and adding to it only after Day 5 — by that point, the probability of a quick reversal has dropped substantially. ([WW 2019-04-07](../../raw/posts/2019-04-07-trading-ipos-with-a-glb-and-a-green-dot-signal-iipr-qqq-short-term-up-trend-is-in-61st-day.md))

A 2016 statement of the same base rate: "many (about 40%) QQQ short term down-trends end in under 5 days" — matching the 2019 tabulation and superseding the "about one quarter" figure of 2014. ([WW 2016-12-04](../../raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md))

## Relationship to the GMI

The QQQ short-term timing count is separate from, but published alongside, the GMI. Several GMI components measure the QQQ's daily and weekly trend — the short-term count overlaps with these but is more granular (it counts days; the GMI components are binary). When the GMI goes GREEN (≥ 4), the QQQ is typically also in a short-term up-trend. When the GMI flashes RED (≤ 3), the QQQ short-term count is typically down.

## Evolution

The count was present from the blog's earliest posts (2005) and appears in post titles consistently. The flip rule is now well-evidenced: closing below/above the **30-day moving average** is the primary trigger; the 10-week average may be a secondary confirmation. See the "What it is" section above for full evidence.

*Note: In early posts (2005–2010) the ETF was called QQQQ (4 Qs); it was later renamed QQQ (3 Qs). Same index.*

**2005 — the 10-day line.** In the first summer the operative short-term line for the QQQQ was its 10-day moving average: "in this rise as in the prior May rally the QQQQ consistently closed above its rising 10 day moving average… Hint: When is the market weakening? Wait for a close below the dotted line." ([WW 2005-07-28](../../raw/posts/2005-07-28-another-strong-day-gmi-6-and-its-track-record-benefits-of-naked-charts-some-darvas-type-stocks.md)) A first close under it after 26 days was read as "the steep rise may be over" and the cue to move stops up. ([WW 2005-06-07](../../raw/posts/2005-06-07-a-strange-day-gmi-back-to-6.md)) And the first duration base rate: the comparable up-trend before May 2005 "lasted about 92 trading days." ([WW 2005-06-02](../../raw/posts/2005-06-02-gmi-goes-to-the-max-6-cme-qsii-cmn.md))

**2013 — a criterion experiment, tried and reverted.** In June 2013 he adopted a new short-term-trend-change criterion "trying to minimize the risk of being whip-sawed in my short term trend count." It cost him the start of a decline: "in doing so, I missed the beginning of the current decline. So I went back to my original method and counted the down trend from where it would have begun" — and re-published the corrected sequence (U-31 ending June 5, a 2-day down-trend, a 2-day up-trend, then the current down-trend from June 12). Two-day trends are therefore *expected output* of the rule he uses, not a defect to be filtered. ([WW 2013-06-24](../../raw/posts/2013-06-24-sell-in-may-worked-my-confession-d-9-of-current-short-term-down-trend.md)) The published day counts are also corrected in public when readers question them.

## Code — an approximation of the day count

Based on the evidence above (see "What it is"), the 30-day MA rule is now well-supported rather than merely a proxy. [`src/ww/indicators/qqq_timing.py`](../../src/ww/indicators/qqq_timing.py) uses *close above its 30-day SMA = up* — this matches his explicit 2013 description of his current techniques. The day count tracks consecutive days since the last MA crossing:

```python
def short_term_trend(daily_close, *, window=30):
    ma = daily_close.astype(float).rolling(window).mean()
    return "up" if daily_close.iloc[-1] > ma.dropna().iloc[-1] else "down"

def trend_day_count(daily_close, *, window=30):
    t = (daily_close.astype(float) > daily_close.astype(float).rolling(window).mean()).dropna()
    last, n = t.iloc[-1], 0
    for v in reversed(t.tolist()):
        if v == last: n += 1
        else: break
    return n
```

`ww compute qqq-timing QQQ` prints the approximated trend and day count — with the caveat printed alongside.

## See also

- [General Market Index (GMI)](gmi.md)
- [Moving-average rules](moving-average-rules.md)
- [Risk & cash](risk-and-cash.md)
- [Market-state playbook](../playbooks/market-state.md)

## Duration base rates — the reasoning, live in 2008

The published trend-duration statistics (2019) have an earlier, working form: on Day 36 of the
autumn 2008 down-trend he reasoned from the year's own prior episodes — "The short term
down-trend... that ended on March 24, lasted **55 days**, and the one that ended on August 5,
lasted **39 days**. So, **we may have a ways to go**." The reference class is recent same-regime
trends, and the output is an expectation, not a prediction. He also kept the short/long split
working mid-crisis: a reversal "would occur within a longer term down-trend but **could still be
a trade-able rally**." ([WW 2008-10-22](../../raw/posts/2008-10-22-gmi-0-gmi-r-0-t2108-3-36th-day-of-qqqq-short-term-down-trend-lphi-my-ta-course.md))

## Sources

- [WW 2005-06-05 — GMI back to +5; on moving averages](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md) ([summary](../sources/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md))
- [WW 2011-03-07 — Introducing the GMI2](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md) ([summary](../sources/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md) ([summary](../sources/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))
- [WW 2014-10-13 — 11th day of QQQ down-trend; how long will this decline last?](../../raw/posts/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md) ([summary](../sources/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md))
- [WW 2021-06-13 — TraderLion conference; black dot signals; GMI=6](../../raw/posts/2021-06-13-follow-on-to-traderlion-conference-this-wednesdays-long-island-talk-examples-of-black-dot-signals-gmi6-of-6.md) ([summary](../sources/2021-06-13-follow-on-to-traderlion-conference-this-wednesdays-long-island-talk-examples-of-black-dot-signals-gmi6-of-6.md))
- [WW 2013-10-20 — TA vs 1987 crash; 30-day MA as short-term trend signal](../../raw/posts/2013-10-20-can-ta-protect-ourselves-from-a-1987-type-of-market-crash-speculative-bull-market-phase-beginning-tplm-green.md) ([summary](../sources/2013-10-20-can-ta-protect-ourselves-from-a-1987-type-of-market-crash-speculative-bull-market-phase-beginning-tplm-green.md))
- [WW 2011-08-07 — Crash coming? 3rd day of QQQ short-term down-trend](../../raw/posts/2011-08-07-crash-coming-only-3rd-day-of-new-qqq-short-term-down-trend.md) ([summary](../sources/2011-08-07-crash-coming-only-3rd-day-of-new-qqq-short-term-down-trend.md))
- [WW 2019-04-07 — IPO GLB; IIPR; QQQ trend duration statistics updated through 2019](../../raw/posts/2019-04-07-trading-ipos-with-a-glb-and-a-green-dot-signal-iipr-qqq-short-term-up-trend-is-in-61st-day.md) ([summary](../sources/2019-04-07-trading-ipos-with-a-glb-and-a-green-dot-signal-iipr-qqq-short-term-up-trend-is-in-61st-day.md))
- [WW 2005-07-17 — GMI since inception; introducing the WPM](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md) ([summary](../sources/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))
- [WW 2022-07-10 — Day 1 of new QQQ short-term up-trend; closes above 10-week average](../../raw/posts/2022-07-10-blog-post-day-1-of-new-qqq-short-term-up-trend-closes-above-10-week-average-9-stocks-near-ath-with-rs-at-50-w.md)
- [WW 2008-10-22 — Down-trend duration as a base rate; rockets inside the crash](../../raw/posts/2008-10-22-gmi-0-gmi-r-0-t2108-3-36th-day-of-qqqq-short-term-down-trend-lphi-my-ta-course.md) ([summary](../sources/2008-10-22-gmi-0-gmi-r-0-t2108-3-36th-day-of-qqqq-short-term-down-trend-lphi-my-ta-course.md))
- [WW 2005-06-02 — GMI goes to the max: +6, CME, QSII, CMN](../../raw/posts/2005-06-02-gmi-goes-to-the-max-6-cme-qsii-cmn.md) ([summary](../sources/2005-06-02-gmi-goes-to-the-max-6-cme-qsii-cmn.md))
- [WW 2005-06-07 — A strange day, GMI back to +6](../../raw/posts/2005-06-07-a-strange-day-gmi-back-to-6.md)
- [WW 2005-07-28 — Another strong day; GMI: +6 and its track record; Benefits of naked charts; Some Darvas type stocks](../../raw/posts/2005-07-28-another-strong-day-gmi-6-and-its-track-record-benefits-of-naked-charts-some-darvas-type-stocks.md) ([summary](../sources/2005-07-28-another-strong-day-gmi-6-and-its-track-record-benefits-of-naked-charts-some-darvas-type-stocks.md))
- [WW 2013-06-24 — Sell in May worked?  My confession; D-9 of current short term down-trend](../../raw/posts/2013-06-24-sell-in-may-worked-my-confession-d-9-of-current-short-term-down-trend.md) ([summary](../sources/2013-06-24-sell-in-may-worked-my-confession-d-9-of-current-short-term-down-trend.md))
- [WW 2016-12-04 — New $QQQ short term down-trend; $NFLX breaking out? TC2000 scan results: 7 rocket stocks](../../raw/posts/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md) ([summary](../sources/2016-12-04-new-qqq-short-term-down-trend-nflx-breaking-out-tc2000-scan-results-7-rocket-stocks.md))
