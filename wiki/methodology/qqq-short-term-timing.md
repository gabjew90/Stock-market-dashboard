---
title: QQQ Short-Term Timing
type: entity
updated: 2026-05-12
sources:
  - raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md
  - raw/posts/2021-06-13-follow-on-to-traderlion-conference-this-wednesdays-long-island-talk-examples-of-black-dot-signals-gmi6-of-6.md
  - raw/posts/2013-10-20-can-ta-protect-ourselves-from-a-1987-type-of-market-crash-speculative-bull-market-phase-beginning-tplm-green.md
  - raw/posts/2011-08-07-crash-coming-only-3rd-day-of-new-qqq-short-term-down-trend.md
  - raw/posts/2019-04-07-trading-ipos-with-a-glb-and-a-green-dot-signal-iipr-qqq-short-term-up-trend-is-in-61st-day.md
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

## Relationship to the GMI

The QQQ short-term timing count is separate from, but published alongside, the GMI. Several GMI components measure the QQQ's daily and weekly trend — the short-term count overlaps with these but is more granular (it counts days; the GMI components are binary). When the GMI goes GREEN (≥ 4), the QQQ is typically also in a short-term up-trend. When the GMI flashes RED (≤ 3), the QQQ short-term count is typically down.

## Evolution

The count was present from the blog's earliest posts (2005) and appears in post titles consistently. The flip rule is now well-evidenced: closing below/above the **30-day moving average** is the primary trigger; the 10-week average may be a secondary confirmation. See the "What it is" section above for full evidence.

*Note: In early posts (2005–2010) the ETF was called QQQQ (4 Qs); it was later renamed QQQ (3 Qs). Same index.*

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

## Sources

- [WW 2005-06-05 — GMI back to +5; on moving averages](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md) ([summary](../sources/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md))
- [WW 2011-03-07 — Introducing the GMI2](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md) ([summary](../sources/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md) ([summary](../sources/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))
- [WW 2014-10-13 — 11th day of QQQ down-trend; how long will this decline last?](../../raw/posts/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md) ([summary](../sources/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md))
- [WW 2021-06-13 — TraderLion conference; black dot signals; GMI=6](../../raw/posts/2021-06-13-follow-on-to-traderlion-conference-this-wednesdays-long-island-talk-examples-of-black-dot-signals-gmi6-of-6.md) ([summary](../sources/2021-06-13-follow-on-to-traderlion-conference-this-wednesdays-long-island-talk-examples-of-black-dot-signals-gmi6-of-6.md))
- [WW 2013-10-20 — TA vs 1987 crash; 30-day MA as short-term trend signal](../../raw/posts/2013-10-20-can-ta-protect-ourselves-from-a-1987-type-of-market-crash-speculative-bull-market-phase-beginning-tplm-green.md) ([summary](../sources/2013-10-20-can-ta-protect-ourselves-from-a-1987-type-of-market-crash-speculative-bull-market-phase-beginning-tplm-green.md))
- [WW 2011-08-07 — Crash coming? 3rd day of QQQ short-term down-trend](../../raw/posts/2011-08-07-crash-coming-only-3rd-day-of-new-qqq-short-term-down-trend.md) ([summary](../sources/2011-08-07-crash-coming-only-3rd-day-of-new-qqq-short-term-down-trend.md))
- [WW 2019-04-07 — IPO GLB; IIPR; QQQ trend duration statistics updated through 2019](../../raw/posts/2019-04-07-trading-ipos-with-a-glb-and-a-green-dot-signal-iipr-qqq-short-term-up-trend-is-in-61st-day.md) ([summary](../sources/2019-04-07-trading-ipos-with-a-glb-and-a-green-dot-signal-iipr-qqq-short-term-up-trend-is-in-61st-day.md))
