---
title: Backtest — the market-state timing overlay
type: methodology
updated: 2026-05-12
sources: []
---

# Backtest — does the GMI timing overlay beat buy-and-hold QQQ?

**The rule (pre-stated, zero fitted parameters):** be long QQQ when the reconstructed [GMI](gmi.md) has been >= 4 for two consecutive days; sit in cash when it has been <= 3 for two consecutive days. Signals on the close of day D, executed at the next day's open (modelled as a 1-day lag, close-to-close). Cost: 5 bps per round trip; no tax (an IRA). Period: 2007-01-01-2026-05-12. Benchmark: buy-and-hold QQQ. **Verdict criteria, fixed in advance:** "adds value" iff the default beats B&H QQQ on Sharpe *and* has <= 0.7x its max drawdown *and* the conclusion is robust across the variant grid; "marginal" if it cuts drawdown at a Sharpe/CAGR cost; "drag" if it underperforms on Sharpe and doesn't cut drawdown. (Caveat: the reconstructed GMI reads optimistic in declines -- ~78% GREEN/RED agreement with his reported GMI -- so this likely *understates* how defensive he actually was; see the breadth-data design spec.)

## Headline result

- **Strategy:** CAGR 7.5% · maxDD -19.3% · Sharpe 0.67 · Sortino 0.67 · Calmar 0.39 · in-mkt 59% · 133 trades · win 21%
- **Buy-and-hold QQQ:** CAGR 16.4% · maxDD -53.4% · Sharpe 0.80 · Sortino 1.03 · Calmar 0.31
- **Buy-and-hold SPY:** CAGR 10.9% · maxDD -55.2% · Sharpe 0.63 · Sortino 0.76 · Calmar 0.20
- **Plain 'QQQ > rising 30-week SMA' filter:** CAGR 11.1% · maxDD -25.2% · Sharpe 0.77 · Sortino 0.85 · Calmar 0.44 · in-mkt 74% · 28 trades · win 30%

### Verdict: **marginal — cuts drawdown (max-DD 19% vs 53%) but at a Sharpe/CAGR cost (Sharpe 0.67 vs 0.80); a stomach-vs-money trade**


![equity curve](https://litter.catbox.moe/v89qxb.png)

*(Strategy vs buy-and-hold QQQ vs SPY, log scale, RED periods shaded -- https://litter.catbox.moe/v89qxb.png)*


## Robustness grid

Each row varies one dimension vs the default. **Picking the best-looking variant after the fact would be data snooping** -- the headline is the default, full-period, no tuning.

| variant | result |
|---|---|
| **default (GMI>=4, 2/2 confirm, 5 bps)** | CAGR 7.5% · maxDD -19.3% · Sharpe 0.67 · Sortino 0.67 · Calmar 0.39 · in-mkt 59% · 133 trades · win 21% |
| GMI>=3 | CAGR 10.4% · maxDD -28.0% · Sharpe 0.79 · Sortino 0.89 · Calmar 0.37 · in-mkt 70% · 113 trades · win 24% |
| GMI>=6 | CAGR -0.6% · maxDD -20.5% · Sharpe -0.11 · Sortino -0.05 · Calmar -0.03 · in-mkt 12% · 103 trades · win 22% |
| confirm 0/0 | CAGR 6.9% · maxDD -23.4% · Sharpe 0.63 · Sortino 0.63 · Calmar 0.29 · in-mkt 59% · 251 trades · win 16% |
| confirm 5/5 | CAGR 7.7% · maxDD -26.7% · Sharpe 0.65 · Sortino 0.65 · Calmar 0.29 · in-mkt 61% · 70 trades · win 26% |
| confirm 2/1 | CAGR 6.7% · maxDD -17.8% · Sharpe 0.65 · Sortino 0.62 · Calmar 0.38 · in-mkt 54% · 187 trades · win 19% |
| +Stage-2 | CAGR 5.5% · maxDD -18.0% · Sharpe 0.55 · Sortino 0.51 · Calmar 0.30 · in-mkt 53% · 119 trades · win 21% |
| +QQQ-short-term-up | CAGR 8.0% · maxDD -19.3% · Sharpe 0.72 · Sortino 0.72 · Calmar 0.41 · in-mkt 57% · 132 trades · win 22% |
| +Stage-2 +ST-up | CAGR 6.1% · maxDD -16.1% · Sharpe 0.62 · Sortino 0.57 · Calmar 0.38 · in-mkt 51% · 117 trades · win 20% |
| reported GMI | CAGR 7.8% · maxDD -30.7% · Sharpe 0.62 · Sortino 0.63 · Calmar 0.25 · in-mkt 61% · 136 trades · win 25% |
| RED->SQQQ | CAGR -31.3% · maxDD -99.8% · Sharpe -0.46 · Sortino -0.55 · Calmar -0.31 · in-mkt 61% · 112 trades · win 28% |
| GREEN->TQQQ | CAGR 19.1% · maxDD -49.1% · Sharpe 0.68 · Sortino 0.68 · Calmar 0.39 · in-mkt 61% · 112 trades · win 20% |
| cost 20bps | CAGR 5.3% · maxDD -21.3% · Sharpe 0.49 · Sortino 0.50 · Calmar 0.25 · in-mkt 59% · 133 trades · win 20% |
| cost 0bps | CAGR 8.2% · maxDD -18.6% · Sharpe 0.72 · Sortino 0.72 · Calmar 0.44 · in-mkt 59% · 133 trades · win 21% |


## When did it help / hurt? (rolling 5-year strategy-CAGR minus QQQ-CAGR)

| 5y ending | excess CAGR |
|---|---|
| 2012-01-03 | -1.0% |
| 2012-07-03 | -0.2% |
| 2013-01-04 | -1.4% |
| 2013-07-08 | -5.9% |
| 2014-01-06 | -15.9% |
| 2014-07-08 | -15.6% |
| 2015-01-06 | -12.8% |
| 2015-07-08 | -18.1% |
| 2016-01-06 | -15.0% |
| 2016-07-07 | -13.1% |
| 2017-01-05 | -12.7% |
| 2017-07-07 | -13.5% |
| 2018-01-05 | -14.1% |
| 2018-07-09 | -16.3% |
| 2019-01-08 | -12.1% |
| 2019-07-10 | -10.5% |
| 2020-01-08 | -10.5% |
| 2020-07-09 | -8.5% |
| 2021-01-07 | -9.4% |
| 2021-07-09 | -12.2% |
| 2022-01-06 | -13.9% |
| 2022-07-11 | -6.1% |
| 2023-01-09 | -3.9% |
| 2023-07-12 | -5.1% |
| 2024-01-10 | -8.7% |
| 2024-07-12 | -9.0% |
| 2025-01-13 | -11.5% |
| 2025-07-16 | -10.4% |
| 2026-01-14 | -10.5% |


## Limitations

- The reconstructed GMI reads optimistic in declines (survivorship bias in the breadth universe) -- so the strategy here is *less* defensive than Dr. Wish actually was; a faithful version would cut drawdown more (and give back more on whipsaws). - 2007-start (the breadth reconstruction is thin before then). - 5-bps cost / no slippage beyond that / no tax. - This is the *timing* layer only -- it does **not** test his GLB/WGB stock-selection signal (a separate sub-project).

## See also

- [General Market Index (GMI)](gmi.md) · [Moving-average rules](moving-average-rules.md) · [QQQ Short-Term Timing](qqq-short-term-timing.md) · [Trend-flip log](../history/trend-flip-log.md)

## Sources

_None -- this page is a generated backtest report; the rules it tests are documented (and cited) on the linked methodology pages._
