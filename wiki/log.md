# Wiki log

Append-only, chronological. Every entry: `## [YYYY-MM-DD] <ingest|query|lint|note> | <title>`.
This is the resume state — `grep "^## \[" wiki/log.md | tail` shows recent activity.

## [2026-05-11] note | wiki bootstrapped

Created the `wiki/` skeleton (`index.md`, `log.md`, `overview.md`, 8 methodology
stubs, 3 playbook stubs, 2 history stubs, `_templates/`) and the `CLAUDE.md`
schema. No posts ingested yet — `raw/posts.jsonl` has ~4,655 rows, all
`ingested == false`. Next: Plan 2.5 (timeline parser), then Plan 3 (the Ingest loop).

## [2026-05-11] ingest | 2005-04-23 Let's Talk Strategy — tier=teaching; touched: methodology/risk-and-cash.md, methodology/moving-average-rules.md, methodology/stock-selection.md, methodology/glossary.md, history/timeline.md, sources/2005-04-23-lets-talk-strategy.md

## [2026-05-11] ingest | 2005-04-30 My Trading Strategy, Part II — tier=teaching; touched: methodology/stock-selection.md, methodology/risk-and-cash.md, methodology/green-line-breakouts.md, history/timeline.md, sources/2005-04-30-my-trading-strategy-part-ii.md

## [2026-05-11] ingest | 2005-06-05 GMI back to +5; on moving averages — tier=teaching; touched: methodology/moving-average-rules.md, methodology/gmi.md, methodology/qqq-short-term-timing.md, methodology/stock-selection.md, sources/2005-06-05-gmi-back-to-5-some-potential-winners-on-moving-averages.md

## [2026-05-11] ingest | 2005-07-17 GMI since inception; introducing the WPM — tier=teaching; touched: methodology/moving-average-rules.md, methodology/gmi.md, methodology/risk-and-cash.md, methodology/glossary.md, history/timeline.md, sources/2005-07-17-gmi-since-inception-introducing-the-wpm-on-analyst-earnings-estimates-ibd-100-rockets.md

## [2026-05-11] ingest | 2010-09-27 Introducing Red White and Blue (RWB) Stocks — tier=teaching; touched: methodology/stock-selection.md, methodology/moving-average-rules.md, methodology/t2108.md, methodology/gmi.md, methodology/glossary.md, history/timeline.md, sources/2010-09-27-introducing-red-white-and-blue-rwb-stocks-the-pattern-of-rockets.md

## [2026-05-11] ingest | 2011-03-07 Introducing the GMI2 — tier=teaching; touched: methodology/gmi.md, methodology/t2108.md, methodology/qqq-short-term-timing.md, history/timeline.md, sources/2011-03-07-introducing-the-gmi2-tc2000-com-ibd50-stock-performance-put-options-on-lulu.md

## [2026-05-11] ingest | 2012-07-23 Stage analysis and green line charts — tier=teaching; touched: methodology/green-line-breakouts.md, methodology/moving-average-rules.md, methodology/gmi.md, methodology/risk-and-cash.md, methodology/glossary.md, history/timeline.md, sources/2012-07-23-24th-day-of-qqq-short-term-up-trend-stage-analysis-and-green-line-charts.md

## [2026-05-11] ingest | 2014-08-03 GMI Successful 10-Day New High Indicator; T2108; AAPL — tier=teaching; touched: methodology/gmi.md, methodology/t2108.md, methodology/moving-average-rules.md, methodology/qqq-short-term-timing.md, methodology/risk-and-cash.md, methodology/glossary.md, sources/2014-08-03-gmi-successful-10-day-new-high-indicator-predicted-current-decline-t2108-indicator-aapl.md

## [2026-05-11] note | first ingest batch — pages now live: methodology/gmi.md (solid: 6 components, GMI2 evolution, long/defensive thresholds, Successful-10-Day refinement), methodology/green-line-breakouts.md (solid: definition, monthly chart, 3-month rule, GLB trigger), methodology/moving-average-rules.md (solid: 3 rules, 30-week, 10-week, 30-day, Stage 2, RWB reference), methodology/t2108.md (solid: definition, 80%/10% thresholds, asymmetry), methodology/stock-selection.md (solid: rocket metaphor, RWB, $80+ preference, GLB entry), methodology/risk-and-cash.md (solid: 70% correlation, GMI≤3 rule, 30-week exit, 2000/2003 exits, SQQQ tactics), methodology/qqq-short-term-timing.md (good: day-count format, down-trend statistics; flip rule undisclosed), methodology/glossary.md (comprehensive: 16 terms), history/timeline.md (2005–2014 covered), overview.md (fully replaced); still stubs: playbooks/market-state.md, playbooks/buying-glb.md, playbooks/exits.md, history/track-record.md; ww lint: OK — 0 errors, 8 warnings (source pages are orphans — warnings only); pytest: 46 passed.

