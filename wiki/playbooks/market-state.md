---
title: Playbook — market state → stance
type: playbook
updated: 2026-05-11
sources:
  - raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md
  - raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md
  - raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md
  - raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md
  - raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md
---

# Playbook — market state → stance

Given the current readings of the [GMI](../methodology/gmi.md), [QQQ Short-Term Timing](../methodology/qqq-short-term-timing.md), and [T2108](../methodology/t2108.md), what posture should you take? This is a decision tree, not a formula — it requires judgment when signals conflict.

## Inputs

- [General Market Index (GMI)](../methodology/gmi.md) (0–6, GREEN if ≥ 4 / RED if ≤ 3)
- [QQQ Short-Term Timing](../methodology/qqq-short-term-timing.md) (up/down-trend; day count)
- [T2108](../methodology/t2108.md) (breadth: % of NYSE stocks above 40-day MA)
- New highs/lows count (breadth divergence signal)
- [Moving-average rules](../methodology/moving-average-rules.md) (30-week and 10-week averages of major indexes)

---

## Decision tree

### GMI ≥ 4 (GREEN)

**Full bull posture.** Be long; run the [GLB buying playbook](buying-glb.md). ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))

- **QQQ in a short-term up-trend:** normal bull mode. Buy GLBs. Add to winners.
- **QQQ in a short-term down-trend, early days (≤ 5 days):** most short-term down-trends last fewer than 6 days — do not panic. Optionally buy a small position in SQQQ (3X inverse QQQ) for a hedge. Add more SQQQ only if the down-trend lasts 5–6 days. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))
- **T2108 > 80% (overbought):** do not add new positions; move stops up to protect gains. The market can remain overbought for a while, but the risk of a pullback is elevated. ([WW 2010-09-27](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md)) ([WW 2010-03-15](../../raw/posts/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md))

### GMI ≤ 3 (RED)

**Defensive posture.** Get defensive in the trading IRA. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)) No new long entries. Raise stops. Reduce exposure.

- **GMI ≤ 3 for two consecutive readings:** move to cash or begin shorting. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- **QQQ/SPY closes below 30-week average:** become "very defensive" — stop all new buys, raise stops on all positions. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))
- **30-week average of QQQ/SPY turns down:** typically exit the market entirely. ([WW 2012-07-23](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md))

### Breadth divergence warning (supplement to GMI)

Even when GMI is GREEN, a surge in new lows while the index is at a high (divergence) is an early warning signal. The documented example: in November 2021, QQQ was at all-time highs (day U-26) while new lows reached 438. Dr. Wish exited the market at or near the QQQ peak and stayed out for over a year through the subsequent Stage 4 decline. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

Watch the daily new-high / new-low counts against the full US stock universe (filtered for close > $10 and volume > 10,000). A surge in new lows — particularly when the index is near highs — warrants raising stops or moving to cash even before the GMI turns RED. ([WW 2023-06-19](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))

### T2108 extremes as contrarian signals

- **T2108 < 10% (deeply oversold):** the market is near the bottom of a steep decline. Action: "grit my teeth while the market gossip is terrible and buy a market index ETF." This is a contrarian buy on the index — not on individual growth stocks. ([WW 2014-08-03](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md))
- **T2108 > 80% (overbought):** raise stops; do not add aggressively. Note: a high T2108 reading is "not as predictive as an extremely low reading below 10%" — the overbought signal is weaker than the oversold signal. ([WW 2010-09-27](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md))

---

## Stance summary table

| GMI | 30-wk MA | T2108 | Stance |
|-----|----------|-------|--------|
| ≥ 4 (GREEN) | QQQ above rising | < 80% | Full bull — buy GLBs |
| ≥ 4 (GREEN) | QQQ above rising | > 80% | Cautious bull — hold, move stops up |
| ≥ 4 (GREEN) | QQQ above rising | Divergence (new lows surge) | Warning — raise stops, consider reducing |
| ≤ 3 (RED) | QQQ above rising | Any | Defensive — no new buys, raise stops |
| Any | QQQ below 30-wk | Any | Very defensive — no new buys; if 30-wk turns down, exit market |
| ≤ 3 (RED) | 30-wk turning down | Any | Exit market |
| Any | Any | < 10% | Contrarian index buy opportunity |

---

## Notes / caveats

- Dr. Wish distinguishes the **trading IRA** (follows these rules actively) from the **university pension** (stays long). The stances here apply only to the trading IRA. ([WW 2011-03-07](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md))
- The GMI can change quickly — moving from 3 to 6 in a single day is documented. "When the instruments tell me the market is reversing direction, I must act on it and not fight it." ([WW 2005-07-17](../../raw/posts/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md))
- The 70%+ rule: more than 70% of all stocks move in the same direction as the major market indexes. Buying growth stocks in a downtrend puts the odds against you. ([WW 2005-04-23](../../raw/posts/2005-04-23-lets-talk-strategy.md))

## See also

- [Risk & cash](../methodology/risk-and-cash.md)
- [General Market Index (GMI)](../methodology/gmi.md)
- [T2108](../methodology/t2108.md)
- [QQQ Short-Term Timing](../methodology/qqq-short-term-timing.md)
- [Exits](exits.md)

## Sources

- [WW 2011-03-07 — Introducing the GMI2](../../raw/posts/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md)
- [WW 2014-08-03 — GMI 10-Day New High Indicator; T2108; AAPL](../../raw/posts/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md)
- [WW 2012-07-23 — Stage analysis and green line charts](../../raw/posts/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md)
- [WW 2023-06-19 — How I compute new US highs and lows; 11/2021 exit](../../raw/posts/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md) ([summary](../sources/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md))
- [WW 2010-09-27 — Introducing Red White and Blue (RWB) Stocks](../../raw/posts/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md)
