---
title: QQQ Short-Term Timing
type: entity
updated: 2026-05-11
sources:
  - raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md
  - raw/posts/2021-06-13-follow-on-to-traderlion-conference-this-wednesdays-long-island-talk-examples-of-black-dot-signals-gmi6-of-6.md
---

# QQQ Short-Term Timing

Dr. Wish's faster on/off signal for the Nasdaq-100 (QQQ). He tracks whether the QQQ is in a short-term up-trend or down-trend, and counts the number of days it has been in the current trend. Blog post titles routinely read "Day N of QQQ short-term up/down-trend."

## What it is

Dr. Wish tracks a day-count for the QQQ's short-term trend. Each day he notes whether the QQQ is in an up-trend (U) or down-trend (D) and increments the count. Examples from the posts:

- "We are in day 20 (U-20) of the QQQQ up trend." ([WW 2005-06-05](../../raw/posts/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md))
- "My short term trend count for the QQQQ is up again, at U-1. Since the large short term up-trend ended at U-64, there have been 3 small trends (D-3, U-2, D-2), and now the new up-trend." ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- An up-trend of 56 days ended, then the count switched to down: "My QQQ short term trend count has now changed to down, after 56 days of a QQQ short term up-trend." ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

The exact rule that flips the signal from up to down (or vice versa) has not been disclosed in the posts ingested so far. Dr. Wish refers to "my technical indicators" without specifying them. He mentions the 30-day moving average as "the most reliable indicator of the short term trend," suggesting it plays a role. ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))

## How he uses it

The QQQ short-term trend count is used alongside the [GMI](gmi.md):

- **New up-trend:** a buy signal (used in combination with GMI ≥ 4 and both the market and stock in Stage 2).
- **New down-trend:** he often makes a small purchase of the 3X bearish QQQ ETF (SQQQ) as a hedge; he adds to it only if the down-trend lasts 5–6 days. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

### Down-trend duration statistics

Most QQQ short-term down-trends since 2006 are short: "about one quarter of new short term down-trends have lasted less than 6 days." He does not automatically go fully defensive — he waits to see if the down-trend persists before adding to his short position. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))

## Relationship to the GMI

The QQQ short-term timing count is separate from, but published alongside, the GMI. Several GMI components measure the QQQ's daily and weekly trend — the short-term count overlaps with these but is more granular (it counts days; the GMI components are binary). When the GMI goes GREEN (≥ 4), the QQQ is typically also in a short-term up-trend. When the GMI flashes RED (≤ 3), the QQQ short-term count is typically down.

## Evolution

The count was present from the blog's earliest posts (2005) and appears in post titles consistently. The exact flip rules have never been publicly documented in the posts ingested so far — this is one thing to look for in future ingests of his detailed methodology posts.

*Note: In early posts (2005–2010) the ETF was called QQQQ (4 Qs); it was later renamed QQQ (3 Qs). Same index.*

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