## [2026-05-11] ingest | 2017-12-17 A strategy for deciding when to sell stocks; GDS, NVDA — tier=teaching; touched: methodology/stock-selection.md, playbooks/exits.md, methodology/moving-average-rules.md, methodology/green-line-breakouts.md, methodology/glossary.md, history/timeline.md, sources/2017-12-17-a-strategy-for-decidng-when-to-sell-stocks-gds-nvda.md

## [2026-05-11] ingest | 2010-03-15 Jim Cramer on stop loss orders; how I trade the 3X ETFs — tier=teaching; touched: methodology/risk-and-cash.md, sources/2010-03-15-jim-cramer-on-stop-loss-orders-terribly-wrong-again-kci-soars-how-i-trade-the-3x-etfs.md

## [2026-05-11] ingest | 2009-03-08 How I use put options as investment insurance — tier=teaching; touched: methodology/risk-and-cash.md, playbooks/exits.md, history/timeline.md, sources/2009-03-08-how-i-use-put-options-as-investment-insurance.md

## [2026-05-11] ingest | 2010-04-19 How I buy AAPL for 12% down without using margin — tier=teaching; touched: methodology/risk-and-cash.md, methodology/glossary.md, sources/2010-04-19-how-i-buy-aapl-for-12-down-without-using-margin.md

## [2026-05-11] ingest | 2017-03-19 How I use daily RWB charts to size up the market and individual stocks — tier=teaching; touched: methodology/moving-average-rules.md, methodology/stock-selection.md, methodology/glossary.md, history/timeline.md, sources/2017-03-19-how-i-use-daily-rwb-charts-to-size-up-the-market-and-individual-stocks-run-my-new-scan.md

## [2026-05-11] ingest | 2010-02-22 How to use IBD 100 and New America stocks to find rocket stocks — tier=teaching; touched: methodology/stock-selection.md, methodology/green-line-breakouts.md, history/timeline.md, sources/2010-02-22-how-to-use-ibd-100-and-new-america-stocks-and-tc2007-to-find-potential-rocket-stocks-market-rally-begun.md

## [2026-05-11] ingest | 2012-04-30 How I find the next AAPL growth stock; new GMI buy signal — tier=teaching; touched: methodology/gmi.md, methodology/stock-selection.md, history/timeline.md, sources/2012-04-30-how-to-find-the-next-aapl-growth-stock-new-gmi-buy-signal-ibd50-out-performs-again.md

## [2026-05-11] ingest | 2005-10-09 Nicolas Darvas trading techniques require markets at all-time peaks — tier=teaching; touched: methodology/green-line-breakouts.md, history/timeline.md, sources/2005-10-09-nicolas-darvas-trading-techniques-require-markets-at-all-time-peaks.md

## [2026-05-11] ingest | 2023-06-19 How I compute new US highs and lows; 11/2021 exit — tier=teaching; touched: methodology/gmi.md, history/timeline.md, history/track-record.md, sources/2023-06-19-blog-post-here-is-an-explanation-of-how-i-compute-new-us-highs-and-lows-each-day-and-used-it-to-exit-in-11-20.md

## [2026-05-11] ingest | 2024-05-27 ANF is an example of how I analyze a stock's trend using my weekly green bar indicator — tier=trade_example; touched: methodology/moving-average-rules.md, methodology/stock-selection.md, history/timeline.md, sources/2024-05-27-blog-post-day-15-of-qqq-short-term-up-trend-anf-is-an-example-of-how-i-analyze-a-stocks-trend-using-my-weekly.md

## [2026-05-11] note | second ingest batch complete — 10 posts ingested (IDs: 10631, 2174, 1285, 2194, 8823, 2157, 3535, 715, 26083, 28144); all 3 playbook stubs fully populated (exits.md, buying-glb.md, market-state.md); history/track-record.md fully populated; 10 new source-summary pages created; all batch-1 and batch-2 source summary pages linked from methodology/history/playbook Sources blocks (orphan-prevention housekeeping); CLAUDE.md §3 point 4 updated with summary-link convention; total ingested ~18 posts.
