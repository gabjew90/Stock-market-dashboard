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

## [2026-05-11] ingest | 2018-11-25 I'm back — daily BWR pattern for QQQ, weekly RWB pattern gone — tier=teaching; touched: methodology/moving-average-rules.md, methodology/risk-and-cash.md, methodology/t2108.md, methodology/glossary.md, history/timeline.md, sources/2018-11-25-im-back-daily-bwr-pattern-for-qqq-weekly-rwb-pattern-gone-content-to-be-on-sidelines.md

## [2026-05-11] ingest | 2021-02-28 TWTR to take off? — tier=trade_example; touched: methodology/green-line-breakouts.md, methodology/moving-average-rules.md, history/timeline.md, sources/2021-02-28-blog-post-twtr-to-take-off-day-20-of-qqq-short-term-up-trend-10-year-base-glb.md

## [2026-05-11] ingest | 2020-12-27 Buying IPOs with Green Line Breakouts (GLB) and a weekly green bar (WGB) signal — tier=teaching; touched: methodology/green-line-breakouts.md, methodology/moving-average-rules.md, methodology/glossary.md, history/timeline.md, sources/2020-12-27-blog-post-buying-ipos-with-green-line-break-outs-glb-and-a-weekly-green-bar-wgb-signal-pgny-tsla.md

## [2026-05-11] ingest | 2008-10-06 GMI=0, GMI-R=0 — current financial mess — tier=teaching; touched: methodology/risk-and-cash.md, methodology/t2108.md, methodology/gmi.md, history/timeline.md, sources/2008-10-06-gmi-0-gmi-r-0-current-financial-mess-and-why-i-got-out-of-my-pension-plan-in-june.md

## [2026-05-11] ingest | 2014-10-13 11th day of QQQ short-term down-trend — tier=teaching; touched: methodology/qqq-short-term-timing.md, methodology/moving-average-rules.md, methodology/t2108.md, methodology/risk-and-cash.md, history/timeline.md, sources/2014-10-13-11th-day-of-qqq-short-term-down-trend-how-long-will-this-market-decline-last.md

## [2026-05-11] ingest | 2025-03-30 Day 24 of QQQ short-term down-trend; IWM looks like Stage 4 — tier=teaching; touched: methodology/moving-average-rules.md, methodology/risk-and-cash.md, methodology/qqq-short-term-timing.md, history/timeline.md, sources/2025-03-30-blog-post-day-24-of-qqq-short-term-down-trend-iwm-looks-like-it-is-at-the-beginning-of-a-stage-4-down-trend-s.md

## [2026-05-11] ingest | 2011-07-25 My strategy for trading stocks that will advance $25 per share in a month — tier=teaching; touched: methodology/stock-selection.md, methodology/glossary.md, history/timeline.md, sources/2011-07-25-my-strategy-for-trading-stocks-that-will-advance-25-per-share-in-a-month.md

## [2026-05-11] ingest | 2021-06-13 TraderLion conference; black dot signals; GMI=6 — tier=teaching; touched: methodology/stock-selection.md, methodology/qqq-short-term-timing.md, methodology/glossary.md, history/timeline.md, sources/2021-06-13-follow-on-to-traderlion-conference-this-wednesdays-long-island-talk-examples-of-black-dot-signals-gmi6-of-6.md

## [2026-05-11] ingest | 2016-01-10 All world stock markets entering BWR down-trends — tier=teaching; touched: methodology/moving-average-rules.md, methodology/t2108.md, methodology/risk-and-cash.md, history/timeline.md, sources/2016-01-10-all-world-stock-markets-entering-bwr-down-trends-a-very-important-tool-for-staying-on-the-right-side-of-the-market.md

## [2026-05-11] ingest | 2009-06-14 How my GMI kept me and my 401k out of the bear market — tier=teaching; touched: methodology/gmi.md, methodology/risk-and-cash.md, methodology/moving-average-rules.md, history/timeline.md, sources/2009-06-14-how-my-general-market-indicator-gmi-kept-me-and-my-401k-out-of-the-bear-market.md

## [2026-05-11] note | third ingest batch complete — 10 posts ingested (IDs: 12676, 20321, 19913, 71, 5216, 29553, 3032, 21145, 6172, 1851); pages extended: methodology/moving-average-rules.md (Stage 1/2/3/4 full definitions, BWR precision, WGB TC2000 formula, WGB trailing stop rule), methodology/green-line-breakouts.md (IPO GLB mechanics, mental stop, WGB second-chance entry, closing-price confirmation), methodology/t2108.md (historical extreme lows table 1987–2025), methodology/glossary.md (black dot, DITM, Stage 1/3/4 entries, WGB formula), methodology/stock-selection.md ($80+ empirical backing, DITM mechanics, black dot signal), methodology/risk-and-cash.md (2008 and 2025 crisis case studies, TWM), methodology/qqq-short-term-timing.md (2 new sources), history/timeline.md (10 new chronological sections 2008–2025); total ingested ~28 posts.

## [2026-05-11] ingest | bulk-tier — 4460 daily_update + 18 meta posts (no summary pages; daily updates feed raw/timeline.parquet; ~149 long_form posts left for future teaching-ingest passes); timeline rebuilt: 4460 rows 2005-04-17..2026-05-11 (1353 high-confidence, 3107 flagged)

## [2026-05-11] ingest | 2018-05-20 Green line breakout (GLB) explained; GMI remains Green — tier=teaching; touched: methodology/green-line-breakouts.md (already-doubled attribute, strict immediate-sell, re-entry, pyramiding-to-30wk hold, GLB Tracker), playbooks/buying-glb.md (exit rules section added), sources/2018-05-20-green-line-breakout-glb-explained-gmi-remains-green.md

## [2026-05-11] ingest | 2017-03-26 Market rally over? My refined strategy for timing exits and entries — tier=teaching; touched: methodology/moving-average-rules.md (TLC definition, BLC, Bollinger Band/low-stochastics buy scan, mental-stop guidance), sources/2017-03-26-market-rally-over-my-refined-strategy-for-timing-exits-and-entries-recent-glb-lite.md

## [2026-05-11] ingest | 2015-02-01 Red, White and Blue (RWB): the rocket pattern — tier=teaching; touched: methodology/moving-average-rules.md (Guppy GMMA attribution, confirmed EMA periods, red-line convergence caution, code Caveat updated to confirmed), sources/2015-02-01-red-white-and-blue-rwb-the-rocket-pattern-and-gldaapl-and-the-dow-30-nyse-bear.md

## [2026-05-11] note | wiki v1 complete — Plans 1-5 done; methodology/playbook/history pages all populated & cited; literate indicator code + GMI/T2108 + ww compute; ww search/ww index; corpus fully tiered; ww lint clean; 112 tests. Next: more long_form ingest passes + Plan 6 (backtest).
