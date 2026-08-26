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

## [2026-05-12] ingest | 2016-06-05 Introducing BOS alerts; GMI at 6; RTN — tier=teaching; touched: methodology/stock-selection.md (BOS strategy section), methodology/glossary.md (BOS entry), history/timeline.md (June 2016 section), sources/2016-06-05-introducing-bos-alerts-for-my-tweets-gmi-at-6-of-6-a-dr-wish-favorite-post-bos-rtn.md

## [2026-05-12] ingest | 2016-07-24 How I buy rocket stocks bouncing off support; HII — tier=teaching; touched: methodology/stock-selection.md (BOS mechanics, Bollinger Band entry signal), methodology/glossary.md (Bollinger Band 15.2 entry), sources/2016-07-24-how-i-buy-rocket-stocks-bouncing-up-off-of-support-bos-an-example-hii.md

## [2026-05-12] ingest | 2017-04-02 Patience after a GLB; PNRA and FIZZ — tier=trade_example; touched: methodology/green-line-breakouts.md (Patience after a GLB section), history/timeline.md (April 2017 section), sources/2017-04-02-end-of-window-dressing-day-78-of-qqq-up-trend-turbulence-ahead-pnra-how-to-have-patience-after-a-glb-glb-fizz.md

## [2026-05-12] ingest | 2017-07-02 GLB the sine qua non of rocket stocks; SHOP SQ BABA Z FB BZUN — tier=teaching; touched: methodology/green-line-breakouts.md (Darvas no-exceptions, overhead supply, origin, six worked examples), history/timeline.md (July 2017 section), sources/2017-07-02-green-line-break-outs-glb-the-sine-qua-non-of-rocket-stocks-shop-sq-baba-z-fb-bzun.md

## [2026-05-12] ingest | 2017-09-04 BGNE example of stock purchase setup for new students — tier=teaching; touched: methodology/stock-selection.md (three-chart analysis chain), history/timeline.md (September 2017 section), sources/2017-09-04-bgne-example-of-a-stock-purchase-set-up-for-my-new-students-gmi-green.md

## [2026-05-12] ingest | 2018-01-15 Why I like RWB daily charts; HRI OLLI NKTR — tier=teaching; touched: methodology/moving-average-rules.md (daily RWB bounce scan section), history/timeline.md (January 2018 section), sources/2018-01-15-why-i-like-rwb-daily-charts-hri-olli-and-nktr.md

## [2026-05-12] ingest | 2018-01-21 Why buying stocks over $100 is more profitable — tier=teaching; touched: methodology/stock-selection.md ($100+ expanded with 85%/95% data and Wyckoff quote), history/timeline.md (January 2018 section), sources/2018-01-21-why-buying-stocks-over-100-is-more-profitable.md

## [2026-05-12] ingest | 2020-03-15 Livermore: Amputation without anaesthetics; COVID exit — tier=teaching; touched: methodology/risk-and-cash.md (2020 exit case study), history/track-record.md (February-March 2020 section), history/timeline.md (March 2020 section), sources/2020-03-15-livermore-amputation-without-anaesthetics-after-avoiding-the-2000-decline-i-began-this-blog-in-2006-to-help-p.md

## [2026-05-12] ingest | 2020-09-06 How I use Bollinger Bands; Nasdaq100 breadth foreshadowed decline — tier=teaching; touched: methodology/moving-average-rules.md (Bollinger Bands as timing overlay), methodology/glossary.md (Bollinger Band 15.2, green dot entries), history/timeline.md (September 2020 section), sources/2020-09-06-new-freshmen-class-and-possible-online-workshop-how-i-use-bollinger-bands-and-how-this-indicator-foreshadowed.md

## [2026-05-12] ingest | 2021-01-24 GLB origin (1960s); overhead supply; no hard stop — tier=teaching; touched: methodology/green-line-breakouts.md (GLB origin, overhead supply, no-hard-stop, IPO adjustment), history/timeline.md (January 2021 section), sources/2021-01-24-blog-post-in-the-60s-i-used-to-receive-a-book-containing-monthly-charts-of-stocks-i-noticed-that-stocks-that.md

## [2026-05-12] ingest | 2022-12-04 TC2000 gap-up scan; TMDX and TMUS — tier=teaching; touched: methodology/stock-selection.md (gap-up scan added), methodology/glossary.md (gap-up scan entry), history/timeline.md (December 2022 section), sources/2022-12-04-blog-post-day-15-of-qqq-short-term-up-trend-time-for-me-to-buy-see-my-tc2000-scan-for-finding-stocks-gapping.md

## [2026-05-12] note | fourth ingest batch complete — 11 posts ingested (IDs: 7174, 7421, 8969, 9412, 9790, 10797, 10830, 17604, 19055, 20101, 24853); pages extended: methodology/stock-selection.md (BOS strategy, three-chart chain, gap-up scan, $100+ 2018 data), methodology/green-line-breakouts.md (Darvas no-exceptions, overhead supply, GLB origin, no-hard-stop, patience-post-GLB), methodology/moving-average-rules.md (daily RWB bounce scan, Bollinger Band 15.2 overlay), methodology/risk-and-cash.md (2020 COVID exit), methodology/glossary.md (Bollinger Band 15.2, BOS, gap-up scan, green dot), history/timeline.md (8 new sections: June 2016, July/Sep/Jan 2017-18, Mar/Sep 2020, Jan 2021, Dec 2022), history/track-record.md (February-March 2020 COVID exit); 11 new source summary pages; total ingested ~45 teaching/trade_example posts.

## [2026-05-12] gap-hunt | gap (b) — QQQ short-term trend flip rule: RESOLVED — 2013-10-20 post retroactively applies "current techniques" to 1987 Dow chart; explicitly states 30-day MA curved down = short-term down-trend declaration. Best evidence from a single post. Updated methodology/qqq-short-term-timing.md from "undisclosed" to "well-evidenced: close above 30-day MA". Gap (a) GMI 3&4 exact rule: UNRESOLVED — 2005-04-26 post explicitly withholds specific indicators. Gap (c) GMI-R/GMI2 full component lists: UNRESOLVED — extras never disclosed. Gap (d) IBD thresholds: UNRESOLVED — no explicit minimums in any post scanned. Gap (e) RWB/BOS precision: ALREADY DOCUMENTED (Bollinger Band 15.2 confirmed as BOS trigger).

## [2026-05-12] ingest | 2013-10-20 TA vs 1987 crash; 30-day MA as short-term trend signal — tier=teaching; touched: methodology/qqq-short-term-timing.md (gap (b) resolved: 30-day MA rule evidenced), methodology/moving-average-rules.md (30-day MA as short-term index trend signal), history/timeline.md (October 2013 section), sources/2013-10-20-can-ta-protect-ourselves-from-a-1987-type-of-market-crash-speculative-bull-market-phase-beginning-tplm-green.md

## [2026-05-12] ingest | 2013-11-24 GMI-based strategy using 3X ETFs beats IBD 50 stocks — tier=teaching; touched: methodology/risk-and-cash.md (GMI buy signal + TQQQ default), history/timeline.md (November 2013 section), sources/2013-11-24-gmi-based-strategy-using-3x-etfs-beats-ibd-50-stocks.md

## [2026-05-12] ingest | 2022-04-17 QQQ/SPY below 10-week avg; GMI Red; WGB scan criteria — tier=teaching; touched: methodology/stock-selection.md (WGB scan criteria expanded + 3-tier trailing stop), history/timeline.md (April 2022 section), sources/2022-04-17-blog-post-qqq-and-spy-closed-back-below-their-10-week-averages-gmi-remains-red-cash-is-king-but-there-are-25.md

## [2026-05-12] ingest | 2021-01-18 Individual IBD/MS stocks outperformed TQQQ for first time — tier=teaching; touched: methodology/risk-and-cash.md (2021 exception note), history/timeline.md (January 2021 section), sources/2021-01-18-blog-post-for-the-first-time-many-individual-stocks-outperformed-just-holding-tqqq-during-a-qqq-short-term-up.md

## [2026-05-12] ingest | 2014-02-23 Covered call income on GLD; GLB examples — tier=teaching; touched: methodology/risk-and-cash.md (covered call income strategy), history/timeline.md (February 2014 section), sources/2014-02-23-9th-day-of-qqq-short-term-up-trend-gld-turning-up-writing-calls-on-gld-gmcr-qcor-irbt-green-line-break-outs.md

## [2026-05-12] ingest | 2012-06-18 1990s trading diary excerpt; GMI buy-signal trigger explicit — tier=teaching; touched: methodology/gmi.md (second citation for buy-signal trigger), history/timeline.md (June 2012 section), sources/2012-06-18-an-excerpt-from-my-trading-diary-from-the-90s-market-at-critical-juncture.md

## [2026-05-12] ingest | 2022-06-05 Day 37 of QQQ down-trend; ATH-only philosophy; GLB re-entry — tier=teaching; touched: methodology/green-line-breakouts.md (re-entry after failed GLB section), methodology/stock-selection.md (ATH-only philosophy + Darvas/Ryan doubler), history/timeline.md (June 2022 section), sources/2022-06-05-bog-post-day-37-of-qqq-short-term-down-trend-14-ibd-marketsmith-stocks-at-20-year-high-on-friday.md

## [2026-05-12] ingest | 2011-08-07 Crash coming? 3rd day of QQQ short-term down-trend — tier=teaching; touched: methodology/qqq-short-term-timing.md (2011 crash reference), history/timeline.md (August 2011 section), sources/2011-08-07-crash-coming-only-3rd-day-of-new-qqq-short-term-down-trend.md

## [2026-05-12] ingest | 2011-02-07 Nicolas Darvas on studying losses; RWB stock stop-loss — tier=teaching; touched: methodology/moving-average-rules.md (30-day MA stop on individual stocks), history/timeline.md (February 2011 section), sources/2011-02-07-nicolas-darvas-on-the-value-of-studying-ones-trading-losses-rwb-stocks-cost-rvbd.md

## [2026-05-12] ingest | 2010-07-06 Pension exit discipline; topping-pattern PCF scan — tier=teaching; touched: methodology/risk-and-cash.md (pension exit discipline + topping-pattern scan), history/timeline.md (July 2010 section), sources/2010-07-06-at-the-beginning-of-a-big-market-decline-my-next-worden-webinar.md

## [2026-05-12] ingest | 2005-12-03 Early GMI breadth details; per-stock short-term up-trend — tier=teaching; touched: methodology/moving-average-rules.md (per-stock short-term up-trend definition: 10d avg above rising 30d avg), history/timeline.md (December 2005 section), sources/2005-12-03-gmi-6-wpm-shows-a-little-dow-30-deterioration-correlation-of-some-indicators-with-s-mcd-break-out-jnj-sick.md

## [2026-05-12] note | fifth ingest batch complete — 11 posts ingested (IDs: 4531, 4626, 23248, 20048, 4813, 3627, 23549, 3048, 2774, 2295, 676); 1 gap resolved (gap (b): QQQ short-term trend flip = 30-day MA crossing on close; qqq-short-term-timing.md updated from "undisclosed" to "well-evidenced"); pages extended: methodology/qqq-short-term-timing.md (gap resolved), methodology/gmi.md (second citation for buy-signal trigger; typo fixed), methodology/risk-and-cash.md (pension exit, TQQQ default, 2021 exception, covered call note), methodology/stock-selection.md (WGB trailing stop tier, ATH-only philosophy, Darvas/Ryan doubler), methodology/green-line-breakouts.md (re-entry after failed GLB), methodology/moving-average-rules.md (per-stock short-term up-trend definition, 30-day MA stop on stocks, 30-day MA as index signal), history/timeline.md (11 new chronological sections: Dec 2005, Jul 2010, Feb 2011, Aug 2011, Jun 2012, Oct 2013, Nov 2013, Feb 2014, Jan 2021, Apr 2022, Jun 2022); 11 new source summary pages; total ingested ~56 teaching/trade_example posts.

## [2026-05-12] ingest | 2009-01-05 I'm up 1200% — tier=teaching; touched: methodology/risk-and-cash.md (capital conservation, 1200% track record), history/timeline.md (January 2009 section), history/track-record.md (1994–2009 section), sources/2009-01-05-im-up-1200-as-my-fellow-boomers-and-college-students-get-screwed-again-qqqq-in-17th-day-of-short-term-up-tren.md

## [2026-05-12] ingest | 2009-03-29 Is the bear market over? Guppy charts — tier=teaching; touched: methodology/moving-average-rules.md (Guppy weekly bear-bottom detector, trend hierarchy), history/timeline.md (March 2009 Guppy section), sources/2009-03-29-is-the-bear-market-over-check-out-my-guppy-charts.md

## [2026-05-12] ingest | 2010-05-09 Washington Worden seminar; Stage 2 pension rule — tier=teaching; touched: methodology/risk-and-cash.md (Stage 2 pension rule precision, 5-day confirmation), history/timeline.md (May 2010 section), sources/2010-05-09-great-washington-worden-seminar-market-in-short-term-down-trend-mainly-in-cash.md

## [2026-05-12] ingest | 2011-01-04 2010 ETF performance; TQQQ beats individual stocks — tier=teaching; touched: methodology/risk-and-cash.md (2010 performance data, Day-1 entry tactic), history/timeline.md (January 2011 section), sources/2011-01-04-2010-etf-performance-why-search-for-individual-stocks-when-one-can-just-ride-the-leveraged-etfs.md

## [2026-05-12] ingest | 2013-05-20 How to find a TSLA-like explosive stock; GLB workflow — tier=trade_example; touched: methodology/stock-selection.md (TSLA GLB workflow), methodology/green-line-breakouts.md (TC2000 alert workflow, TSLA re-test entry), history/timeline.md (May 2013 section), sources/2013-05-20-how-to-find-a-tsla-like-explosive-stock-before-its-huge-advance-more-green-line-break-outs.md

## [2026-05-12] ingest | 2013-06-09 2-for-1 method; TQQQ outperformance — tier=teaching; touched: methodology/risk-and-cash.md (2-for-1 method), history/timeline.md (June 2013 section), sources/2013-06-09-up-trend-intact-2-for-1-method-for-managing-stock-market-risk-gmi-based-system-to-trade-qld-leads-the-pack-ag.md

## [2026-05-12] ingest | 2014-04-27 Staged pension exit; GMI/QQQ divergence — tier=teaching; touched: methodology/risk-and-cash.md (staged pension exit protocol), history/timeline.md (April 2014 section), sources/2014-04-27-i-do-not-want-to-be-long-in-this-market.md

## [2026-05-12] ingest | 2014-09-28 Biotech scan; AGIO; 3:45 PM rule — tier=teaching; touched: methodology/stock-selection.md (biotech scan, news-catalyst integration, 3:45 PM rule), history/timeline.md (September 2014 section), sources/2014-09-28-this-market-is-not-out-of-the-woods-finding-bio-tech-stars-like-agio-and-vrtx.md

## [2026-05-12] ingest | 2016-10-02 O'Neil 1995 workshop diary; LMAT setup — tier=teaching; touched: methodology/stock-selection.md (O'Neil 1995 workshop: volume/RS over EPS), methodology/green-line-breakouts.md (TC2000 alert workflow, two-close GLB failure rule), history/timeline.md (October 1995/October 2016 section), sources/2016-10-02-my-trading-diary-entry-from-william-oneils-workshop-in-1995-a-set-up-for-buying-lmat-heia-cup-and-handle-brea.md

## [2026-05-12] ingest | 2016-11-20 Weekly 4wk/10wk hold discipline; NTES — tier=teaching; touched: methodology/moving-average-rules.md (4wk/10wk hold discipline, O'Neil weekly-chart-only), playbooks/exits.md (4wk/10wk exit ladder), history/timeline.md (November 2016 section), sources/2016-11-20-short-and-long-term-trends-now-up-on-using-weekly-charts-to-stay-in-a-growth-stock-ntes.md

## [2026-05-12] ingest | 2018-02-25 Rising interest rates; monthly RWB on bonds — tier=teaching; touched: methodology/moving-average-rules.md (monthly RWB on bond ETFs, Martin Zweig principle), history/timeline.md (February 2018 section), sources/2018-02-25-rising-interest-rates-suggest-market-to-form-top.md

## [2026-05-12] ingest | 2023-04-24 WING missed GLB; written GLB rules published — tier=teaching; touched: methodology/green-line-breakouts.md (TC2000 alert workflow, written GLB rules, Turtle Traders principle), playbooks/buying-glb.md (student checklist section added), history/timeline.md (April 2023 section), sources/2023-04-24-blog-post-day-26-of-qqq-short-term-up-trend-wing-flies-to-ath-how-i-missed-the-glb-true-confessions-and-see-m.md

## [2026-05-12] note | sixth ingest batch complete — 12 posts ingested (IDs: 9, 1502, 2210, 2707, 4254, 4285, 4948, 5182, 7776, 8062, 11033, 25696); topics: 1200% IRA track record, Guppy bear-bottom detector + trend hierarchy, Stage 2 pension rule precision, 2010 TQQQ year-in-review + Day-1 tactic, TSLA 5-step GLB workflow, 2-for-1 risk management, staged pension exit protocol, biotech scan + news catalyst, O'Neil 1995 workshop diary + LMAT GLB+BOS, 4wk/10wk weekly hold discipline, monthly RWB on bond ETFs + Martin Zweig, WING missed GLB + written rules; pages extended: methodology/risk-and-cash.md (2-for-1, staged exit, 2010 data, Day-1 tactic), methodology/moving-average-rules.md (Guppy bear-bottom, monthly bond ETF RWB, 4wk/10wk hold, Martin Zweig), methodology/stock-selection.md (TSLA workflow, biotech scan, O'Neil 1995 workshop), methodology/green-line-breakouts.md (TC2000 alert workflow, written GLB rules, Turtle Traders, WING), playbooks/exits.md (4wk/10wk exit ladder extended), playbooks/buying-glb.md (student checklist section), history/timeline.md (12 new chronological sections), history/track-record.md (1994–2009 1200% IRA section); 12 new source summary pages; total ingested ~68 teaching/trade_example posts.

## [2026-05-12] ingest | 2005-08-27 Weinstein Dow sell signal; bank shorts; SBUX submarine — tier=teaching; touched: methodology/moving-average-rules.md (Weinstein 30-week sell signal, 30-week curve-down), methodology/risk-and-cash.md (2005 case), history/timeline.md (August 2005 section), sources/2005-08-27-stan-weinstein-dow-sell-signal-gmi-1-sick-bank-stocks-sbux-in-the-drink.md

## [2026-05-12] ingest | 2005-11-13 First GMI track record chart; Cramer refutation; stock criteria — tier=teaching; touched: methodology/gmi.md (2005 GMI evolution), history/timeline.md (November 2005 section), sources/2005-11-13-gmi6-my-favorite-posts-gmi-as-a-trend-indicator-wpm-shows-all-indexes-strong-jim-cramer-on-charts-some-big-ea.md

## [2026-05-12] ingest | 2006-02-06 Wyckoff/Darvas noise isolation; GMI-S introduced — tier=teaching; touched: methodology/gmi.md (GMI-S 2006 evolution), history/timeline.md (February 2006 section), sources/2006-02-06-darvas-anticipated-gmi-4-gmi-s-31-ominous-market.md

## [2026-05-12] ingest | 2006-05-22 Submarine scan fully described; IBD-100 in down-trends — tier=teaching; touched: methodology/risk-and-cash.md (submarine scan 5 criteria, IBD amplification data), history/timeline.md (May 2006 section), sources/2006-05-22-gmi-0-ibd-100-stocks-decline-more-my-epiphany-on-discount-brokers-submarine-stocks.md

## [2026-05-12] ingest | 2009-02-23 Quantitative bear comparison: 2008 vs 1929/1973/1987 — tier=teaching; touched: history/timeline.md (February 2009 section), history/track-record.md (Feb 2009 projection entry), sources/2009-02-23-comparison-of-current-bear-to-bear-markets-of-1929-1973-74-1987-suggests-dow-3500-possible.md

## [2026-05-12] ingest | 2010-05-03 TC2007 submarine scan on former leaders; PWRD/NTES sector failure — tier=teaching; touched: history/timeline.md (May 2010 section), sources/2010-05-03-market-showing-serious-signs-of-weakness-surprising-tc2007-submarine-scan-results.md

## [2026-05-12] ingest | 2010-07-19 14x IRA; stochastic 10,4,4; QQQ 10wk/30wk down-trend rule — tier=teaching; touched: methodology/moving-average-rules.md (stochastic 10,4,4 section), history/timeline.md (July 2010 section), history/track-record.md (14x entry), sources/2010-07-19-major-indexes-remain-in-long-term-down-trends-in-cash-or-short.md

## [2026-05-12] ingest | 2011-04-04 IBD50 vs Nasdaq100/S&P500 comparison; 10-week bounce scan — tier=teaching; touched: methodology/stock-selection.md (IBD50 comparison, 10-week bounce scan), history/timeline.md (April 2011 section), sources/2011-04-04-ibd50-list-from-110-out-performs-nasdaq100-and-sp500-stocks.md

## [2026-05-12] ingest | 2017-01-29 David Ryan; ATH-past-40-days + lower BB scan; PLAY — tier=teaching; touched: methodology/stock-selection.md (ATH-past-40-days scan, David Ryan), methodology/green-line-breakouts.md (post-GLB pullback scan section), history/timeline.md (January 2017 section), sources/2017-01-29-on-david-ryan-and-my-new-tc2000-scan-for-glb-rockets-bouncing-off-up-of-support-play.md

## [2026-05-12] ingest | 2018-03-25 GMI Red Q1 2018; put/call contrarian; pension trigger — tier=teaching; touched: methodology/risk-and-cash.md (2018 case study, put/call contrarian rule), methodology/t2108.md (below-10% action), history/timeline.md (March 2018 section), sources/2018-03-25-time-for-cash-gmi1-of-6-turns-red.md

## [2026-05-12] ingest | 2022-05-01 T2108 monthly; BWR onset vs 2008; index GLB tops — tier=teaching; touched: methodology/t2108.md (monthly context, SPY accumulation tactic), methodology/risk-and-cash.md (2022 case study), methodology/green-line-breakouts.md (index ETF GLB section), history/timeline.md (May 2022 section), sources/2022-05-01-blog-post-based-on-my-analysis-of-the-market-it-is-nowhere-oversold-enough-to-be-near-a-bottom-here-is-the-ev.md

## [2026-05-12] ingest | 2016-09-05 DW GLB worked example; GLB tracker table; weekly scan criteria — tier=teaching; touched: methodology/green-line-breakouts.md (weekly scan criteria, GLB tracker table, relative strength during corrections), history/timeline.md (September 2016 section), sources/2016-09-05-dw-a-successful-green-line-break-out-updated-glb-tracker-table-all-gmi-components-positive.md

## [2026-05-12] ingest | 2019-04-07 IPO GLB; IIPR; QQQ trend duration statistics — tier=teaching; touched: methodology/qqq-short-term-timing.md (down-trend duration stats updated through 2019), methodology/green-line-breakouts.md (IPO GLB Livermore citation, green dot secondary entry), history/timeline.md (April 2019 section), sources/2019-04-07-trading-ipos-with-a-glb-and-a-green-dot-signal-iipr-qqq-short-term-up-trend-is-in-61st-day.md

## [2026-05-12] ingest | 2020-07-19 Bounce-off-support strategy; green dot signal + stop below bounce low — tier=teaching; touched: methodology/stock-selection.md (bounce-off-support section, green dot mechanics), history/timeline.md (July 2020 section), sources/2020-07-19-blog-post-my-bounce-off-of-support-strategy-some-possible-examples-ddog-etsy-net-band-plmr-domo-cien-ping-adb.md

## [2026-05-12] ingest | 2020-09-27 Monitoring GLBs in corrections; weekly chart hold rule — tier=teaching; touched: methodology/green-line-breakouts.md (weekly chart management during corrections), history/timeline.md (September 2020 section), sources/2020-09-27-this-week-will-determine-if-tech-down-trend-will-continue-monitoring-glbs-to-find-leaders-during-a-correction.md

## [2026-05-12] ingest | 2023-02-15 CRDO failed GLB; gap-down stop lesson — tier=teaching; touched: methodology/green-line-breakouts.md (CRDO failure case; gap-down risk), history/timeline.md (February 2023 section), sources/2023-02-15-blog-post-day-24-of-qqq-short-term-up-trend-when-technical-analysis-fails-crdo-my-confession.md

## [2026-05-12] ingest | 2023-11-26 Canonical GLB re-statement; PGR worked example — tier=teaching; touched: methodology/green-line-breakouts.md (canonical re-statement, PGR), history/timeline.md (November 2023 section), sources/2023-11-26-very-important-blog-post-explaining-glbs-day-15-of-qqq-short-term-up-trend-123-us-new-highs-and-2-lows-43-at.md

## [2026-05-12] ingest | 2024-06-16 x8/x21/30-day daily alignment bounce entry introduced — tier=teaching; touched: methodology/stock-selection.md (x8/x21/30 section), methodology/moving-average-rules.md (x8/x21/30 in recent practice), methodology/glossary.md (x8/x21/30 term), history/timeline.md (June 2024 section), sources/2024-06-16-blog-post-day-29-of-qqq-short-term-up-trend-introducing-the-x8-x21-30-day-set-up-examplescost-anf-nvda-cvlt.md

## [2026-05-12] ingest | 2025-04-06 Day 29 of QQQ down-trend; T2108=7%; 10wk/30wk cross; tariff decline — tier=teaching; touched: methodology/t2108.md (T2108=7% April 2025 corroboration), methodology/moving-average-rules.md (10wk/30wk cross-down April 2025), methodology/risk-and-cash.md (2025 April tariff entry), history/timeline.md (April 2025 section), sources/2025-04-06-blog-post-day-29-of-qqq-short-term-down-trend-t2108-declines-to-7-where-bottoms-tend-to-occur-we-can-time-the.md

## [2026-05-12] ingest | 2025-05-22 Blue dot of happiness full scan formula; Boston IBD Meetup — tier=teaching; touched: methodology/stock-selection.md (blue dot scan section), methodology/glossary.md (blue dot of happiness term), history/timeline.md (May 2025 section), sources/2025-05-22-blog-post-day-20-of-qqq-short-term-up-trend-thank-you-for-attending-my-presentation-to-the-boston-ibd-meetup.md

## [2026-05-12] ingest | 2025-06-29 GLB on mutual funds; Fidelity Contrafund; pension re-entry — tier=teaching; touched: methodology/green-line-breakouts.md (GLB on mutual funds), methodology/moving-average-rules.md (10wk/30wk crossover pension), methodology/risk-and-cash.md (2025 re-entry June entry), history/timeline.md (June 2025 section), sources/2025-06-29-blog-post-day-44-of-qqq-short-term-up-trend-ta-works-also-for-mutual-funds-see-glb-last-week-in-fidelity-cont.md

## [2026-05-12] ingest | 2025-08-10 Day 73 of QQQ up-trend; stop losses sine qua non; blue dot re-entry — tier=teaching; touched: methodology/green-line-breakouts.md (stop losses sine qua non), history/timeline.md (August 2025 section), sources/2025-08-10-blog-post-day-73-of-qqq-short-term-up-trend-shaken-out-but-back-in-blue-dot-of-happiness-signal-held-see-dail.md

## [2026-05-12] ingest | 2025-10-23 4-week weekly bounce strategy; SPY GLB June 2025 — tier=teaching; touched: methodology/moving-average-rules.md (4wk weekly bounce entry), methodology/green-line-breakouts.md (SPY GLB 2025), history/timeline.md (October 2025 section), sources/2025-10-23-blog-post-day-43-of-qqq-short-term-up-trend-come-back-at-halloween-barring-bad-inflation-news-friday-my-indic.md

## [2026-05-12] ingest | 2026-02-16 Day 8 of QQQ down-trend; QQQ at green line + 30wk; Stage 3/4 warning — tier=teaching; touched: methodology/risk-and-cash.md (2026 February-March entry), methodology/moving-average-rules.md (4wk below 10wk warning), history/timeline.md (February 2026 section), sources/2026-02-16-blog-day-8-of-qqq-short-term-down-trend-utilities-had-most-aths-13-see-list-followed-by-oilgas-10-rotation-aw.md

## [2026-05-12] ingest | 2026-03-15 Day 27 of QQQ down-trend; GMI=0 Red; Stage 4 confirmed — tier=teaching; touched: methodology/t2108.md (T2108=23% during GMI=0), methodology/risk-and-cash.md (2026 February-March entry), history/timeline.md (March 2026 section), sources/2026-03-15-blog-post-day-27-of-qqq-short-term-down-trend-gmi-0-and-red-more-new-us-52-week-lows-than-highs-this-weekly-c.md

## [2026-05-12] ingest | 2026-05-10 Day 22 of QQQ up-trend; 4wk>10wk>30wk confirmed; 5-day EMA post-GLB exit — tier=teaching; touched: methodology/green-line-breakouts.md (5-day EMA exit), methodology/moving-average-rules.md (4wk>10wk>30wk 2026), history/timeline.md (May 2026 section), sources/2026-05-10-bog-post-day-22-of-qqq-short-term-up-trend-qqq-10-wk-avg-now-closes-week-above-30-wk-avg-gmigreen-glb-breakou.md

## [2026-05-12] BATCH 8 COMPLETE — recent-weighted ingest: 15 posts (3 from 2026, 5 from 2025, 1 from 2024, 2 from 2023, 2 from 2020, 1 from 2019, 1 from 2016). All re-tiered to teaching. Methodology pages updated: green-line-breakouts.md, moving-average-rules.md, t2108.md, risk-and-cash.md, stock-selection.md, qqq-short-term-timing.md, glossary.md. New glossary terms: blue dot of happiness, x8/x21/30-day setup. History/timeline.md: 15 new sections added (September 2016 through May 2026). wiki/index.md: 15 new Sources entries + description updates. wiki/log.md: 16 entries (15 ingest + 1 batch summary). Total batch 8 source pages created: 15.

## [2026-05-12] note | seventh ingest batch complete — 11 posts ingested (IDs: 747, 690, 636, 577, 1144, 2204, 2324, 2881, 8525, 11177, 23331); topics: Weinstein 30-week sell signal (first 2005 instance), first GMI historical track-record chart, Wyckoff/Darvas noise isolation + GMI-S, submarine scan fully described (5 criteria), bear market comparison 2009 (Dow 3,500 projection), TC2007 submarine scan on former leaders, 14× IRA update + stochastic 10,4,4, IBD50 vs indexes quantitative comparison, David Ryan + ATH-past-40-days scan, GMI Red Q1 2018 + put/call contrarian, T2108 monthly + 2022 BWR onset + index GLB; pages extended: methodology/moving-average-rules.md (Weinstein quote, stochastic 10,4,4 section), methodology/risk-and-cash.md (submarine scan 5 criteria, IBD amplification, 2018+2022 case studies, put/call contrarian), methodology/t2108.md (2022 SPY accumulation, monthly chart context, 2018 contrast), methodology/gmi.md (GMI-S evolution entry), methodology/stock-selection.md (IBD50 comparison 2011, ATH-past-40-days scan), methodology/green-line-breakouts.md (post-GLB pullback scan, index ETF GLB), methodology/glossary.md (4 new terms: ATH-past-40-days scan, put/call ratio, stochastic 10,4,4, submarine scan), history/timeline.md (11 new chronological sections: Aug 2005, Nov 2005, Feb 2006, May 2006, Feb 2009, May 2010, Jul 2010, Apr 2011, Jan 2017, Mar 2018, May 2022), history/track-record.md (14× IRA July 2010 entry, Feb 2009 bear projection entry); 11 new source summary pages; total ingested ~79 teaching/trade_example posts.

## [2026-05-12] note | added history/trend-flip-log.md — ST/LT flip framing + 60 short-term flips (2007–2026) + 12 long-term-stage transitions + detailed entries (2007–2008 GFC, 2011, 2018 Q4, 2020 COVID, 2022 bear, April-2025 tariff decline, April-2026 Iran-war period); 3 head-fake examples; index.md + overview.md + timeline.md + track-record.md updated

## [2026-07-02] note | code-review fixes: gmi.py point-in-time bug (components 3/4/5 now truncate prices at `date`; validation stats in methodology/gmi.md flagged stale pending a `ww breadth validate` re-run), dashboard Day-N count aligned to the documented closing-cross rule (was shifted +1 session), CI cache now saves only on success + n_nyse floor gate. Touched: methodology/gmi.md, src/ww/indicators/gmi.py, scripts/build_market_regime.py, both workflows.

## [2026-07-02] lint | fixed backtest-timing-overlay.md — equity-curve image path was resolving to a nonexistent wiki/methodology/assets/ (now ../../assets/backtest/equity_curve.png) and the page was missing from index.md (added under Methodology); clears the CI wiki-lint failure on main

## [2026-07-02] note | QC of GMI/T2108/stage logic — stage determination consolidated into src/ww/indicators/ma_stages.py (weinstein_stage_series): Stage 2 now requires the weekly 10wk>30wk cross (per WW 2026-05-10 / the 2010-05-09 pension rule; the April-2026 recovery had been labelled Stage 2 three weeks early), and the slope test gained a 2-week curl-down guard (long-window slope misses fresh tops). Historical impact: 2.9% of days since 2010 relabelled, all premature-Stage-2 recoveries or rolling tops. Re-ran ww breadth validate after the point-in-time gmi() fix: exact-match 20%->24%, corr 0.60->0.66, his-GMI-0 days now reconstruct 0-1 (was 3-4); methodology/gmi.md validation section updated.

## [2026-08-12] lint | end-to-end semantic review — coverage, provenance and backfill gaps

Full pass over `wiki/**` against the corpus manifest (`raw/url_map.json`, 4,655 posts).
Caveat: `raw/posts/` and `raw/posts.jsonl` were absent and `wishingwealthblog.com` is
blocked by this environment's egress proxy, so post *bodies* could not be re-read; the
coverage analysis works from post titles/slugs plus the wiki's own citations.
`ww lint .` is clean (0 errors, 1 corpus-absent warning).

**Provenance risk (highest priority).** `raw/posts.jsonl` has never been committed
(`git log --all -- raw/posts.jsonl` is empty) and `/raw/posts/` is gitignored. The ingest
ledger — tier, summary, indicators, tickers and the `ingested` flag for all 4,655 posts —
therefore exists only outside version control. Recoverable state in git is limited to the
91 filenames under `wiki/sources/` plus this log. Re-deriving it requires both a machine
that can reach the blog and the WordPress API still serving the full archive.

**CLAUDE.md §6 resume state is stale.** It reports "~31 teaching and ~2 trade_example
fully ingested … ~149 long_form remaining" as of 2026-05-11; batches 6–8 (logged below
that date) took it to 91 source-summary pages / ~79+ ingested. A fresh session reading the
schema starts from the wrong picture.

**Corpus coverage.** 91 posts (2.0%) have summary pages; 129 distinct posts are cited
anywhere in the wiki. Year holes: **2007** — 185 posts, 0 source pages, 0 `timeline.md`
sections, despite spanning the October 2007 top; **2015** — 1 source page, 0 timeline
sections; **2019** — 1 source page; 2006, 2008 and 2024 are thin. A title-pattern sweep
finds ~109 un-ingested posts carrying explicit teaching markers ("how I…", "introducing…",
"why I…", "…explained"), clustered in 2021–2022 (26) and 2019–2020 (14).

**Concept gaps — taught on the blog, absent from the wiki.** (1) **OSB / ATHOSB**
(oversold bounce) — zero occurrences anywhere in `wiki/`, yet 2023-07-13 states he *prefers*
the OSB setup over breakouts; doctrine-level omission. (2) The **$200 price-level revision**
(2021-08-11 "why buying stocks over 200 works better revisited") supersedes the $80/$100
rule that `stock-selection.md` still presents as current. (3) **Hourly / multi-timeframe
GMMA** (2022-08-07, 2019-11-03) — the hourly layer is undocumented. (4) **Position sizing
and portfolio construction** — no page; only scattered asides. (5) **Short-side playbook** —
SQQQ, protective puts and the submarine scan are spread across three pages with no unifying
page. (6) **Off-blog teaching corpus** — ~63 posts point at Worden webinars, AAII workshops,
TraderLion, TASC interviews, YouTube tutorials and his TC2000 club; the wiki has no map of
where that material lives. (7) **Trading psychology / discipline** — 2009-11-26 ("my trading
philosophy and why I use technical analysis") and 2019-03-15 ("how I avoid getting shaken out
of strong growth stocks") are un-ingested; no page owns the topic. (8) **Twitter/tweet alerts**
as his signal-delivery channel. (9) **University-course context** — the 2020-12-13 "final 10
thoughts for my fall semester freshmen class" is an un-ingested capstone summary.

**Open definitional questions still unclosed.** The GMI's *current* six components are
unconfirmed — `gmi.md` documents the 2005 list, flags component 6 as "later replaced or
modified" without resolving it, and records GMI-R/GMI2 components as undisclosed. The QQQ
short-term flip rule remains an inference (30-day MA) rather than a verbatim disclosure.

**Page-level defects found.** `overview.md` carries four stale `*(stub)*` markers for
`market-state.md`, `buying-glb.md`, `exits.md` and `track-record.md` — all four are now
populated (817–2,565 words). `timeline.md` is ordered by ingest sequence, not chronology
(April 2005 → November 2005 → June 2005 → … → February 2009 → January 2009), which defeats
the page's purpose. 24 in-body citations across 9 pages are absent from those pages'
`## Sources` blocks (`trend-flip-log.md` 8, `buying-glb.md` 4, `market-state.md` 3) — `ww lint`
checks only that the heading exists, so this drift is invisible to CI. The founding GMI post
`2005-04-26-general-market-index-gmi` is cited on 5 pages and is the most-cited post with no
summary page. All 129 cited slugs resolve to real posts in `url_map.json` — no fabricated
citations.

## [2026-08-12] lint | acted on the review — page fixes, and the ingest ledger put under version control

Follow-up to the review entry above.

**Page fixes.** `timeline.md` re-sorted chronologically — its 82 sections had been
appended in ingest order (April 2005 → November 2005 → June 2005 → … → February 2009 →
January 2009), which defeated the page's only job; all 82 headings preserved, the diff is
a pure reorder (123 insertions / 123 deletions). `overview.md`: the four stale `*(stub)*`
markers replaced with real one-line descriptions (`market-state.md`, `buying-glb.md`,
`exits.md`, `track-record.md` have all been populated for months), plus a new bullet for
the bounce-off-support entry family (BOS / WGB / the dot signals), which the overview had
never mentioned despite it being his stated preference over buying the GLB moment.
The 24 in-body citations missing from their pages' `## Sources` blocks are now listed, and
added to each page's `sources:` front-matter — 9 pages touched, link text reused from the
canonical bullet already used elsewhere in the wiki.

**Lint gained two checks**, so this class of drift fails CI instead of accumulating:
a post cited in a page's body but absent from that page's `## Sources` block is now an
error (text-based, so it works without the corpus), and `summary_page` integrity is
checked on `raw/ingest-ledger.jsonl` as well as `raw/posts.jsonl`.

**The ingest ledger is now committed.** `raw/ingest-ledger.jsonl` (91 rows) holds the
curated half of `posts.jsonl` — tier, summary, indicators, tickers, `ingested`,
`summary_page` — keyed by post stem. New module `src/ww/corpus/ledger.py` and `ww ledger
export | apply | rebuild`: `export` after each Ingest batch (commit the result), `apply`
after a `ww scrape` to re-attach state to a fresh corpus, `rebuild` to reconstruct from
`wiki/sources/*.md` if the ledger itself is lost. The committed ledger was produced by
`rebuild` and recovers 85 `teaching` + 6 `trade_example` rows with the richer one-line
summaries catalogued in `index.md`. Verified end-to-end against a synthetic 4,655-row
corpus built from `url_map.json`: 91 applied, 0 unmatched. `daily_update` and `meta` tiers
have no summary page and so are *not* recoverable this way — they must be re-derived after
a scrape.

**Still blocked:** `wishingwealthblog.com` is denied by this environment's egress policy
(GitHub-only), so the corpus could not be re-fetched here and no new posts were ingested.
Everything above works without post bodies. `ww lint .` clean; 181 tests pass.

## [2026-08-12] ingest | OSB/ATHOSB doctrine + the $200 revision + GMI component 6 resolved — 13 posts, tier=teaching×9/trade_example×4

Corpus restored (`ww scrape`, 4,694 posts) and committed, which unblocked the three
highest-priority gaps from the review entries above.

**(a) OSB / ATHOSB — new page `methodology/oversold-bounce.md`.** The review flagged
zero occurrences of "OSB" anywhere in `wiki/`; the corpus has 27 posts mentioning it.
The doctrine post is 2023-07-13: he prefers the oversold bounce **to breakouts**, and the
reason is stop placement, not hit-rate — "with a failed break-out... it is not always easy
to designate [the stop] in advance," whereas with an OSB you "place the stop just below the
low of the bounce." Also recovered: the setup's first naming (2021-05-06), the scan
definition (2021-05-23), the ATHOSB name and the disclosed oversold basis — the daily
10.1/10.4/10.4.4 stochastics (2022-06-15), the recent-yearly-high refinement (2023-07-09),
industry clustering as a second-order read (2023-07-10), the unconditional immediate-stop
rule and earnings-gap caveat (2023-08-03), the GLB+OSB pairing (2023-09-13), and the
blue-dot variant that carries the setup into current practice (2025-07-09).
**Framing decision:** OSB is presented as a renamed and tightened continuation of BOS
(2016), not as a new idea — BOS triggered off the lower 15.2 Bollinger Band, OSB adds the
recent-ATH prerequisite and a stochastic trigger. `green-line-breakouts.md` gained a
caveat section saying the GLB is load-bearing for *identification* and weaker as an
*entry*, which is what the corpus actually supports.

**(b) The $200 revision (2021-08-11).** Flagged as a supersession per CLAUDE.md §4.3
rather than overwritten: `stock-selection.md`'s section is now
"$80+ (2011) → $100+ (2018) → $200+ (2021)" with a callout naming $200 as current and the
earlier numbers kept as the audit trail — they carry the only quantitative evidence he has
ever published for any of the three. The operational detail that makes it more than a
preference: the threshold was added as a filter to the **OSB scan** specifically.

**(c) GMI component 6 — open question closed.** `gmi.md` had flagged component 6 as
"later replaced or modified" without resolving it. **It was never replaced.** Confirmed in
his own words at four separated dates: 2008-08-22, 2009-01-12, 2023-08-09 and 2025-12-14 —
the last being the most recent verbal description of any GMI component in the corpus, and
still "the IBD Growth Mutual Fund index (0MUTI) has closed above its 50 day average."
Also recovered: the series' symbol (`0muti`, inside IBD's own charting application, adopted
after IBD stopped publishing the 50-day average), and that the GMI-R is "more sensitive"
than the GMI and shares component 6 with it. The reconstruction note in `gmi.md` was
corrected accordingly — FFTY substitutes for a series that is still live and identifiable,
not a retired one. *Still open:* the daily GMI table is published as an image, so the exact
current wording of components 3–5 has not been recovered from post text.

**Also fixed:** `timeline.md` still had one section out of chronological order —
November 2021 sat between April 2023 and June 2023 (it had been filed by ingest date,
since the exit was documented retroactively in a June 2023 post). Moved to 2021.

Touched: **new** `methodology/oversold-bounce.md`; `methodology/gmi.md` (component-6
resolution section, GMI-R sensitivity, reconstruction note), `methodology/stock-selection.md`
($200 supersession, OSB cross-reference), `methodology/green-line-breakouts.md`
(entry-vs-identification caveat), `methodology/glossary.md` (OSB, ATHOSB, 0muti, VCP),
`history/timeline.md` (5 new sections + 1 reorder), `overview.md`, `index.md`;
13 new `sources/` pages. `ww lint .` clean; 181 tests pass; `ww ledger export` run.

## [2026-08-12] ingest | 2007 — 7 posts, tier=teaching; the year-hole closed and two undocumented indicators recovered

The review flagged 2007 as the worst coverage hole: 185 posts, 0 source pages, 0
`timeline.md` sections, spanning the October 2007 top. `timeline.md` jumped straight
from May 2006 to June 2008.

**What the year actually contained.** More than a gap-fill — 2007 is when the
supporting composites were reported in full, and two of them were absent from the wiki:

- **GMI-L** — "my longer term measure of weekly trends," reported as a percentage and
  published throughout 2007. Now documented in `gmi.md` and the glossary. Its value is
  comparative: it fell to 31% in December 2007, and *"in the two declines in 2007 (March
  and August), the GMI-L never fell below 50%"* — so sub-50% separated the onset of the
  2008 bear from an ordinary correction. It still read **94%** days after the October top.
- **GMI-S construction, disclosed** — the page previously said "its construction is not
  disclosed." It is: "Only one of the 16 short term indicators for the IJR, DIA, SPY and
  QQQQ is positive (GMI-S: 6%)" — i.e. the percentage of sixteen short-term indicators
  across four index ETFs that are positive. Corrected.

**Two further GMI findings.** (1) The daily-trend components are **30-day-average tests**:
"Several closes below the 30 day would decrease the GMI" (2007-09-17). `gmi.py` had
treated the 30-day SMA as an unverified proxy; it is better supported than that. (2)
Component 5 is the **"Weekly QQQQ Index"**, which he singles out as "my primary indicator
of a longer term up or down move," charted against the 30-week average (2007-11-19).

**A threshold inconsistency, recorded rather than resolved.** 2007-08-20 gives "exit
below 4, buy above 3" — the earliest statement of the rule the wiki had been citing to
2011. But 2007-10-29 says "I will trade long as long as the GMI is greater than 2."
`gmi.md` now carries a small table of all four stated variants; ≥4/≤3 remains the
dominant and durable reading and is what the backtest uses.

**The October 2007 top is now documented as a case where the indicators did not fire.**
Three weeks after the peak: GMI 4 (and only because Successful 10-Day turned negative
"barely"), GMI-L 94%, GMI-R 80%, QQQQ on Day 41, seven weeks of closes above the 10-week
average. The long-term signal held until November, and the GMI read 1 rather than 0
precisely *because* the Weekly QQQQ Index stayed positive while QQQQ sat on its 30-week
average — a support test he marked with a "?" rather than calling.

**Also recovered:** the earliest and sharpest statement of the capital-conservation
doctrine ("THE KEY TO SUCCESS IN TRADING IS HOW LITTLE ONE LOSES DURING MARKET WEAKNESS",
2007-12-17) and the behavioural failure it exists to prevent ("I used to profit in the
up-trend and give it all back and more in the subsequent decline"); T2108's **~80%
post-decline recovery expectation**, which makes a *failed* recovery a signal in itself;
the **covered-call income strategy** (2–4%/month, later constrained by the 2014 "never on
rocket stocks" rule); his own **audit of the IBD100** finding survivorship bias in IBD's
published figures and ~4-month leadership decay; **buy-stop automation** with the Darvas
precedent; and contrarian sentiment framed as a bounce warning, never a re-entry trigger.

Touched: `history/timeline.md` (new consolidated 2007 section covering May/Aug/Sep/Oct/
Nov/Dec), `methodology/gmi.md` (GMI-L, GMI-S construction, 30-day and Weekly-QQQQ
corroboration, threshold table), `methodology/glossary.md` (GMI-L; GMI-S construction),
`methodology/t2108.md` (pendulum / 80% recovery), `methodology/risk-and-cash.md` (capital
conservation, covered calls, contrarian sentiment, relative strength in declines),
`methodology/stock-selection.md` (IBD100 caveats, buy-stop automation),
`history/track-record.md` (what the panel read at the top; Oct 2000 attribution),
`index.md`; 7 new `sources/` pages. `ww lint .` clean; 181 tests pass; ledger exported
(111 rows).

**Still open from the review:** 2015 and 2019 remain at one source page each; hourly /
multi-timeframe GMMA, position sizing, a unified short-side page, the off-blog teaching
map, trading psychology and the Twitter alert channel are all still unwritten. The GMI
table's current component *labels* remain unrecovered because it is published as an image.

## [2026-08-12] lint | end-to-end review #2 — measured against the full corpus

First review run with `raw/posts/` actually present, so these are counts rather than
title-pattern inferences. `ww lint .` clean; 181 tests pass.

**Coverage.** 151 of 4,694 posts are cited anywhere in `wiki/` (3.2%); 111 have summary
pages (2.4%). Year-by-year, citations as a share of that year's posts:

| Hole | Posts | Cited | Source pages | `timeline.md` §§ |
|---|---|---|---|---|
| **2008** | 240 | 3 | 1 | 6 |
| **2015** | 242 | 1 | 1 | **0** |
| **2019** | 240 | 1 | 1 | 1 |
| **2024** | 168 | 2 | 2 | 2 |
| 2006 | 218 | 3 | 2 | 2 |
| 2012 | 257 | 3 | 3 | 3 |
| 2013 | 241 | 4 | 4 | 4 |

**2008 is now the worst hole, and it is worse than 2007 was.** One source page for the
year that contains the defining episode of his entire track record — the crisis his GMI
is credited with avoiding. The 2007 work just done makes this more conspicuous, not less:
the December 2007 GMI-L warning has no 2008 follow-through documented from primary sources.
2015 is the only year left with *zero* timeline sections.

**Concept gaps, ranked by corpus frequency against wiki presence.**

1. **MACD as a breadth gauge — 231 corpus mentions, 6 in wiki.** Not a per-stock signal:
   he reports "% of Nasdaq 100 stocks with MACD above its signal line" as a short-term
   strength/weakness reading, in the same breath as the GMI. An undocumented indicator,
   and a plausible member of the GMI-S's sixteen.
2. **Mark Minervini — 66 mentions across 31 posts, 1 in wiki.** 2016-10-25 is a dedicated
   post on his 3-day Master Trader Program (taught with David Ryan), covering stop-setting,
   pyramiding, cutting losses and a session on trading psychology. The wiki has a lineage
   (Darvas / O'Neil / Weinstein / Livermore / Wyckoff) that stops before the modern
   influences.
3. **Cup with handle — 60 mentions across 41 posts, 0 in wiki.** A chart pattern he names
   and trades, entirely absent.
4. **Window dressing — 131 mentions across 110 posts, 3 in wiki.** Quarter-end flows he
   positions around; no page owns calendar/seasonal effects.
5. **IBD follow-through day — 62 mentions, 3 in wiki.** Notable because he is *sceptical*
   of it: "Maybe IBD has decided that a high volume follow through day is no longer needed"
   (2010-12-06). A documented disagreement with IBD orthodoxy is exactly the kind of thing
   this wiki should record.
6. **Yellowband — 39 mentions of "yellow band", 0 (the glossary has the one-word spelling
   only), plus an un-ingested teaching post 2017-06-25 "How I use Yellowband up and down
   trends."** The glossary currently frames it as an *abandoned* earlier term; a 2017
   how-to post says otherwise.
7. **Selling climax (22/2), post-earnings handling (26/0), mutual-fund market-timing
   restrictions.** The last is a real operational constraint on the pension strategy the
   wiki presents as frictionless — funds blocking re-entry after a timing exit (2010-12-06).
8. **Off-blog teaching corpus** — YouTube 78 mentions / 1 in wiki; interviews 26 / 1. Still
   unmapped, as flagged in the first review.
9. **Trading psychology** still has no owner. Two un-ingested posts are squarely on it:
   2009-11-26 "My Trading Philosophy and Why I Use Technical Analysis" and 2019-03-15
   "How I Avoid Getting Shaken Out of Strong Growth Stocks".

57 un-ingested posts carry explicit teaching markers in their titles, clustered 2022 (8),
2025 (6), 2015 (5), 2016 (5), 2023 (5).

**Structural — the wiki has outgrown its own convention.** CLAUDE.md §2 says to split a
page past ~800 words. **13 of 18 pages exceed it**, several by 4–7×: `timeline.md` 6,034,
`stock-selection.md` 4,574, `moving-average-rules.md` 4,105, `risk-and-cash.md` 3,990,
`green-line-breakouts.md` 3,864. `stock-selection.md` is now doing at least eight jobs
(screens, price levels, RWB, four scans, BOS, the dots, biotech, IBD comparisons, an
O'Neil diary excerpt) and is the natural next split — the scan catalogue and the
entry-signal family are each their own page.

**The playbooks are the thinnest layer and should be the thickest.** 3,696 words across
three pages against ~25,000 in methodology. `market-state.md` is 891 words. These are the
pages that answer "what do I do today," and they are the least developed.

**Provenance.** 40 cited posts have no summary page. The founding GMI post
(`2005-04-26-general-market-index-gmi`) remains the most-cited post in the wiki (5 pages)
with no summary page — flagged in the first review, still open.

**Schema drift.** CLAUDE.md §2 promises `risk-and-cash.md` covers "modified buy-and-hold"
and `moving-average-rules.md` covers "the 10-week rule". Neither phrase occurs anywhere in
4,694 posts. They are schema-invented terminology and should be dropped or renamed before a
future session hunts for a concept the blog does not have.

**Fixed in this pass.** `timeline.md` had one section out of chronological order — July 2025
sat after October 2025, introduced by the OSB batch earlier today. `track-record.md`'s data
note carried pre-re-scrape counts (1,797 / 989 / 808); refreshed to 1,811 / 995 / 816 and
`raw/timeline.parquet` rebuilt.

**Checked and cleared.** `ww timeline` keys off `kind_guess`, not `tier`, so the outstanding
`daily_update` tier regression does not block the timeline dataset — it rebuilt cleanly
(1,811 rows, 2005-07-25..2026-08-05). The remaining ordering flag in `timeline.md` is the
dual-dated "October 1995 (diary) / October 2016" heading, which is intentional.

**Suggested next batch, in priority order:** (1) 2008 — the crisis year, from primary
sources; (2) MACD breadth + the GMI-S sixteen; (3) a psychology/discipline page from the
2009 and 2019 posts; (4) Minervini/modern-influences and the off-blog map; (5) split
`stock-selection.md`; (6) 2015 and 2019; (7) thicken the playbooks.

## [2026-08-12] lint | review #3 — context backfill: what we cannot reconstruct about him

A third pass, asking a different question from the coverage review above: not *which topics
are missing* but *what context is unrecoverable from what we hold*. Three structural findings,
one of which changes how the ingest queue should be chosen.

**1. He curates his own corpus, and we never captured it.** The scraper requests only
`content,date,id,link,slug,title` (`_DEFAULT_FIELDS` in `src/ww/scrape/wp_api.py`). The
WordPress API also exposes `categories`, `tags`, `excerpt`, `author`, `modified`, `views`
and a separate `/comments` endpoint. His category taxonomy — now captured to
`raw/categories.json` — is:

| Category | Posts | Un-ingested |
|---|---|---|
| General Market Index (GMI) table | 866 | — |
| **My Favorite Posts** | **145** | **112** |
| Nicolas Darvas | 65 | 54 |
| Tutorial | 13 | 7 |
| UMDSMC Education Posts | 11 | 9 |

**"My Favorite Posts" is Dr. Wish's own answer to "what matters most," and 112 of 145 are
un-ingested.** Every ingest batch to date has selected posts by word count and title-pattern
heuristics; his own curation was sitting in the API the whole time and is a strictly better
signal. `Tutorial` (13, explicitly instructional) and `UMDSMC Education Posts` (his
University of Maryland course) are small, high-density, and nearly untouched.

Worth noting the two queues are *not* the same job: only 14 of the 112 un-ingested favorites
fall in the year-holes identified in the review above, and **2007 and 2008 contain zero
favorites at all** — his curation skews hard to 2017–2026 (91 of 145). Year coverage and
his own curation are orthogonal priorities and should be worked separately.

**2. The visual layer is ~half the blog and we read none of it.** 6,354 embedded images
across **3,599 of 4,694 posts (77%)**, against 713k words of text. Of those, **2,547 are
GMI-table images** on a systematic `gmi<date>` filename convention, plus `wpm<date>` (WPM
tables) and `ibdperf<date>` (IBD performance tables). This is the direct answer to an open
question the wiki has carried for two sessions: `gmi.md` says the current component *labels*
for slots 3–5 "remain unrecovered because the daily GMI table is published as an image."
Those images are enumerable, dated, and downloadable. The same applies to the GMI-R, GMI2,
GMI-S and GMI-L component lists, all recorded as "undisclosed" — they are very likely
printed in the table rows. A single OCR pass over a sample of `gmi*` images would probably
close every open GMI definitional question at once.

**3. 4,136 reader comments exist and none are captured.** The comments endpoint returns
them; the scraper never asks. On a methodology blog the comment threads are where readers
ask "what exactly counts as a close below?" and he answers — clarifications that by
definition do not appear in the post text. This is the single largest body of primary
material we have never looked at.

**Secondary findings.**

- **4,922 in-corpus self-references** (`wishingwealthblog.com/20…` links inside post bodies).
  He builds context by citing his own prior posts constantly — that is a resolvable citation
  graph, and it is his own map of which posts he considers foundational. Unused.
- **Where he sends readers off-blog**, by link count: worden.com 86, guppytraders.com 71,
  youtube.com 56, investors.com 43, amazon.com 43 (book recommendations), proshares.com 35,
  aaiidcmetro.com 16. The "off-blog teaching corpus" gap flagged in earlier reviews now has
  concrete destinations and volumes rather than an estimate.
- **No biography or career-arc page.** The wiki documents the method thoroughly and the man
  barely at all: trading since the 1960s, the 1990s diary, a university teaching career, the
  Worden/AAII/TraderLion circuit, co-instructor David McCandlish (deceased). A reader cannot
  currently answer "who is this and why should I trust the track record."

**Recommended sequencing change.** Before the next content batch, spend one small session on
plumbing, because it changes what every later batch can do: (a) widen `_DEFAULT_FIELDS` to
include `categories`/`tags`/`modified` and persist them on `PostRecord`; (b) add a comments
fetch; (c) OCR a sample of `gmi*` images to close the GMI component questions. Then work
"My Favorite Posts" as the primary ingest queue, with the 2008 / 2015 / 2019 year-holes as a
separate parallel track.

`ww lint .` clean; 181 tests pass. `raw/categories.json` committed as the evidence and as a
ready-made ingest queue.

## [2026-08-12] ingest | the GMI table images — every open GMI definitional question closed

Acting on review #3's finding that the visual layer was never read. Read four GMI table
images spanning 2007 / 2013 / 2020 / 2026 (they are ~2,547 dated images on a systematic
`gmi<date>` filename convention). No OCR needed — the images are legible directly.

Everything the wiki had recorded as "undisclosed" or "not recovered" is printed in the table.

**GMI — all six labels verbatim, and unchanged since 2005.** Two amendments the prose never
mentioned: component 1 carries a **`min. 20` floor** (the ≥50% rule is suspended below 20
qualifying stocks — a small-sample guard), and component 2's universe drifted with the data
source, **`4,000 STOCKS` (2007) → `5,000+` (2013, 2020) → `6,000+` (2026)** while the
threshold stayed at 100. That means the component has quietly got easier to satisfy, which
matters for any cross-era comparison of GMI readings — including our own backtest.

**GMI-R's four extra indicators are named** (2007 table, items 7–10 marked `*`): more new
highs than lows; QQQQ above its 10-week, 4-week and 10-day averages. So the GMI-R is the slow
structural GMI plus a fast QQQQ trend ladder — which is precisely why he calls it "more
sensitive."

**GMI2 was wrong on this page and is not a fixed 6-component index.** It grew
**6 → 8 → 9** components between 2013 and 2026, inheriting the GMI-R's four extras as its own
first four. The 2013 "QQQ closed above 5 month average" was dropped and replaced by
oscillator tests — 10.4 and 10.1 stochastics and a 12/26/9 MACD histogram condition. Its
character changed from a trend panel to a trend-plus-oscillator panel, and **a GMI2 value is
not comparable across eras** (his own tables print the denominator, e.g. `GMI2: 5/6`). The
stochastics driving GMI2 components 6 and 9 are the same ones behind the black and blue dots
of the [oversold bounce](../methodology/oversold-bounce.md).

**GMI-S construction settled.** The 2007 table prints
`GMI Short term index (GMI-S): 44 (SPY:50, QQQ:75, DIA:25, IJR:25)` — the mean of four
per-ETF readings, each moving in 25-point steps, i.e. four indicators per ETF. That is
exactly the "16 short term indicators for the IJR, DIA, SPY and QQQQ" of the prose. Shape
settled; the identity of the four per-ETF tests is still undisclosed.

**The MACD question from review #2 is answered.** 231 corpus mentions against 6 in the wiki:
it is a **breadth gauge with a permanent slot in the table** — "% of Nasdaq 100 stocks above
MACD signal line," with weekly change — not a per-stock entry signal and not a GMI component.
A separate MACD test on QQQ itself *is* GMI2 component 7.

**A threshold conflict surfaced and is now documented rather than smoothed.** The daily table
prints "*Market tops likely above 80, bottoms likely below 25*" (80/30 in 2007). `t2108.md`
taught only the **<10%** contrarian zone. Both are his: 25–30% is the routine daily band,
<10% is the rare extreme he actually buys into. The page now carries both.

**Also recovered:** the table's standing context block (QQQ trend count, weeks above/below the
10-week for QQQ and SPY, weeks the QQQ 10-week has been above the 30-week, T2108, MACD
breadth, QQQ weekly 10.4 stochastic), and a footer that points readers at **"my favorite
posts" for GMI definitions** — corroborating that category as the definitional source and as
the right ingest queue.

Touched: `methodology/gmi.md` (verbatim labels; GMI-R extras; the GMI2 evolution table;
GMI-S construction; the published-table context block), `methodology/t2108.md` (two bands),
`methodology/glossary.md` (**GMI table**, **MACD breadth**), `index.md`. 3 posts recorded as
`daily_update` for their tables (2013-01-07, 2020-01-05, 2026-01-04). `ww lint .` clean;
181 tests pass; ledger exported (114 rows).

**Method note for future sessions:** the images are readable directly by the model — no OCR
dependency. `wpm<date>` (WPM tables) and `ibdperf<date>` (IBD performance tables) follow the
same convention and are still unread.

## [2026-08-12] ingest | first batch from "My Favorite Posts" — 5 posts, tier=teaching

The first batch selected from **his own curation** rather than from word-count and title
heuristics, using the new `ww batch --category "My Favorite Posts"`. 95 → 90 remaining.
Deliberately chosen against the gaps the three reviews identified, and four of the five
corrected something the wiki had wrong.

**New page: `methodology/trading-philosophy.md`.** Trading psychology and first principles had
no owner. The 2009-11-26 post supplies them as five numbered propositions: markets are
unpredictable; trends nonetheless persist; so identify trends once begun and stay with them;
since only ~50% of trades work, winners must dwarf losers (stops and small initial positions;
riding and pyramiding); and therefore **success is determined mostly by exit rules, not entry**
— "one could probably **select stocks at random** as long as losses are kept at a minimum and
profits are maximized." Previously published under the pseudonym **Sir Silent Knight** in the
Worden TC2007 journal. The page maps each proposition onto the machinery it produced.

**The founding GMI post finally has a summary page.** `2005-04-26-general-market-index-gmi`
was the most-cited post in the wiki with no summary across two reviews. It also shows component
1 was explicitly provisional from day one — "I reserve the right to change this threshold" —
which is exactly what the 2014 ≥50% rule and the table's `min. 20` floor turned out to be.

**Correction — the GMI has a published limitation, and we never recorded it.** In February 2015,
with the GMI at 6 of 6, he documented that it had issued **7 Sell and 7 Buy signals since early
2014 while the QQQ never left its RWB up-trend**, and demoted it: GMI for short-term trading
only, weekly GMMA for the pension. This is the origin of the two-speed design the wiki
described but never justified. **It also reframes our own backtest**: the "marginal" verdict
measures the GMI at a job he explicitly abandoned in 2015. `backtest-timing-overlay.md` now
says so, and names the untested alternative (stay long while the weekly RWB holds).

**Correction — yellowband is not a superseded term.** The glossary said he moved away from it.
The 2017-06-25 post — itself a favorite — presents it as a *primary* framework: a 1990s pattern,
defined precisely as weekly closes above a **rising** 10-week average that is itself above a
**rising** 30-week, used both to select ("I primarily buy stocks... that have a yellowband
up-trend") and to hold ("I try not to sell as long as the yellowband is intact"). Its job is
preventing premature exits. The December 2017 post the glossary relied on is six months *later*
and concerns a different job (when to leave, not whether to hold). Entry rewritten with the
misreading noted.

**Correction — the bounce-over-breakout preference is from 2018, not 2023.** The green-dot post
states it plainly: "I have more success trading strong up-trending stocks that are turning up
after they have had a small decline **than buying break-outs**... I know exactly where to get
out if I am wrong." So 2023-07-13 is the sharpest statement, not the origin; the reasoning runs
2016 (BOS) → 2018 → 2023 unchanged.

**The green dot is now fully specified** rather than a one-line reference: 10.4.4 daily
stochastic, fast crossing above slow, preferably below 50; the dot drawn **at the 5-day low**,
so its placement *is* the stop reference; written in TC2000 by co-instructor David McCandlish;
prerequisites (daily RWB or yellowband confirmation, price above a rising 30-week average);
and two exit triggers. Plus a methodological rule for the philosophy page — "I try not to rely
on a single indicator."

Touched: **new** `methodology/trading-philosophy.md`; `methodology/gmi.md` (the 2015
limitation), `methodology/glossary.md` (yellowband rewritten, green dot fully specified),
`methodology/oversold-bounce.md` (preference back-dated to 2018),
`methodology/backtest-timing-overlay.md` (reframed against his own finding),
`history/timeline.md` (4 new sections: Nov 2009, Feb 2015, Jun 2017, Mar 2018), `index.md`;
5 new `sources/` pages. `ww lint .` clean; 189 tests pass; ledger exported (119 rows).

**Queue state:** 90 of 145 favorites remain un-ingested, plus `Tutorial` (7) and
`UMDSMC Education Posts` (9). Year-holes 2008 / 2015 / 2019 / 2024 remain a separate track —
2008 still has one source page and contains zero favorites.

## [2026-08-12] ingest | blog-post context — the comment threads made reachable and mined

The 4,136 comments captured earlier today were inert: stored but unreachable and unused.

**`ww search` now covers them.** `build_index` indexes one chunk per comment, and hits carry a
citation naming the author, the date and the parent post (`ww search "…" --source comments`).
The index grew 5,472 → 9,776 chunks. Pickles written before comments existed still load
(`comment_meta` defaults empty).

**First mining pass — new page `methodology/reader-qa.md`.** Of the 678 replies by Dr. Wish,
501 answer a reader directly and 128 are substantive rule answers. What they contain is not a
restatement of the posts; it is the edge cases readers pushed him on.

Highest-value findings:

- **How the green line is actually drawn**, three ways the posts never say. The 3-month test is
  in *monthly closes* ("a peak that is not followed by a higher monthly close for 3 months");
  the line is **not always the intraday ATH** ("sometimes near its highest monthly close which
  may be below the highest price it traded at during the month if it did not hold") — which
  explains why two readers can legitimately draw different lines on the same chart; and
  **there is no GLB scan at all** — "I do not have a single scan for this... I **manually draw
  in green lines**," with TC2000 automating only the alert. For a toolkit that is otherwise
  scan-driven, that is a significant qualifier.
- **A correction to what this log claimed a few hours ago.** The previous entry credited the
  Feb-2015 post with originating the two-speed design (GMI for trading, GMMA for the pension).
  It did not: the practice is stated as settled routine in a **November 2010** comment. 2015 is
  where he published the *evidence* and formalised it. `gmi.md` corrected.
- **The pension has an administrative constraint, not only a signal:** "I am limited as to how
  often I can transfer funds in and out of equity funds." The wiki had presented pension moves
  as purely signal-driven; some of the lag is structural. `risk-and-cash.md` updated, tied to
  the 2010-12-06 post where he attacks fund market-timing restrictions publicly.
- **What the GMI is *not*:** "GMI does not require 10 week to be above 30 week" — a useful
  negative confirming the component list is complete and Stage 2 sits outside it. Plus its 2010
  cadence: updated weekly, not nightly.
- **Stops are support levels, not percentages**; the 30-day rule for momentum stocks stated in
  2009 with a bounce entry and bounce-low stop — earlier than BOS (2016); and a defence of
  stop-losses after the 2010 flash crash.
- **Re-entry after being stopped out** recurs and the post pages under-weight it: "such
  situations have often provided me with my best profits."
- **The hourly timeframe** — flagged as undocumented in review #1 — appears in his research
  chain: "monthly... then weekly, daily and hourly." Still no page for it.

**CLAUDE.md §3 gains a citation convention** for comments (`WW comment <date>` + permalink; not
listed in `## Sources`, which catalogue posts only).

Touched: `src/ww/search/index.py` (+5 tests), `cli.py`, **new** `methodology/reader-qa.md`,
`methodology/gmi.md` (two-speed origin corrected), `methodology/green-line-breakouts.md`
(drawing mechanics), `methodology/risk-and-cash.md` (fund-switch constraint), `CLAUDE.md`,
`index.md`. `ww lint .` clean; 194 tests pass.

**Still unmined:** ~373 of the Q→A pairs and the 3,458 reader-authored comments (which show
what people actually find unclear — a map of where the wiki should be more explicit).

## [2026-08-12] lint | post-coverage audit — the honest denominator, and what is actually missing

Direct question: has the wiki covered all the blog posts? **No — 2.5%.** The full taxonomy,
measured rather than estimated:

| Bucket | Posts | Share |
|---|---:|---:|
| 1. Ingested, with a `wiki/sources/` page | 121 | 2.6% |
| 2. Cited in a wiki page, no summary page | 40 | 0.9% |
| 3. Parsed into `raw/timeline.parquet` only (structured signal extraction, no prose) | 1,784 | 38.0% |
| 4. **Untouched — never read, never parsed** | 2,749 | 58.6% |

**But bucket 4 is not 2,749 lost essays**, and this is the part that changes the plan. Its word
counts: median **33**, p75 118, and **77% are under 150 words**. 2,269 of them carry at least one
chart. They are overwhelmingly image-first daily posts where the text is a caption and the
content is in the picture — which is why `kind_guess` calls 2,659 of them "unknown."

**The real target is the prose subset: 574 untouched posts with ≥250 words.** By year that set is
front-loaded hard — **113 are from 2005**, 59 from 2006, and the longest untouched post in the
corpus is 1,909 words from 2005-05-13. The early blog was long-form essay writing and we had read
almost none of it. Also in bucket 4: 67 of his "My Favorite Posts", 37 "Nicolas Darvas" posts.

**Sampling confirmed real loss, not just noise.** A random draw of six untouched posts returned
one that is plainly methodology — 2017-07-23, "TC2000 Scan for bounce up off of support," 312
words describing a new scan with its criteria — alongside genuinely empty ones ("[CHART]
Screenshot", 1 word). So the untouched bucket is low-density, not zero-density.

**First 2005 batch ingested as proof of the thesis, and it was the richest material in weeks:**

- **2005-04-20 "STOP THIS MADNESS"** — written *six days before the GMI was named*, and three of
  its six components are already running as standalone indicators, each explained more fully
  than in the founding post. **The GMI is a packaging of instruments already in use**, which is
  the best explanation yet for why its components have been so stable for twenty years. It also
  discloses that the IBD mutual fund index tracks **23 growth mutual funds** (new), reveals that
  component 1's "greater than 100" threshold is simply its March-2005 reading (hence
  "provisional"), and adds a meta-signal the wiki had nowhere: "**a good indication that things
  are souring is when the types of trades I have been profiting from suddenly produce a string
  of losses**." Plus a full rebuttal of the "you'll miss the best N days" anti-timing argument.
- **2005-05-04 "A Google Confession"** — the earliest form of the **gap rule** ("the trick is to
  wait to see if the gap is filled"), which is the conceptual ancestor of the 2022 gap-up scan,
  seventeen years earlier. Explains Darvas's already-doubled criterion as a base-rate argument.
  Treats the stop as the thing that *buys emotional detachment*. And states the one prohibition
  in capitals: "NEVER BUY MORE OF A STOCK THAT HAS DECLINED."

**Revised priority.** Chasing raw post coverage is the wrong goal — bucket 4 is 58.6% of posts
but a small share of the *prose*. The ordered targets are now:

1. **The 574 untouched ≥250-word posts**, worked newest-value-first but with **2005–2006 (172 of
   them) treated as a block** — that is where the founding reasoning lives.
2. The 90 remaining "My Favorite Posts".
3. **2008** — still 1 source page for the crisis year, and it contains zero favorites, so his own
   curation will never surface it.
4. The image layer: `wpm<date>` and `ibdperf<date>` tables are still unread, and 3,888 chart
   images sit inside bucket 4.

`ww lint .` clean; 194 tests pass; ledger exported (121 rows).

## [2026-08-12] lint+ingest | 2010–present audited — the era's record lives in images, not prose

Answering "what about 2010 to present?" — measured, and it changes the diagnosis.

**Coverage 2010–2026:** 3,763 posts, 93 ingested (2.5%), 1,194 in `timeline.parquet`, **2,441
untouched**, of which only **303 carry ≥250 words of prose**. So unlike 2005–2009, the modern
gap is *not* unread essays.

**The real finding: from ~2014 the blog's information migrates out of text into the published
images, and our text-parsing pipeline degrades in lockstep.** Untouched-post median word counts
by era: 2010–2013 → 55; 2014–2017 → 23; 2018–2021 → **10**; 2022–2026 → 37 (with mean charts per
post *rising* to 1.7). Meanwhile `ww timeline` — a text parser — captures 113/199 posts in 2010
but only 24–35/year by 2020+, and **866 of its 1,811 rows have no extracted GMI value**. Sixty
2020+ timeline rows have no parsed GMI while carrying a perfectly legible `GMI<date>` table
image. The prose shrank to captions; the table kept publishing the full panel daily.

**Worked proof, and a track-record entry from it:** the 2020-02-14 table — five days before the
COVID top — was a parser miss. Read directly: **GMI 6/6, GMI2 7/8, day count U-86, T2108 53%
(+5), MACD breadth 82% (+19)**. Every instrument at maximum five days before the top — the same
"trend-followers don't call tops" pattern as October 2007, now documented with a dated snapshot
at both ends. `track-record.md` gains the section; `gmi.md` gains "The modern era is an image
problem," which reframes the ~2,547 `gmi*` images as *the primary daily record* for the modern
era rather than illustrations. Future timeline work should read them, not the captions.

**Also ingested — 2 of the 303 modern prose posts, both closing named gaps:**

- **2015-08-30 (flash crash)** — 2015's first timeline section (the year had zero). From 100%
  cash; severity judged by comparison against October 2014's analogous GMI=0 episode; the
  pension trade-off in one sentence: "**I would rather miss a further 5-10% rise than sit
  through a possible 20-40% decline**"; the Boomer-supply thesis (retracement toward break-even
  triggers selling).
- **2014-05-26 (Stage Analysis tutorial)** — timeframe as a *life* choice ("the equivalent of
  flying with the Blue Angels... only part-time"); the pension rule as a pundit filter;
  "**a healthy market rises and consolidates over and over again**"; IBD calling a correction
  while his GMI had been on Buy for a month.

Touched: `methodology/gmi.md`, `history/track-record.md`, `methodology/risk-and-cash.md`,
`methodology/trading-philosophy.md`, `methodology/moving-average-rules.md`,
`history/timeline.md` (Aug 2015 + May 2014 sections), `index.md`; 2 new `sources/` pages.
`ww lint .` clean; 194 tests pass; ledger exported (123 rows).

**Standing queues after this entry:** 2005–2006 block (170 prose posts remaining), 301 modern
prose posts, 90 favorites, 2008, and now the image-first work item: read the `gmi*` tables
into a structured series to replace the degraded text-parsed timeline for 2014+.

## [2026-08-12] ingest | 2005 essays + 2008 opened — 4 posts, tier=teaching

Working the queues from the coverage audit: two from the 2005–2006 essay block (including the
corpus's longest untouched post) and the first two prose posts from **2008**, the worst
year-hole, which his own curation would never surface (zero favorites in it).

**2005-05-13 "This Schizoid Market" (1,909w, longest untouched post):** rotation detected by
comparing the *share of components rising* across indexes on the same day; the Weekly QQQQ
Index quantified as "a major uptrend... that typically lasts **months, not days**"; the fullest
MoneyStream explanation in the corpus; and a pilot buy priced to the cent including the
buy-stop alternative's extra cost. Also a self-aware caveat: new-high-based breadth *lags a
rotation by construction*.

**2005-05-18 "Livermore on profits, Cramer on sleepers":** the **track-money principle** —
Livermore's racetrack story; risk profits freely, "risking your capital, however, was suicide";
fear is not a valid reason to sell, only a technical signal is. The anti-sleeper argument. And
the first fully-specified rocket scan: 4,000 → 371 new highs → EPS ≥100% → doubled → near ATH →
15 survivors, with a PEG-style market-temperature observation.

**2008-01-14 "Darvas on staying clear of bear markets":** 2008's first prose ingest. The blog's
origin story in his own words ("It is because I was angry at how these mental midgets misled
the public in the 2000-2002 debacle that I began this blog"), and Darvas's 1977 bear doctrine —
"I prefer to **sleep soundly at night**, even if it means going into cash for long periods."

**2008-04-21 "My GMI catches trend changes again!":** the richest live snapshot of the
four-composite dashboard — GMI 5, GMI-R 9, **GMI-S 100%, GMI-L 50%** in the April 2008 bear
rally, with the slow half correctly refusing to confirm. **The 2000 pension exit priced for the
only time in the corpus: out ~$103, the fund in the 30s by 2002.** Plus the
pension-until-GMI-6 re-entry bar (stricter than the ≥4 trading threshold) and the
**tax-deferred precondition** — the in-and-out style works because round trips are untaxed, a
structural fact the wiki had nowhere.

Touched: `history/track-record.md` (2000 exit priced), `methodology/risk-and-cash.md` (Darvas
doctrine, tax-deferred precondition), `methodology/gmi.md` (dashboard-in-live-use section),
`methodology/glossary.md` (MoneyStream entry), `history/timeline.md` (3 new sections),
`index.md`; 4 new `sources/` pages. `ww lint .` clean; 194 tests pass; ledger 127 rows.

Queues: 2005–2006 block 168 remaining; 2008 has 39 more ≥250w prose posts; favorites 90.

## [2026-08-12] ingest | 2008 crisis weeks — 3 posts, tier=teaching

The capitulation and retest, from the posts written those weeks. 2008 now has 6 prose source
pages (was 1 this morning).

- **2008-10-13** — the record breadth extreme: 2008-10-10 saw **2,832 of 4,000 stocks at new
  lows** (blog record) with **T2108 at 1%** — a direct calibration point for `ww breadth
  validate`. Discipline at maximum stress ("No one knows when this down-trend will end"), the
  Cramer receipt, and the education mission at its most explicit.
- **2008-10-22** — **duration base rates computed live**: Day 36 against the year's own 55- and
  39-day down-trends → "we may have a ways to go." The earliest working form of the 2019
  published duration statistics. Watch-list doctrine with a numeric trigger; "stocks that can
  survive this market near their all-time highs are potential rockets."
- **2008-11-21** — **the retest read via breadth**: November's low made 2,185 new lows against
  October's 2,832 — positive divergence noted, bottom call refused (the *yearly* Dow chart vs
  1929–32 said not near a bottom). Also a T2108 threshold-evolution datapoint — it "used to be"
  reliable at 70/20 — now recorded in `t2108.md`'s Evolution section, completing the
  70/20 → 80/25–30 → <10% history. Baruch surfaces in the lineage.

Touched: `methodology/t2108.md` (extreme-lows table + threshold evolution),
`history/track-record.md` (capitulation + retest inside the 2008 account),
`methodology/qqq-short-term-timing.md` (duration base rates), `history/timeline.md`
(Oct–Nov 2008 section), `index.md`; 3 new `sources/` pages. `ww lint .` clean; 194 tests pass;
ledger 130 rows.

## [2026-08-12] ingest | three teaching favorites — screener, ATH watchlist, GLB mechanics

Continuing the "My Favorite Posts" queue with the three strongest remaining how-to titles.
87 favorites remain un-ingested.

- **2018-04-01 "How I track stocks at all time highs"** — the construction of the ~800-stock
  ATH watchlist several scans run against. Notable: **he identifies a survivorship trap in his
  own tooling** — TC2000 filters return null for stocks that didn't exist over the lookback,
  silently dropping recent IPOs — and engineers around it via barchart.com → Excel → TC2000.
  Green lines then drawn **by hand** on monthly charts, corroborating the comment-thread
  finding from a post. Red-signal buying allowed only with "a very close stop loss."
- **2020-10-04 "How I used the IBD screener"** — the four-criterion screen verbatim (RS 90-99,
  ACC/DIS A/B, >$30, next-Q EPS est >100% → 36 of 7,000+), the Excel→TC2000 pipeline, the
  O'Neil origin credit ("I began to make money in the market after reading it"), and a hard
  total-exit line: QQQ below **all 12 GMMA averages** = "time to exit all positions," stated
  with the price. Tutorial video by his own student Richard Moglen — the student channel again.
- **2023-01-16 "How I trade a GLB"** — the ACLX case that *justifies* the close-below rule:
  the day after its GLB it traded below the line intraday but closed above, "that is why I sell
  a GLB only if the stock *closes* a day back below." OSB taught as the standard alternative
  entry six months before the CAVA doctrine post; TQQQ accumulation tiered by GMI score
  (start at Green, conviction at 6).

Touched: `methodology/stock-selection.md` (ATH pipeline + IBD screener sections),
`methodology/green-line-breakouts.md` (close-below case; manual-drawing corroboration),
`methodology/moving-average-rules.md` (all-12-GMMA exit), `history/timeline.md` (3 sections),
`index.md`; 3 new `sources/` pages. `ww lint .` clean; 194 tests pass; ledger 133 rows.

## [2026-08-12] ingest | four favorites — the timing evidence, the top template, the cycle layer, the first ETF study

Continuing "My Favorite Posts" (83 remain). Four posts that each add a missing structural layer.

- **2009-06-07** — the **earliest** ultra-ETF-vs-stock-picking study (the wiki had only the 2011
  and 2013 versions): off the March 2009 bottom, QLD +99.2% and TYH +179.4% vs QQQQ +42.9%,
  with the 3X matching the *best stock in the index*. The needle-vs-haystack framing originates
  here, and the staged pension re-entry runs alongside with never-average-down applied at
  account level.
- **2010-12-13** — the **cycle layer**: monthly Dow, 5/30-month averages plus a 25.4.4 monthly
  stochastic, validated by eye back to 1915. Bottoms with the stochastic <50 (severe ~20). And
  the simple-over-complex doctrine at full strength: "the road is littered with the carcasses
  of Ph.D.'s." Filed into moving-average-rules (completing the daily→weekly→monthly ladder) and
  trading-philosophy.
- **2013-12-09** — the timing thesis **with its evidence published**: the red/green GMI signal
  chart 2006–2013, whipsaws admitted ("but only for a few days"); a link to third-party
  tracking (dark-liquidity's GMI→QLD strategy); and the IBD50 **downside test**, run because an
  honors student challenged the earlier study — more big gainers, no more big decliners.
- **2014-06-08** — the **monthly GMMA top template** (SPY 2000-01 and 2007-08) and the sentence
  the whole exit-latency defence rests on: "**Market tops take months to develop, leaving
  plenty of time for the watchful investor to exit the market.**" This is the doctrinal
  counterpart to the Oct-2007/Feb-2020 instrument-panel snapshots in track-record.

Touched: `methodology/moving-average-rules.md` (monthly layer section),
`methodology/gmi.md` (published signal record + third-party tracking),
`methodology/stock-selection.md` (IBD50 downside test), `methodology/risk-and-cash.md`
(earliest ETF study), `methodology/trading-philosophy.md` (simple-beats-clever),
`history/timeline.md` (4 sections), `index.md`; 4 new `sources/` pages.
`ww lint .` clean; 194 tests pass; ledger 137 rows.

## [2026-08-12] ingest | exits and scans — 4 posts, tier=teaching

- **2005-06-08** — protective puts **back-dated to 2005** (the wiki had 2009 as the origin),
  with the decision rule the later post lacks: a put beats a stop **when shakeout risk is
  high**; strike = the would-be stop, expiry past the window that matters.
- **2011-08-15** — the complete August 2011 exit, both drivers admitted ("I just got tired of
  worrying" *and* the rules); banks breaking 2010 support read against the 2008 template;
  component shares below the 30-week (83/87/81%); "I do not own *any* stock that is below its
  30 week average"; and the addiction line: "**If one cannot exit the market to go to cash, one
  should not be in the market at all.**"
- **2015-07-26** — the **warning four weeks before the flash crash**, completing 2015's
  warning→aftermath pair: narrow leadership ("QQQ looked strong because of a few big name
  stocks, but most stocks were breaking down"), Stage IV spreading, a failed 30-week retake as
  the tell, SQQQ and a China put already on.
- **2016-11-27** — a scan the catalogue lacked: weekly consolidation-breakouts (4 of ~4,900),
  plus a concept the wiki had nowhere — **short interest read as breakout fuel** ("the higher
  the number, the greater the buying pressure"), now a glossary entry.

Touched: `methodology/risk-and-cash.md` (3 new sections), `methodology/stock-selection.md`
(weekly consolidation scan), `methodology/glossary.md` (short interest ratio),
`history/timeline.md` (4 sections), `index.md`; 4 new `sources/` pages.
`ww lint .` clean; 194 tests pass; ledger 141 rows. Favorites remaining: 81.

## [2026-08-12] ingest | the shaken-out rule and its enforcement — 4 posts, tier=teaching

Closes the "how I avoid getting shaken out" gap named in review #1, and completes the
weekly-first exit doctrine across three posts written over seven years.

- **2019-03-15** — the rule itself: **buy on daily set-ups, sell only off the weekly.** "Look at
  the stock's weekly chart before every sale... if the stock is still holding its rising 10 week
  average, do not sell." COUP as the hard test: two of his own daily sell signals fired; the
  weekly said hold; he held.
- **2020-09-20** — the enforcement ("**I have created a note on my monitor** that says I must
  look at the weekly chart before I sell") plus a scan the catalogue lacked, with **verbatim
  TC2000 syntax**: `H=maxH50; H>2*H50 or H>1.5*MinL50; V>1.3*AvgV50; C>20` → 74 of 5,096.
  Machine screen, hand-drawn green line afterwards — consistent everywhere now.
- **2013-10-13** — the AAII talk: "**sell down to the sleeping point**"; the failed-GLB logic
  inverted into a sell-side warning (a stock that *builds a new green line* is a candidate to
  leave), worked on GLD's Stage 3→4; the SPY-plus-stages simplification; and a dated link into
  the off-blog corpus (the December 2012 Worden webinar).
- **2011-09-19** — the behaviorist epistemics in one line ("concentrate on their behavior rather
  than their words — the same goes for the markets"); adviser-sentiment inversion as re-entry
  evidence, distinguished from the 2007 bounce-only case; and the **point-move arithmetic priced
  through an option**: "a 17 point move on one call option = $1,700."

Also: `exits.md` now reconciles the fast daily-RWB exit with the slow weekly-first rule as two
tools for two risks (give-back vs shakeout).

Touched: `playbooks/exits.md`, `methodology/stock-selection.md` (doubler scan + point-move),
`methodology/risk-and-cash.md` (sleeping point; 2011 sentiment case),
`methodology/green-line-breakouts.md` (sell-side inversion), `history/timeline.md` (4 sections),
`index.md`; 4 new `sources/` pages. `ww lint .` clean; 194 tests pass; ledger 145 rows.

## [2026-08-12] ingest | order doctrine, signal audits, the yellowband scan — 4 posts, tier=teaching

- **2005-05-26** — order-type doctrine the wiki had nowhere: "**BUY AND SELL AT THE MARKET!**"
  (limit orders risk missing the exit entirely), and re-entry engineered as a **resting
  buy-stop** — the ORCT order triggered at the breakout "without my having to pay any
  attention to it." Plus Peter Lynch's observation method with three personal receipts.
- **2011-01-31** — a five-part **warning stack** published while headline indicators read
  strong: 19.1% bearish advisers (the *inverse* of the re-entry read — sentiment cuts both
  ways and both directions are now documented), sudden selling in leaders, **AAPL/GOOG failing
  to make new highs on great earnings**, the muni worry, the calendar lull. The Zweig
  rate-hike template applied abroad with price noticed before the explanation: "the bad news
  usually comes out long after a stock has peaked."
- **2016-02-07** — a **per-signal audit** of the Dec 2015 Sell: 78–92% of component stocks
  down, circularity acknowledged; the anguish framing ("if I get back in lower or even equal to
  where I exited, I did well enough"); and **cash over short** as the age-based bear default.
- **2017-09-17** — the **yellowband scan** (criteria + purple-dot convention), further
  confirming yellowband as a live 2017 framework; and the **TC2000 club** as a named off-blog
  distribution channel for his actual scan files.

Touched: `playbooks/exits.md` (order types + resting buy-stop), `methodology/gmi.md`
(per-signal audit), `methodology/risk-and-cash.md` (warning stack; cash-over-short),
`methodology/glossary.md` (yellowband scan, purple dots), `history/timeline.md` (4 sections),
`index.md`; 4 new `sources/` pages. `ww lint .` clean; 194 tests pass; ledger 149 rows.
Favorites remaining: ~74.

## [2026-08-12] ingest | the hourly layer, the FTD disagreement, the orthodox agnostic — 4 posts

Two more named gaps from the reviews closed.

- **2022-08-07** — the **hourly GMMA**, the timeframe flagged as undocumented in review #1. Also
  recovers a construction detail no page had: his adapted Guppy carries a **13th "average" equal
  to 1 that plots price itself** — the dotted line that should lead in an up-trend — and
  red-line convergence reads as a base at any timescale. The ladder is complete:
  hourly → daily → weekly → monthly, each with a distinct job.
- **2010-06-04** — the **follow-through-day disagreement worked in real time** (review #2 flagged
  his FTD scepticism): IBD confirmed an up-trend, his instruments said Day 21 down, he stayed in
  cash — and was right; the July 2010 pension exit followed. "Preparation without participation":
  mining thin new-high lists for the next leaders while unconvinced.
- **2005-05-30** — the **orthodox agnostic** ("if there are good reasons, they almost always come
  out after the move... just jump on board"), the fullest **window-dressing** explanation in the
  corpus (131 mentions, previously unexplained; Bogle's denial noted; an SEC disclosure fix
  proposed), the Successful 10-Day read as a *ratio* nine years before the formal rule change,
  and the MW plan with the **re-entry condition pre-written at entry**.
- **2012-05-07** — the 30-day close rule endorsed at full strength; the AAPL
  good-news-no-rise tell repeated; a rare GMI-above-4-inside-a-down-trend divergence; and the
  **new-money-vs-old-money** distinction — pension contributions keep buying funds on the way
  down while the balance sits in cash, "I never do so with individual stocks, because a company
  could go bankrupt (GM, Enron, Lehman)." DCA is acceptable exactly where bankruptcy is
  impossible.

Touched: `methodology/moving-average-rules.md` (hourly layer; 30-day rule),
`methodology/risk-and-cash.md` (FTD worked; new-vs-old money), `methodology/glossary.md`
(window dressing), `methodology/trading-philosophy.md` (the orthodox agnostic),
`history/timeline.md` (4 sections), `index.md`; 4 new `sources/` pages.
`ww lint .` clean; 194 tests pass; ledger 153 rows.

## [2026-08-12] ingest | the AOL epiphany, the kiss-of-death study, the pilot portfolio — 4 posts

- **2008-01-02** — **the origin story of the market gate.** The 1990s AOL observation ("even
  the strongest stocks did poorly when the market went into a down-trend") replicated
  quantitatively on ISRG: 2007's best Nasdaq stock earned ~69% of its tripling inside the two
  major up-trends and fell 22% from top inside one down-trend. The 70%-correlation doctrine,
  the GMI gate and Proposition 3 all trace here. Also a second self-published GMI limitation:
  its **QQQ-centricity** "masking the deterioration in the Dow and S&P 500" — named in January
  2008, of all months.
- **2008-05-05** — the **kiss-of-death study**: twelve months of his own monthly IBD100
  snapshots. Two-sided verdict — a leader-finder, not a portfolio; new-high concentration
  dominates the indexes; the year-old list's tail ran +50–315%; sector concentration is the
  failure mode. Completes the IBD-audit series (2007 → 2008 → 2011 → 2013).
- **2014-10-05** — the **pilot portfolio**: up-to-25-share radar positions across 11 biotech
  GLB candidates inside a down-trend — "ownership as attention," winners self-select. The
  biotech exemption stated; AMGN's monthly chart carries both a successful and a failed GLB.
- **2017-07-23** — the **triple-support bounce scan** (the post that surfaced in the coverage
  audit's random sample and proved the untouched bucket held methodology): three daily support
  indicators bounced at once, 8 of 4,800; the PETS confluence stack; the earnings-collar idea.

2008 now has 8 prose source pages (had 1 yesterday morning).

Touched: `methodology/trading-philosophy.md` (AOL epiphany), `methodology/gmi.md`
(QQQ-centricity), `methodology/stock-selection.md` (kiss-of-death; pilot portfolio;
triple-support scan), `history/timeline.md` (4 sections), `index.md`; 4 new `sources/` pages.
`ww lint .` clean; 194 tests pass; ledger 157 rows.

## [2026-08-18] lint | front-matter enforcement — 20 `sources:`↔`## Sources` drifts synced (timeline ×12, trend-flip-log ×4, exits, backtest-timing-overlay, sources/2015-07-26, sources/2021-08-11); `ww lint` now requires title/type/updated(ISO)/sources and two-way agreement; test fixtures updated

## [2026-08-18] note | CLAUDE.md §4 ingest step 3 rewritten: one canonical page per fact, pointers elsewhere, playbooks hold procedure only (~1,200-word budget). Motivation: the audit found the GMI signal rules restated on 5 pages, which is how the "two consecutive ≤3" fabrication and the "one quarter" drift propagated. §4 Lint updated to list the new mechanical checks.

## [2026-08-18] query | what is the step-by-step OSB entry procedure? — filed: playbooks/buying-osb.md (14 sources; black/green/blue dot triggers tabulated; chains onto buying-glb.md); linked from overview, index, oversold-bounce.md, buying-glb.md

## [2026-08-18] note | exits.md reconciled — the three trailing systems (2016 weekly ladder, 2017 daily RWB, 2024 green bars) plus the 2019 weekly-first veto laid out as one dated evolution in a new "Which trailing system when" section; the page's earlier "daily RWB is primary post-2017" claim corrected to "primary Dec 2017–early 2019, reversed on the sell side March 2019"; same correction propagated to sources/2017-12-17 and the timeline's 2017 entry; Step 4's GMI≤3 line now quotes 2011-03-07 verbatim and points at gmi.md#signals

## [2026-08-18] note | market-state.md rebuilt as a complete procedure (5→17 sources): adds the account split (2011 IRA rule + 2015 pension demotion of GMI Sells), the TQQQ default and Day-1 tactic, the 5-day down-trend confirmation, the GMI-Buy-vs-long-QQQ-down-trend warning (2014-04-27), T2108's two bands with the 2022 SPY method, and the staged pension exit; every rule one line + citation + pointer to its canonical page. Playbook thickening (T3) complete — buying-glb.md left as is (already procedure-complete at 1,458 words).

## [2026-08-18] note | structural split — gmi.md → gmi.md (3.5k words: components, signals, usage, code) + methodology/gmi-family.md (GMI-S/L/R/2 + the rest of the table) + methodology/gmi-evidence.md (verbatim table labels, 2005 track-record chart, 2013 signal record, 2016 audit, image problem); risk-and-cash.md → risk-and-cash.md (3.2k: trading-account doctrine) + methodology/pension-management.md + methodology/short-side.md + methodology/leveraged-etf-default.md + history/defensive-episodes.md (six case studies); stock-selection.md → stock-selection.md (3.6k: philosophy, fundamentals, price level, watchlist) + methodology/scans.md (nine published scan definitions) + methodology/entry-signals.md (BOS, dots, x8/x21/30, with a lineage note). Sections moved verbatim by heading; each side's front-matter `sources:` and `## Sources` recomputed from the citations it retains; anchors repointed in market-state, exits, track-record, buying-osb; index.md and overview.md updated.

## [2026-08-18] note | history/timeline.md sorted chronologically — 128 sections, 20 repositioned (e.g. "May 2005 (order doctrine)" and "(epistemics)" had sat after June 2005; "June 2009 ultra-ETF" after November 2009; "August 2011 (cont.)" before "August 2011"; "November 2018" before "April 2018"; "April 2019" before "March 2019"; "August 2022" before "May 2022"). Sort key = first month/year in the heading; "(cont.)" sorts after its base; the O'Neil 1995-diary entry sorts by its 2016 post date.

## [2026-08-18] note | glossary alphabetised (was roughly grouped, e.g. Bollinger Band first, RLC last, MACD breadth between GMI table and GMI-L) and seven entries added from their canonical pages: 2-for-1 method, already doubled, doubler, follow-through day, gap rule, sleeping point, topping-pattern scan.

## [2026-08-18] note | GLB stop reconciled — buying-glb.md Step 5 now states both rules with their sources: the general 2010 rule (decide the level before buying, place a GTC stop-loss order on fill — [WW 2010-03-15]) and the 2021 GLB-specific override (no resting order for a GLB; the same level is a mental stop evaluated on the close, to avoid intraday probes of the green line — [WW 2021-01-24], [WW 2018-05-20]). exits.md Step 1 cross-references the exception. Previously the playbook said "GTC" in Step 5 and "mental stop" in Step 6 without connecting them.

## [2026-08-18] note | page-level meta-commentary retired — the wiki's habit of writing "an earlier version of this page said X" / "the wiki lacked Y" into methodology text has been removed from 12 passages (glossary yellowband, gmi component 6 + Sell-rule aside, gmi-evidence image-problem intro, gmi-family GMI-S/GMI-L, moving-average-rules GMMA rung, pension-management ×2, reader-qa, short-side puts, t2108 two bands, timeline ×4); each now states the fact and its date. The corrections themselves are already recorded in this log (2026-08-12 entries). Going forward: facts on pages, corrections in log.md.

## [2026-08-18] ingest | 2015-01-25 Fly by my gut or follow my instruments? — tier=teaching; touched: methodology/trading-psychology (new), history/timeline
## [2026-08-18] ingest | 2015-02-16 GMMA charts show no market top in sight — tier=teaching; touched: moving-average-rules (GMMA top signature), pension-management (Feb 2015 re-entry), trading-psychology, timeline
## [2026-08-18] ingest | 2015-03-01 On my use of the GMI; Darvas RWB rocket AMBA — tier=teaching; touched: pension-management (the 30-week pension rule and the 2014 breach, in his words), trading-psychology, scans (Darvas EasyScan), timeline
## [2026-08-18] ingest | 2015-07-19 Buying climax in the QQQ? — tier=teaching; touched: risk-and-cash (breadth divergence, 2015 read), timeline
## [2026-08-18] ingest | 2015-09-08 Market trend clearly down; diminished trust in ETFs after the flash crash — tier=teaching; touched: risk-and-cash (flash-crash caveat on resting stops), pension-management (new money DCA; Sept 2015 state), timeline
## [2026-08-18] ingest | 2015-09-13 Taking stock: technical indicators at extreme levels; INGN — tier=teaching; touched: t2108 (2015 single digits + II + put/call), stock-selection (leaders in weak tapes), timeline
## [2026-08-18] ingest | 2019-02-10 Green dot signal: LULU — tier=trade_example; touched: entry-signals (green dot in practice), oversold-bounce (2019 evolution row), timeline
## [2026-08-18] ingest | 2019-03-24 Inverted yield curve or Mueller report? Stage 4 decline? — tier=teaching; touched: moving-average-rules (declining 30-week under a GREEN GMI; curve-up re-entry rule), timeline
## [2026-08-18] ingest | 2019-03-29 Buying IPOs with a recent GLB: SAFE YETI TWLO — tier=teaching; touched: green-line-breakouts (IPO window; close-below/repurchase-above), timeline
## [2026-08-18] ingest | 2019-06-02 Shorting stocks at new lows beats buying stocks at new highs — tier=teaching; touched: gmi (successful-10-day-new-low mirror), short-side, t2108, glossary (new term), trading-psychology, timeline
## [2026-08-18] ingest | 2019-07-14 DC AAII meeting; riding SPY and TQQQ — tier=teaching; touched: leveraged-etf-default, trading-psychology, timeline
## [2026-08-18] ingest | 2019-11-24 Why I sold INMD at $57 — tier=trade_example; touched: trading-psychology (the too-easy sell), exits (discretionary parabolic exit pointer), timeline

## [2026-08-18] query | what are the rules he uses to manage his own psychology? — filed: methodology/trading-psychology.md (8 rules, 11 sources; closes the "trading psychology" gap). 2015 and 2019 now have 7 source pages each (were 1 each).

## [2026-08-18] query | does he have a position-sizing rule? — answer: no, by his own account ("I have no specific rules for that", comment 2014-05-31; "I go in in phases", 2012-11-13; reading list Weinstein/O'Neil/Lefèvre/Covel, 2011-01-06). Filed as risk-and-cash.md#position-sizing (the stand-in habits: pilot buy → add to winners, wade in, 2-for-1, sleeping point, "manage the risk with stops and position size") and reader-qa.md. Closes the position-sizing gap.
## [2026-08-18] ingest | 2022-06-26 69% of Nasdaq-100 in hourly RWB up-trends; RS-at-50-week-high scan; LLY — tier=teaching; touched: moving-average-rules (hourly layer), scans (new scan), timeline
## [2026-08-18] ingest | 2022-08-01 MACD hourly histograms reveal weakening — tier=teaching; touched: moving-average-rules (hourly layer), timeline
## [2026-08-18] ingest | 2022-07-12 Day 1 of new QQQ down-trend; hourly GMMA looks weak — tier=daily_update (cited inline, no summary page); touched: moving-average-rules, timeline. Closes the hourly-GMMA gap.

## [2026-08-18] ingest | 2009-05-31 Rally gaining strength; Guppy chart reveals major turn — tier=teaching; touched: moving-average-rules (the first weekly Guppy chart, May 2009; "rely on the weekly"), t2108, trading-psychology, timeline
## [2026-08-18] ingest | 2010-06-21 Stocks near ATH; IBD100 3× more likely to rise 10%+ — tier=teaching; touched: stock-selection (2010 IBD100 check), scans (new-high + EPS≥50%), gmi (the "?" grade), t2108 (pendulum), trading-psychology, timeline
## [2026-08-18] ingest | 2010-06-28 I only ride the yellow band trends — tier=teaching; touched: moving-average-rules (yellow band on the index), risk-and-cash (many small losses), short-side, timeline
## [2026-08-18] ingest | 2010-12-06 IBD gives up on the FTD; mutual funds restrict timing; IBD100 top-10 — tier=teaching; touched: pension-management (the constraint from the post itself), stock-selection, timeline
## [2026-08-18] ingest | 2013-03-17 More GLB stocks; pilot buy; Dow Theory buy signal — tier=teaching; touched: green-line-breakouts (2013 statement; index GLBs), timeline
## [2026-08-18] ingest | 2014-06-22 RWB patterns in QQQ across four timeframes — tier=teaching; touched: moving-average-rules (the ladder and each layer's role, first stated), green-line-breakouts (IPO precursor), timeline
## [2026-08-18] ingest | 2016-10-25 Back from Minervini's Master Trader Program — tier=teaching; touched: trading-philosophy (the lineage he names), timeline
## [2026-08-18] ingest | 2016-12-11 New TC2000 scan for bounces: CELG — tier=teaching; touched: scans (full spec), entry-signals (the green dot's dated ancestor: BOS 2016-06 → bounce scan 2016-12 → green dot 2018-03), timeline

## [2026-08-18] ingest | 2006-01-03 Happy New Year — What if?; trade with the trend — tier=teaching; touched: trading-philosophy (the 2006 credo), timeline
## [2026-08-18] ingest | 2006-06-12 GMI 0; 185 submarines, 8 rockets; brainwashed against shorting — tier=teaching; touched: short-side, pension-management (the chicken's record), timeline
## [2026-08-18] ingest | 2008-01-22 GMI 0; 12th day of down-trend; sucker rally near?; IBD100 holds winners — tier=teaching; touched: moving-average-rules (10-week odds; +10% rally requirement), t2108 (19%), stock-selection (IBD100 as starting universe; resisters watchlist), timeline
## [2026-08-18] ingest | 2009-03-01 No bottom in sight — how bear markets end — tier=teaching; touched: risk-and-cash (new section: the volume signature), trading-philosophy (the truck), timeline
## [2026-08-18] ingest | 2011-01-24 Still cautious; the muni-bond thesis; IBM — tier=teaching; touched: short-side (thesis-driven hedge under GREEN GMI), gmi (indicators confirm after the fact), t2108 (2011 bands), moving-average-rules (20 weeks above the 10-week), timeline
## [2026-08-18] ingest | 2011-06-20 No one knows when this market will bottom — tier=teaching; touched: pension-management (2011 best-days rebuttal), moving-average-rules (weekly 10.4.4 stochastic as relative-oversold gauge), timeline
## [2026-08-18] ingest | 2011-11-28 GMI performance since April; the two-day confirmation rule adopted — tier=teaching; touched: gmi (signals table: origin row), gmi-evidence (the first self-audit), market-state (origin note), timeline. **Corrects the wiki's dating of the two-day rule from 2012-04-30 (first stated as "my criterion") to 2011-11-28 (adopted) / 2011-12-01 (first signal under it).**
## [2026-08-18] ingest | 2011-12-05 GMI signal #13; the "major innovation" — enter oversold in a Stage 2 up-trend — tier=teaching; touched: oversold-bounce (the doctrine dated to December 2011, five years before BOS; evolution row), entry-signals (lineage now starts 2011-12), gmi, timeline
## [2026-08-18] ingest | 2014-04-20 Guppy charts show relative weakness in QQQ vs SPY — tier=teaching; touched: moving-average-rules (the periods stated 2014; split-market read), risk-and-cash (leaders decimated as a warning), timeline

## [2026-08-18] ingest | 2006-08-07 GMI +3; QQQQ masks underlying strength in IBD-100 — tier=teaching; touched: gmi (the new-low mirror statistic re-dated from 2019 to 2006), gmi-family (MACD breadth as "my earliest indicator", 2006), glossary, timeline
## [2026-08-18] ingest | 2006-08-14 Cramer contrary indicator; IBD 100 Index rigged? — tier=teaching; touched: moving-average-rules (30-week defensive rule, 2006), stock-selection (IBD survivorship, 2006 origin), trading-psychology, timeline
## [2026-08-18] ingest | 2007-02-26 GMI 6; GMI-S 88; Dow climbs wall of worry — tier=teaching; touched: green-line-breakouts (2007 index precursor: overhead supply on the Dow's base; O'Neil's 8% rule), gmi-family + pension-management (GMI-L as the pension's stay-invested condition), timeline
## [2026-08-18] ingest | 2008-04-07 GMI 3; 9th day of QQQQ up-trend; QLD; URBN — tier=teaching; touched: gmi (why component 1 has a minimum count), moving-average-rules (rising 10-week; 2:1 odds), green-line-breakouts (URBN/FDG precursors), trading-philosophy (the truck, first telling), timeline
## [2026-08-18] ingest | 2009-04-11 The dirty little secret about the up-tick rule — tier=teaching; touched: short-side (mechanics; short interest as latent buying), timeline
## [2026-08-18] ingest | 2010-09-07 This rally may have legs; IBD100 top ten out-shine — tier=teaching; touched: stock-selection (the strategy sentence; top-10 check), risk-and-cash (Investors Intelligence), moving-average-rules, timeline
## [2026-08-18] ingest | 2012-04-16 Thoughts about the Worden DC seminar — tier=teaching; touched: gmi + market-state (**Sell rule "2 consecutive days below 3" re-dated to April 2012** from 2014-08-03), pension-management (the 2012 two-speed statement), short-side (weekly covered calls), trading-philosophy (no rules → index ETFs), timeline
## [2026-08-18] ingest | 2016-11-13 QQQ down-trend but GMI Green; 16 GLB stocks; OLLI — tier=teaching; touched: green-line-breakouts (the pre-defined exit in his words), trading-psychology (don't marry a stock), timeline

## [2026-08-18] ingest | 13 posts (2006-01-23, 2006-08-21, 2009-02-15, 2010-02-01, 2010-05-17, 2010-07-12, 2011-01-18, 2011-02-14, 2011-02-23, 2013-04-14, 2013-09-08, 2014-04-13, 2014-10-26) — all tier=teaching; the last of the non-2005 long_form queue. Touched: gmi (confirms-not-predicts 2006; "?" grade 2006; ≥4 to commit money), gmi-evidence (the 2008 record in numbers), gmi-family (GMI-S vs GMI-L read together), risk-and-cash (caution triggers 2011; leader tell 2006; contrarian trio 2010; put/call 1.2), market-state (the both-trends rule), t2108 (30/20 in 2010; pendulum 2011; 41% not a bottom 2014), moving-average-rules (30-week close → turn-down sequence 2014; retake 2014; daily Guppy 2010; BWR ≈ submarine 2011), pension-management (May 2010 and April 2014 triggers), leveraged-etf-default (2011 arithmetic; Day-1 nibble / Day-5 accumulate 2014), entry-signals (2011 IBD 50 bounce scan), green-line-breakouts (Livermore 1940 root; index GLBs and the failed-GLB rule; consolidation in weak markets), stock-selection (IBD100 turnover), defensive-episodes (the muni alarm opens the Jan 2011 stack), trading-philosophy (react don't anticipate; market usually right; reaction to news), trading-psychology (one eye on the exits; the animal taxonomy), timeline (+12 sections). Non-2005 long_form queue is now empty; 36 posts from 2005 remain.

## [2026-08-18] ingest | 2005 long_form remainder — 36 posts (2005-04-18 → 2005-12-11): 17 tier=teaching with source pages (04-18, 05-01, 05-03, 05-05, 05-07, 05-22, 05-23, 06-02, 06-13, 06-14, 06-26, 07-02, 07-11, 07-28, 08-17, 09-11, 12-11), 19 tier=daily_update (summaries on the row, cited inline where used: 05-12, 05-31, 06-01, 06-07, 06-11). Touched: gmi (**component 1 redefined 2005-07-11 from a count >100 to 'count ≥ 100 OR ≥ 50%' — the origin of the percentage rule**; first positive count 2005-06-02; strict-rules reflex 2005; new-high vs new-low success May 2005), gmi-evidence (the first performance charts, June–July 2005), gmi-family (the 2005 breadth rows: % above 10-week, % in short-term up-trend, the doubler indicator), qqq-short-term-timing (the 10-day line in 2005; the 92-day precedent), leveraged-etf-default ("why mess around with individual stocks…", July 2005), pension-management (May 2005 re-entry; June 26 2005 first pension exit), risk-and-cash (the 70% rule's first appearances incl. the letter to Cramer; Loeb's pyramid as the pilot buy's root), stock-selection (buy-stop entry on BTU), short-side (2005 case; D-6 odds), trading-philosophy (Darvas's one reason; the freight train; the truck dated to Sept 2005), trading-psychology (instruments-over-gut dated to May 2005; Appel's streak trap; GOOG parabolic 2005), glossary (doubler indicator origin), timeline (+6 sections). **The long_form queue is now empty** (175/175 ingested); 246 posts ingested in total.

## [2026-08-18] lint | semantic pass after today's 100+ ingests: 0 duplicate paragraphs across methodology/playbooks/history; moving-average-rules.md had grown to 7,228 words (the GMMA material outgrew the single-average rules) → split: methodology/gmma-charts.md (RWB/BWR, daily RWB system, bottom detector, bond-ETF monthly RWB, hourly + monthly layers, all-12 exit line, consolidation; 3,884 words, 27 sources) leaving moving-average-rules.md at 3,682 words; anchors repointed in three source pages. Remaining oversized pages to watch: timeline (25.6k, by design), trend-flip-log (6.3k), green-line-breakouts (5.8k), risk-and-cash (5.0k), glossary (4.8k), gmi (4.6k).

## [2026-08-18] ingest | unknown-queue batch 1 — 10 posts (2013-06-24, 2016-12-04, 2017-03-20, 2018-07-16, 2021-05-31, 2021-07-12, 2022-01-30, 2022-02-08, 2022-10-03, 2025-04-20); 9 teaching + 1 trade_example. Triage method: 1,064 un-ingested `unknown` posts filtered by title hook (how i / why / rules / scan / set-up / explain / confession …) → 52 candidates → read the longest. New material: **the black-dot formula published in full** (2021-07-12) with the claim beneath it ("almost every significant rise in a stock begins from an oversold level. But not every oversold level leads to a big rise"); **the <5%-below-a-recent-ATH TC2000 column scan** with its complete spec (2022-10-03); **the green line's 3-monthly-bar drawing rule and the IPO exception** (2021-05-31); **the weekly RWB hold rule** — hold until the white band disappears, never buy BWR (2018-07-16); **Bollinger 15.2 usage** — the band bounce and the pinch (2022-02-08); **the 30-week curve-up as the definitive re-entry** plus the bottom-watch pair p/c > 1.10 and T2108 < 10% (2022-01-30); **RLC in practice with two stop references** (2017-03-20); **SQQQ as the symmetric mirror of TQQQ on Day 1** (2025-04-20). Also a methodology self-correction: in June 2013 he adopted an anti-whipsaw criterion for the QQQ short-term trend count, missed the start of a decline, and reverted to the original method — so two-day trends are expected output of the rule the wiki documents (2013-06-24). Touched: qqq-short-term-timing (the 2013 experiment; the 2016 ~40% figure), gmma-charts (RLC in practice; the weekly hold rule), green-line-breakouts (drawing rule; IPO exception), entry-signals (black-dot formula; Bollinger bounce/pinch), scans (the new column scan), stock-selection (O'Neil ATH argument; fallen leaders excluded), leveraged-etf-default (SQQQ mirror), moving-average-rules (curve-up definitive), market-state (bottom-watch pair; window-dressing rallies), trading-psychology (wait for the bottom to define itself), glossary (Bollinger bounce/pinch), timeline (+9 sections). Ledger 246 → 256.

## [2026-08-18] ingest | unknown-queue batch 2 — 10 teaching posts (2010-05-24, 2012-09-30, 2014-09-01, 2017-01-22, 2021-04-18, 2021-11-21, 2022-03-06, 2022-08-25, 2024-01-21, 2025-10-15). New: **the Wish-Darvas scan criteria in full** (>$20, near ATH, yellowband 5+ weeks, new high within 25 days, up today, up >80% y/y, bounce off the 21-EMA or 30-SMA); **the submarine scan measured** — 56% of hits down ≥15% vs 17–19% of index components, the only published performance check on one of his scans; **RWBCount** (weekly analogue of RLC) defined; **a declining 30-week stated arithmetically** (this week's close below the close 31 weeks ago) and cap-weighting named as what hid the 2021 decline; **the ATH scan's weekly-RS-vs-SPY-at-a-20-week-high condition**; **Darvas's GTC buy-stop** as the answer to a breakout you cannot watch; **TQQQ beats >95% of stocks measured again** (Jan 2024); the 5-day/10-week bounce scan and the cup-and-handle's three components; the 5-day rule applied to inverse ETFs. **Supersession flagged: the 5-day EMA replaces the 8-day EMA for trailing a rising post-Blue-Dot stock (2025-10-15)** — this is the origin of the "5-day EMA post-GLB exit rule" the wiki already carried from 2026; oversold-bounce evolution table and green-line-breakouts now both point at it. Ledger 256 → 266.

## [2026-08-18] ingest | unknown-queue batch 3 — 12 posts (2005-07-24, 2005-12-29, 2017-02-12, 2021-07-05, 2021-08-22, 2022-09-15, 2022-09-19, 2023-02-12, 2023-06-04, 2025-03-16, 2025-07-27, 2025-10-05); 10 teaching + 2 trade_example. The most important item is **his own critique of setup evidence** (2025-10-05): "anyone can show us collections of *winning* stocks… just buying every Friday could have yielded profits on a steadily rising stock… these collections do not show us the number of times that each setup fails, especially in a declining market!" — now on trading-philosophy.md#your-own-hit-rate-is-an-indicator with a caveat that this wiki's worked examples inherit the same selection bias and that the backtest is its only unselected evidence. Also: **the definition of a set-up** (objective conditions + the stop price they imply + many small losses and a few big winners, 2021-08-22); **the 10-week crossing above the 30-week as the bottom signal** (2022-09-15, with the 2020 instance giving 1.6 years); **the 30-day close rule stated in 2005**; two more scan specs (first-day 100-day high run in the last hour, 2017; 20-week RS + recent ATH + 4-week bounce with the stop at the weekly green bar's low, 2023; the 8-EMA bounce scan, July 2025); TQQQ +23.3% from U-1 beating 94%+ of stocks (2021); price moving before news (PANW/S&P 500, 2023); reading the ATH list hardest when it is shortest (2025); and the 2005 bear trap — "act AFTER the decline has begun." Ledger 266 → 278.

## [2026-08-18] ingest | unknown-queue batch 4 — 8 teaching/trade_example posts with source pages (2010-04-14, 2020-06-09, 2020-07-23, 2022-07-07, 2023-01-25, 2023-03-06, 2024-01-04, 2026-06-01) + 6 thin scan-result posts tiered daily_update. New: **where the green line is actually drawn** — "the top of the highest monthly bar even though the stock retreated from the high that month," not a later lower peak (2022-07-07, from a reader question); **TC2000 GLB alerts set weeks in advance** (the alert on AMD was created June 19 and fired July 22); **"4wk>10wk>30wk averages, my prime pattern for advancing stocks"** stated outright (2023-01-25) and the green bar scan's one-line spec (2023-03-06); the **oldest oversold-bounce scan on the blog** (2010 Worden webinar: oversold stochastic + 30-day bounce/breakout) which pushes the OSB family's lineage back to 2010; the green dot's gate restated — above the last green line top is "a critical requirement" (2020-06-09); QS as an explicit exception to his own horizon (concept held long, short-interest squeeze as fuel, 2024-01-04); and the 2026 restatement of the 30-week signal with the 2000 chart beside it, plus "I got defensive in April 2025 until the 30 week resumed its rise." Ledger 278 → 286.

## [2026-08-18] note | unknown-queue triage exhausted for teaching hooks: of 1,064 un-ingested `unknown` posts, 52 had a teaching hook in the title; 40 are now ingested (34 with source pages, 6 tiered daily_update as thin scan-result posts) and the remaining 12 are one-line scan-result posts of the same kind. **The title-hook seam is worked out.** Next session should either (a) sample the body text rather than titles — many `unknown` posts are daily notes with a paragraph of teaching buried mid-post — or (b) accept that the remaining ~1,000 are daily updates and bulk-tier them, which would make `ww stats` by-tier counts meaningful again.

## [2026-08-18] ingest | unknown-queue batch 5 (body-text seam) — 7 teaching posts found by scanning post *bodies* for teaching markers rather than titles (2005-05-02, 2009-10-19, 2011-03-13, 2014-01-26, 2014-02-09, 2020-03-29, 2020-10-11). This seam works: none of these titles would have passed the hook filter. New: **"the WW-GMI is not a leading indicator… by definition, the index will not register a strong market until after the turn has come"** — the disclaimer one week after launch (2005-05-02); **the mistake the whole bounce doctrine exists to prevent** — "buying a stock when it is too extended from support… all I had to do was to reverse my actions," found by reviewing his own losses, with Bollinger Bands at the **standard 20-day/2-SD setting in 2009**, before his 15.2 (2009-10-19); **the earliest published duration table** — 52 QQQ short-term up-trends since 2006, the ten longest tabulated, five years before the 2019 tabulation (2014-01-26); **the SQQQ→TQQQ turn procedure** — "the key is to not rush in but to ease into the new move," with both branches pre-planned (2014-02-09); the daily-RWB column filter used to build a list for the turn during the COVID crash (2020-03-29); "without emotion and no ego involvement" and TSM's GLB → consolidation → WGB (2020-10-11); and the 10-week odds framing after a 26-week run (2011-03-13). Ledger 292 → 299.

## [2026-08-18] ingest | unknown-queue batch 6 (body-text seam, threshold 3 distinct markers) — 9 teaching posts (2005-11-25, 2005-12-08, 2008-03-31, 2009-02-08, 2010-08-04, 2012-06-11, 2016-03-18, 2018-06-03, 2018-08-05). New: **T2108 at 3.8% in late January 2016, "a low level only surpassed by the bottoms in 1987 and 2008"** — with the confession attached, "I promise that the next time the T2108 goes into single digits I will buy an index ETF. **But I know I will be too scared**" (2016-03-18); **"a growth stock strategy of buying stocks at new highs will not work in an environment when only 12 stocks out of 4,000 can hit a new high in a day"** — the precondition the method needs, stated in March 2008; **"stocks that have doubled often go on to double again"** and **"some of my best gains have come from stocks that have shaken me out for a small loss and then produced another buy signal"** (2018-06-03); the **3× ETFs catalogued at their February 2009 emergence** (sixteen Direxion funds), two years before TQQQ became the default; the **oversold-stochastic-then-30-day-close scan** (2010, PCLN) with its market-state caveat; the green-dot scan's **$70 price floor** — "I have more success with expensive stocks" (2018-08-05); "it is in the new high list that I look for the leaders of the next move up" (2012); the GMI as a reader's "tie breaker" and "I always trade consistent with the GMI" (2005); and a sub-50% component-1 reading read as failed break-outs (2005-12-08).

## [2026-08-18] lint | self-caught drift: a sentence I wrote this session called the 2016 T2108 reading of 3.8% "the lowest reading documented on the blog" — which contradicts Dr. Wish's own words in the same post ("only surpassed by the bottoms in 1987 and 2008") and the blog's own 6% reading of 2008-10-06. Corrected on t2108.md to state his ranking and cite both the 2008 blog figure and the reconstruction's ~1.7% at the October 2008 low. Exactly the failure mode the 2026-08-18 audit was about: a superlative added by the wiki, not by the source.

## [2026-08-18] ingest | unknown-queue batch 7 (body-text seam, threshold 2 markers + ≥200 words) — 6 teaching posts (2005-04-21, 2009-11-09, 2012-06-04, 2013-02-03, 2022-04-06, 2023-06-11). New: **a documented revision to the pension trigger** — "in the past when I took more chances I would wait for the 30 week average to curve down before taking my conservative university pension money out… however, as I wrote last November, I began to transfer my university pension money out then because of the technical weakness I saw" (2022-04-06), i.e. the November 2021 breadth-divergence exit moved the pension *five months before* the formal 30-week trigger — the discretionary overlay overriding the written rule in the opposite direction to the 2014 breach; **T2108's series begins September 1986** and "while it cannot call a top or bottom, the more extreme it becomes, the greater the likelihood" (2012-06-04); **the best-measured leveraged-ETF claim** — TQQQ +29.6% from Day 1 beat all but six Nasdaq-100 stocks, all but five S&P 500 stocks (99%), and >90% of his *curated* MarketSmith Growth 250 watchlist (2023-06-11); **"'bear market' is a dangerous habit… it is much safer to say that the market is in a down trend"** (2005-04-21, the blog's first week); lower-Bollinger-band bounces numbered in series years before the dots, with "if only I had the patience to wait for the bounce to enter my long positions!" (2009-11-09); and the 1970s range-bound market as the formative lesson — "I would make money and then give it all back and more" (2013-02-03). Noted without resolving: he gives the 1929 recovery as 26 years here and 25 years in 2025-04-20 — both recorded with their dates rather than picking one. Ledger 308 → 314.

## [2026-08-18] note | propagated the April 2022 pension-trigger revision to the two other pages that stated the 30-week rule flatly: market-state.md Step 5 (the staged-pension bullet now records the November 2021 early exit) and pension-management.md (the staged protocol is now labelled as the practice through 2014–2020, pointing at the revision below it). One canonical statement, two pointers — per CLAUDE.md §4.

## [2026-08-18] lint | playbook budget enforced (CLAUDE.md §4). Two playbooks had drifted well over the ~1,200-word procedure-only budget as batches appended to them, and both had structural damage from my append helper: it computed a section's end as the next heading, so on pages that put a `---` rule before each heading the appended bullets landed *after* the rule, orphaned from their step. Fixed the helper (a trailing rule is now kept last), then rewrote both pages. **market-state.md** 2,148 → 1,062 words of prose: orphaned bullets folded back into Steps 2/3/5, quotes compressed to one-line rules with pointers, stance table gained the 10/30-cross row. **exits.md** 2,067 → 1,307: Step 3's three trailing systems reduced to a trigger table pointing at their canonical pages, and the doctrine moved out — the order-type doctrine and the ORCT standing buy-stop to `risk-and-cash.md#stop-loss-discipline`, the COUP weekly-first worked example and the monitor note to `moving-average-rules.md#the-10-week-average`, the daily-RWB exit mechanics (two-closes rule, red-line convergence, white-space rule, the 15-day-EMA and purple-dot stop levels) to `gmma-charts.md#the-daily-rwb-chart`, the weekly ladder's rationale and NTES/NVDA examples to `moving-average-rules.md#the-4-week--10-week--30-week-alignment`. Sections reordered so both pages run Inputs → Steps → reconciliation → notes → see also → sources. No citations dropped; lint clean. Remaining: buying-glb.md at 1,492 words — over budget but procedure throughout, left as is.

## [2026-08-18] note | new command `ww tier` — bulk-tiering with a hold list, and the tier regression closed. The ~4,460 `tier: null` rows flagged in CLAUDE.md §6 since the corpus was restored have finally been re-derived, but *not* by blanket-labelling: `src/ww/corpus/tiering.py` codifies the body-marker screen that the hand triage validated over the past two days, and `screen()` proposes `daily_update` **only** for posts with no first-person teaching marker and a short body. Everything else is **held** — left untiered and un-ingested, because "not yet read" is not a classification and sweeping it flat would bury the rules the last several batches were finding. `long_form` is never bulk-tiered. Result over the 4,380 un-ingested: **3,932 tiered `daily_update`** (each carrying a `[bulk-tiered]` summary recording the reason, so the decision is auditable and reversible), **448 held** — 373 with a teaching marker in the body, 75 with a long body and no marker. `ww stats` by-tier counts are meaningful again (448 null / 268 teaching / 3,961 daily_update / 17 trade_example); the ingest queue is now a real prioritised list of 448 rather than a wall of 4,380. Command is dry-run by default and idempotent; 14 new tests (`tests/test_tiering.py`, `tests/test_tier_cli.py`), 225 passing. Ledger 314 → 4,246 rows (1.2 MB — the bulk rows are self-identifying by their summary prefix).

## [2026-08-18] note | `raw/timeline.parquet` rebuilt after the bulk tiering: **3,402 → 4,197 rows** (2005-04-24 – 2026-08-11, back from 2005-07-25 — the blog's second week is now covered), 1,154 high-confidence and 3,043 flagged. `ww timeline` parses only `daily_update`-tiered posts, so the 3,932 rows `ww tier` classified were previously invisible to it. The high-confidence share is unchanged at ~27% for the same reason as before: these posts carry their GMI and day-count readings in the title or the GMI-table image, not the body. Parsing the table images is still the outstanding upgrade — it would convert most of the 3,043 flagged rows. `history/track-record.md`'s data note refreshed.

## [2026-08-18] ingest | held-queue batch 1 — 6 teaching posts, the first drawn from the 448 posts `ww tier` held rather than swept (all had ≥2 teaching markers) (2007-10-15, 2008-04-17, 2009-04-12, 2011-02-04, 2015-10-04, 2023-08-09). This validates the hold list: every one carried primary material. New: **a concrete position-sizing constraint** — "I usually wade into these in stages **with each purchase having to be higher than the previous one. I never add to a long position that is moving down — I always average up**" (2011-02-04), which *refines* rather than contradicts the documented absence: he has no rule for *how much*, but he does have one for *when the next tranche is allowed*. The opening of `risk-and-cash.md#position-sizing` was softened accordingly. Also: **the cost of not anticipating, priced honestly** — "of course, this means that I lose some profits as the top is formed. However, I prefer to take this approach over trying repeatedly (and mistakenly) to predict the turn" (2007-10-15), with the mirror lesson six months later — hedging *inside* an intact up-trend is itself anticipation, and cost him (2008-04-17); **"while most of the world looks for bargain stocks at new lows, I seek rockets heading to the moon"** (2009-04-12); **the GMI is deliberately slower than the day count** — IBD's follow-through day rates as analogous to his short-term count, not to the GMI, and "it takes much stronger action for my GMI to signal a Buy" (2015-10-04); SQQQ accumulated through a down-trend past day 5, with component 6 watched as the swing vote to Red (2023-08-09). Also noted: a **10.2** Bollinger setting on the 2015 chart — a third setting alongside the 20.2 of 2009 and the 15.2 he settled on; a dated note added to `entry-signals.md`. Ledger 4,246 → 4,252.

## [2026-08-18] ingest | held-queue batch 2 — 6 teaching posts (2008-02-11, 2010-08-05, 2013-08-25, 2018-08-26, 2019-04-21, 2024-03-12). Two are datings the wiki lacked. **(1) The `min. 20` floor on GMI component 1 is dated 2008-02-11** — "I have added the additional requirement that it be 50% *and* that there were at least 20 new highs 10 days ago (the denominator ≥ 20). I think that the 50% requirement is not enough if it is based on fewer than 20 stocks." The component's definitional history is now complete and ordered: raw count > 100 (2005-04) → count *or* ≥ 50% (2005-07-11) → *and* denominator ≥ 20 (2008-02-11). Note the correction to sequencing: the April 2008 remark about the indicator being "very unstable when only a few stocks hit new highs" comes *after* the fix, not before it. **(2) GMI2 grew from 6 to 8 components on 2013-08-25** — "I have revised the GMI2 by adding two new indicators (7 and 8)"; the wiki previously dated the 8-component form only to a 2020 table image. Also new: the three-part selection checklist (already doubled + at/near ATH + on an IBD New America/IBD100 list, 2010) and the fact that the **Darvas scan is the one he declines to publish**; the **barchart.com → Excel → TC2000 workflow** for finding recent-IPO GLBs, with the `c/c4` yearly column trick and Livermore credited for "the first GLB of a recent IPO"; a third published GMI self-audit (2016–2019 signal chart, after 2011 and 2016); and a 2024 black-dot scan whose stop goes "just below the low of the past 2 days" — a wider window than the bounce-day low, now noted as a variant on the OSB playbook. Ledger 4,252 → 4,258.

## [2026-08-18] ingest | held-queue batch 3 — 6 teaching posts (2009-07-20, 2016-03-06, 2022-01-09, 2022-06-07, 2023-08-20, 2025-03-06). The find of the batch: **a 31-year duration study** — "our analyses from **1990-2021** showed that **23% of QQQ short term up-trends lasted 5 days or less, or 77% lasted longer. After 5 days these short term trends tend to last**" (2022-06-07). That is the quantitative basis for the Day-5 rule used throughout the playbooks, over a far longer window than the 2006-onward tabulations, and it measures *up*-trends (the side the rule is applied to when buying TQQQ). Note "our analyses" — collaborative work. Also: the 30-week rule stated as an entire system — "I get out of the market when the 30 week averages turn down and back in when they turn up. I know this seems simplistic and naive, **BUT IT WORKS!!**" (2009-07-20), with its scorecard from January 2022 — "penetration of the 30 week average saved me from the market debacles in 2000, 2008 and 2020"; **the pension was already ~20% invested by 2022-01-09**, independently corroborating the November 2021 early exit documented from the April 2022 post; "selling too soon" defended with Rothschild, Baruch and Livermore quoted in a row; the two speeds visibly diverging in March 2016 (trading IRA re-entering, pension staying out); "the key in technical analysis is to be prepared to react once a trend is in" (2023-08-20); and **"all stocks are bad unless they are going up. Stocks are only worth what someone will pay for them. Value is a myth"** (2025-03-06), with the remaining pension exposure to be sold *into a bounce* rather than at the low.

## [2026-08-18] lint | `qqq-short-term-timing.md` — the duration section was headed "Down-trend duration statistics" but had accumulated up-trend figures too, from four posts across three different windows measuring two different things. Rewritten as **"Trend duration statistics — what he has actually published"**: a four-row table (2014 / 2016 / 2019 / 2022) giving each figure with its window and which trend it measures, a note that the 2022 1990–2021 study is the one grounding the Day-5 rule, and the individual long-trend data points kept separately below. The 2014 "about one quarter of down-trends" figure is marked superseded by the ~40% of 2016 and 2019. Inbound anchors repointed in market-state.md and three source pages; two mistyped post stems in the new table caught by lint and fixed.

## [2026-08-18] ingest | held-queue batch 4 — 6 teaching posts (2007-09-04, 2010-07-15, 2011-03-15, 2014-03-30, 2025-01-09, 2025-06-22). This exhausts the ≥2-marker tier of the hold list (30 of 30 read; all 30 carried teaching). New: **component 1's thresholds clarified as inclusive** — "greater than or equal to 100 or 50%" (2007-09-04), a fourth footnote to that component's history; **the stochastic rule stated as a rule** — "declines tend to begin from a stochastic reading above 80 and advances begin from a level below 20," with the caveat that "stocks and index ETF's can stay overbought for a long time," i.e. the extreme is a precondition and not a trigger (2010-07-15); **"every long term down-trend begins with a short term down-trend"** — the reason the daily count is watched inside an intact weekly up-trend — plus the observation that the February 2011 peak preceded the Japanese earthquake by weeks, so news accelerated a turn the tape had already made (2011-03-15); **the GLB exit at its strictest wording** — "I must sell it if it *closes any day* back below its green line" — and consecutive weekly closes above a rising 4-week average as a strength count, nine for CRDO (2025-06-22); the 2025 form of the pension conditional and "I always have one foot out the door" on SQQQ (2025-01-09). **Re-dating:** the 3:45 PM intraday rule appears in **March 2014**, six months before the September 2014 post the wiki cited as its origin.

## [2026-08-18] lint | the 3:45 PM rule had ended up stated on two pages (`scans.md` from 2014-09-28 and, from this batch, `stock-selection.md` from 2014-03-30). Consolidated per CLAUDE.md §4: the canonical statement stays on `scans.md` and now carries the earlier date; `stock-selection.md` keeps only the scan material from that post and points at it. One canonical page per fact.

## [2026-08-18] ingest | held-queue batch 5 — 6 teaching posts, the first from the **long-body-no-marker** tier of the hold list (2009-08-24, 2012-03-12, 2014-12-25, 2016-12-26, 2018-07-08, 2018-10-21). That tier is productive too, so the length heuristic was worth keeping. New: **a GMI backtest that predates this wiki's** — "the same decision rules that **my student and I backtested to 2006** with incredible success" (2012-03-12), with a third party (dark-liquidity.com) independently charting GMI-driven QQQ/QLD performance. Neither the rules as tested nor the results are reproduced on the blog, so it cannot be checked — noted on `backtest-timing-overlay.md#limitations` as prior art, with the caveat that his test used his *reported* GMI rather than a reconstruction. **RWBCount re-dated to 2016-12-26** ("I have created a new indicator"), a month earlier than the wiki had it, with the fuller definition: it tests *strict ordering* (1>3>5>…>60), not merely red-above-blue. Also: the index-over-stock argument in full before TQQQ existed, with the Nasdaq-100 preferred partly because it "contains no financial stocks" and a 100-stock basket blunting single-name earnings risk (2009-08-24); the **rates thesis** — competing yield, not valuation, as the mechanism that would end the bull, with a concrete personal threshold of 6% on insured CDs (2014-12-25), which is why bond ETFs are on his charts at all; **"all green dot signals do not work and if it were possible to predict in advance which ones will, I would be living on my own island"**, with the setup's value located in the cheap failure rather than the hit rate (2018-07-08); and an intraday all-time-high TC2000 condition set with his own filters, which is how a GLB gets caught *during* the session (2018-10-21). Ledger 4,270 → 4,276.

## [2026-08-20] ingest | held-queue batch 6 — 6 teaching posts from the long-body tier (2005-06-22, 2009-04-05, 2011-02-28, 2013-12-26, 2014-04-06, 2016-09-11). The find: **the clearest rationale for GMI component 6 anywhere in the corpus** — "the IBD Mutual Fund Index is above its 50 day average, indicating to me that growth mutual funds are starting to make money. **When these fund managers can make money buying growth stocks, so can I**" (2009-04-05). The component is a proxy for whether professionals running his own strategy, with more resources, can currently make it work — which is why he treats it as a precondition rather than one vote of six. Also: **why a breakout level becomes support** — "people who missed the break-out get a second chance to buy the stock near that level" (2011-02-28), the demand mechanism behind every bounce entry, with the stop below the recent bounce low; **band expansion as the pinch's other half** — "the expansion (widening) of the bands often signals the beginning of a major move" (2016-09-11), plus the seasonals (Friday declines → ugly Mondays, bottoms often in October, September the weakest month); **"when the market leaders fail, the rest of the stocks eventually falter"** with a rotation *into* value read as a late-cycle tell (2014-04-06); two crowd tells read as warnings that do not trigger a sale — the uninterested announcing purchases, and all his holdings rising at once (2013-12-26); and sentiment read from an IBD Meetup room, where low attendance at the lows and fear of the leading stock were both bullish (2005-06-22). Ledger 4,276 → 4,282.

## [2026-08-20] lint | `entry-signals.md` had drifted the way the playbooks did: repeated appends had put **13 `###` subsections under a heading labelled "Recent practice (2020-2025)"** that by then held 2009, 2011, 2016, 2018 and 2019 material. Regrouped into three themed sections, each internally coherent — **The dots in practice** (green dot: LULU 2019, the green-line gate 2020, stop-below-bounce 2020, the $70 floor 2018, the hit rate 2018, the dot sequence 2024), **Bollinger Bands — the settings, the bounce, the pinch** (extended-from-support 2009, the series of lower-band bounces 2009, bounce and pinch 2022, expansion 2016, the settings note), and **The moving-average setups** (x8/x21/30 2024, blue dot 2025). No content dropped, no citations lost, no inbound anchors broken; the one cross-link into the pinch was repointed at its subsection.

## [2026-08-20] lint | structural pass over every wiki page, prompted by the drift found in `entry-signals.md` two entries up. Three findings, all fixed.

**(1) Closing matter stranded mid-page.** Repeated appends had pushed 6 sections past `## See also` on three pages (`green-line-breakouts.md` ×4, `moving-average-rules.md`, `qqq-short-term-timing.md`), so content added later read as an afterthought below the page's own "see also" list. Rather than fix by hand and let it recur, this is now **a lint check**: `_sections_after_see_also` errors when any section other than `## Sources` follows `## See also`. Three new tests; the check found exactly the 6 real cases and the three pages were reordered.

**(2) A genuine contradiction about where the green line is drawn.** The page carried both statements ~200 lines apart, unreconciled: a 2013 comment — "I draw the green line on a monthly chart, **sometimes** near its highest monthly **close** which may be below the highest price it traded at during the month" — and the 2022 post — "I drew it at **the top of the highest monthly bar** even though the stock retreated from the high that month… I adhere to the rule to draw it at the highest monthly bar, at 56.40. When it crosses that line it is truly at an ATH." These disagree. Resolved as a dated supersession: the 2022 form is the rule (later, stated as a rule, with a rationale), the 2013 comment describes earlier practice with "sometimes" doing real work. Flagged in both directions — on `green-line-breakouts.md` and on `reader-qa.md` — and a third variant on the same page ("highest monthly close not surpassed for 3+ months", asserted of index green lines) was corrected to the neutral wording, since it was a wiki paraphrase rather than his words.

**(3) `green-line-breakouts.md` at 5,866 words**, the largest methodology page. Split: the *evidence* — worked cases, failures, the missed WING breakout, the close-below justification, the sell-side inversion, the entry caveat, recent practice 2019–2026 — moved to **`methodology/glb-in-practice.md`** (2,402 words, 19 sources), leaving the definition, drawing convention, entry and exit on the parent (4,824 words). Catalogued in index and overview.

Also noted: my earlier page-size audit under-counted several pages because it split on internal `---` rules rather than the front-matter delimiter; corrected, `reader-qa.md` is 1,700 words rather than the 125 it appeared to be.

## [2026-08-20] ingest | held-queue batch 7 — 5 teaching posts + 1 meta from the long-body tier (2005-12-26, 2006-06-05, 2006-07-18, 2006-10-23, 2014-10-19; meta: 2009-01-26 the TypePad→WordPress migration, which explains the migrated URLs and image paths in pre-2009 posts). **The re-dating of the batch: the ultra-ETF thesis is quantified in October 2006, not June 2009** — QQQQ +8.9% since August 16 while QLD rose 16.9%, "a return that beat 84% of the Nasdaq 100 stocks… Why try to find the few individual stocks that outperform the QQQQ?" The entry condition is already the GMI and the comparison is already against the *distribution* of component stocks rather than an average, which is the form every later measurement takes; `leveraged-etf-default.md` now opens with 2006 and keeps the 2009 study below it. Also: **GMI-S and GMI-L share one construction** — "each index measures 4 trend indicators each for the DIA, IJR, SPY and QQQQ," so both are 16 tests reported as a percentage and differ only in horizon, which is why they are always quoted together on the same scale; the **cap-weighted-index divergence observed in July 2006** (index breadth 50–54% against universe breadth 36%), the same mechanism as the November 2021 exit fifteen years earlier; the **10-day/30-day average relationship** used to define the short-term trend in 2005, before the day count became the published measure; and the pension sold **into resistance** in October 2014 ("if the market rises to likely resistance levels, I will take more of my pension out"), the same pacing as the March 2025 instruction. Ledger 4,282 → 4,288.

## [2026-08-20] ingest | held-queue batch 8 — 8 long-body posts (2005-07-21, 2005-10-06, 2006-01-17, 2006-06-08, 2010-04-26, 2016-01-03, 2017-01-08, 2017-07-16); two re-datings and one indicator concept the wiki did not have. **Why GMI component 1 exists, in his own words.** The wiki has carried component 1's *definition* and its three revisions since early on, but never its rationale. Two posts supply it: October 2005 credits the observation to the literature rather than to himself — "many of the gurus cited in the books to the right have observed that **failed break-outs are a sign of impending market weakness**" — and January 2017 states the purpose in one sentence, "**when stocks that hit a new high do not continue to rise, it is one sign of potential weakness I track**." It is a follow-through test, not a new-high count, which is why the 2008 denominator floor was worth publishing. **Re-dating 1: the low-side mirror statistic moves from August 2006 to October 2005** — "there were more (99) 'successful' 10 day new lows, suggesting that shorting stocks at new lows has been profitable" — so the heading on `gmi.md` now reads "in use by 2005," which also resolves an internal inconsistency (the section's closing line already documented a May 2005 instance). **Re-dating 2: the leader-on-good-news tell moves from April 2014 to July 2005** (GOOG and MSFT slammed after earnings), and now runs 2005 → 2006 → 2014 → 2016 (NKE after a good report, DIS on Star Wars) in near-identical language. **New concept: the Hindenburg Omen** — the coincidence of elevated new highs *and* new lows, named 2005-10-06 (41 highs vs 148 lows), added to `gmi.md` and `glossary.md`; he names it once and never builds a component on it, which is worth recording as much as the concept. **The override case:** with the GMI at its maximum +6 he sold anyway — "**yes, I know the GMI is still at +6, but if I wait for it to give a definite sell I will lose most of my profits**" — the doctrinal counterpart to the lagging-by-design disclaimer, and he flags his own accompanying forecast as a departure from his method. Also: "**I would never hold a long position in a stock or ETF in a BWR down-trend**" (the RWB/BWR rule at its most absolute, with the six-chart index survey that produces it); **O'Neil's shopping list** as the documented source of his watch-list procedure, with the TC2000 GLB volume-buzz alert dated to July 2017 (a year before the 2018 condition set) and the SHOP alert he missed in 2017 — the same failure mode as WING in 2023, twice documented; the market gate **quantified** in January 2006 (QQQQ +13.4% off its 10-week signal while 86% of the Nasdaq-100, 88% of the S&P 500 and 87% of the Dow 30 advanced), filed on `trading-philosophy.md` with the caveat that it measures the gate working rather than a base rate, and that his stated figure drifted from ~70% (2005) to "80%+" (2006); **TRLG (2010)** as the round-trip-to-an-ATH worked case, notable for naming the missing breakout volume as a defect while buying and for using calls to cap risk into an earnings report; and T2108's **90% upper band** (2010) — his highest published figure, against 80% in 2007 and 2011, so the upper band is now written as a 70–90% zone. New: `trading-psychology.md` rule 9 (not trading is a position), `stock-selection.md` watch-list section, `glb-in-practice.md` TRLG section. Ledger 4,288 → 4,296.

## [2026-08-20] note | structural debt for the next pass: `risk-and-cash.md` (6,492 words), `stock-selection.md` (6,022) and `gmi.md` (5,786) are all far past the ~800-word guideline and each is now doing several jobs. risk-and-cash was split once on 2026-08-18 and has grown back; the natural next seams are the *tells* (leader behaviour, sentiment, breadth divergence, rates) as a page of their own, and stock-selection's O'Neil/IBD-audit material as a lineage page. Not done in this batch to keep the ingest and the restructuring separable.

## [2026-08-20] ingest | held-queue batch 9 — 6 long-body posts (2005-06-09, 2005-06-23, 2005-10-08, 2006-03-30, 2014-02-17, 2017-04-16). **The find: his earliest and most general self-published limitation, from March 2006.** Back from a break — "I have been burnt out on this market. Nothing I have done worked and my account has gone nowhere" — he diagnoses the *regime* rather than his execution: "**I realized that moving averages are useless for providing signals in a trendless market**… the index has gone back and forth over the 30 day (red) and 50 day (green) moving averages. Thus, **the averages and the GMI have been giving erratic, contradictory signals**." The wiki already carried two limitations he published about the GMI — the 2008 QQQ-centricity blind spot and the 2015 whipsaw demotion — but both concern *what* it measures; this one concerns the conditions under which any trend-following measurement carries information at all, and it predates both. It also contains the check worth copying ("this index has gone nowhere since last November. Why should we expect to have made any money trading tech stocks in this period?") and the substitute tool: trend lines and channels, with a volume condition on the break, justified with unusual frankness — "I guess because so many people think they work. Why should I care to understand the reasons, so long as the lines help me to predict probable levels of support and resistance." New section on `moving-average-rules.md`; the 2015 GMI limitation section now points back to it. **The other candid one:** October 2005 gives the temptation he still has and the mechanism he uses on it — "the same price pattern that works so well in a rising market is likely to fail in a declining market… **one way I handle such a temptation is to use a very small portion of my portfolio to buy that irresistible stock — just in case I am right**." Filed as `trading-psychology.md` rule 10, because it is a sizing decision rather than an act of will, and the same design as the stop and the pilot portfolio: build the machine so being human is affordable. Also: **the 10-day average given its actual job** — "a close below the average may not be a sell signal, but it serves as a yellow light to me," gating *new* buying rather than exits (new section on `moving-average-rules.md`, replacing its absence); **the defensive sequence in order** — stops raised to just under the day's lows first, 100% cash only when "my QQQQ daily index definitely turns negative," which is keyed to the trend indicator and not to the GMI; **the gate measured on the downside** (QQQQ −4.3% from the August 2005 peak, only 34% of components up, 18% up 5%+), the mirror of the January 2006 measurement filed yesterday; **0/0 and 6/6** as the extremes of the RWB count notation, with "a return to 6/6… would be a new buy signal for me" — the notation is a trigger, not a description — plus the weekly-BWR pension trigger and the screening inversion "**I like market declines because it is easier for me to find potential leaders in a dwindling new high list**" (60 names in a 4,800-stock universe, read in full); **I-bonds** as the only specific cash instrument he has recommended, chosen because they cannot be marked down by the rate reversal his 2014 thesis warns about; weekly covered calls quantified at ~3%/month on GLD; and a clean corroboration of the GMI Sell rule six years into its use — a score of 1 "still on a GREEN signal. One more day below 3 will change it to RED." Ledger 4,296 → 4,302.

## [2026-08-20] ingest | held-queue batch 10 — 6 long-body posts (2006-02-27, 2006-05-30, 2007-01-08, 2009-04-19, 2015-07-12, 2018-02-04). **Two instruments gained their missing half.** The **put/call ratio** was documented only at high readings, as a bounce warning; January 2007 supplies the other pole — at 0.41, near a 12-month low of 0.38, "**a low p/c ratio suggests relatively fewer people bearish enough to buy puts, a contrary indicator, often signaling impending market weakness**" — and February 2018 supplies the number the glossary was missing: "when the ratio reaches **1.2 or higher** we will be near a bounce," quoted alongside the other oversold gauge, a QQQ daily 10.4 stochastic of 0.20 or less. The glossary entry's claim that 2018-03-25 was the first explicit citation is corrected: the indicator is in use by February 2006 ("a relatively high .76"), so 2018 is where the threshold is fixed, not where the instrument starts. The **monthly GMMA top template** was documented only as an endpoint (red converging with and falling below blue); 2018 gives the ordered stages — (1) price closes below all six red averages, (2) the red averages turn down and converge with the blue, (3) red crosses below blue — with "**this pattern takes several months to develop**," which is the exit-latency argument in mechanical form. Stage 1 alone is common and means little. **The IBD 100 comparison has an origin date and a first finding.** 2006-05-30: "I expanded the comparison of my indicators to include the IBD 100 stocks… to see how the highly rated IBD100 stocks' performance compares with my universe of 4,000 stocks" — begun as a *market* diagnostic, a second breadth sample, not a scorecard for IBD. Its first result reconciles the harsher audits already on `stock-selection.md`: short-term the two groups were indistinguishable, but 31% vs 51% above the 10-week average and **52% vs 90% above the 30-week**. Growth-list stocks hold long-term trends better than the market *and* underperform inside declines — both audits are true, and the page now says so with a table. **The GMI limitation, restated harder.** July 2015: the red arrows marking Sell signals "indicate that **during this bull market one would have done well by buying stocks when the GMI issued a Sell**" — not merely that the Sells were early, but that fading them would have paid. His defence is about tails, not hit rate, and the cost is absorbed by *where* he trades: "I don't mind exiting with a GMI Sell and going back in… **this is a benefit of trading in a tax deferred IRA**." Recorded with the qualification that the same rule would be poor advice in a taxable account. Also: **a named fallacy** — "the media pundits claim the market needs to rest. The market gets tired and needs to consolidate for a while — such utter nonsense!" — answered with a duration base rate (day 22 against an 80-day up-trend), which is the day count used against a narrative rather than for sizing; **QSII's three-year base** as the strongest form of the ATH pattern, with Darvas's supply argument ("everyone who owned them had a profit"); **the short-side scaling rule written while losing on the position** — small bets with close protective stops, accumulate only if the decline deepens, and pick "the inverse ETF **on the weaker index**"; **component 6 stated in the negative** in 2007, two years before the positive form; the pension exit trigger as a **conjunction** (a close below the 30-week *and* the average turning down); and, from February 2006, an honest anomaly — Investors Intelligence bullishness *fell* as the market rose, and rather than rescue the contrarian model he wrote the puzzle down and backed the technicals. Ledger 4,302 → 4,308.

## [2026-08-20] ingest | held-queue batch 11 — 6 long-body posts (2006-07-17, 2007-07-30, 2009-10-26, 2010-10-11, 2012-10-21, 2016-03-20). **A term the wiki used constantly and had never defined.** "Volume buzz" appears in the GLB alert workflow, the 2018 intraday ATH condition set and the breakout criteria, always as though its meaning were obvious. The 2009 Worden post defines it: "**volume buzz compares each stock's volume to its average volume at a specific time during the trading day**… at 10:05 AM I can rank my watchlist by how each stock's current volume at 10:05 AM compares with its average volume at 10:05 AM." The **time-of-day normalisation is the whole point** — it is not volume against average *daily* volume, which is what makes unusual volume detectable while the session is still open rather than after the close. Now a glossary entry; the averaging window is undisclosed and recorded as such. **The two-tier timing rules, stated canonically.** 2012-10-21 was written to settle reader confusion and is the most explicit statement in the corpus — and the finding is that the two triggers **are not the same shape**. Speculative money runs on a *disjunction* ("when my QQQ short term indicator turns down **or** the GMI goes below 3… I may raise sell stops, move to cash or go short"); the pension on a *conjunction* at a lower threshold ("only after the GMI has been **1 or 2 for a while** *and* the longer term moving averages curve down"). Note **1 or 2, not "below 3"** — a GMI of 3 makes him cautious in the trading account and does nothing to the pension. Filed as a table on `pension-management.md`. **Why the lag in his exit rules is affordable**, from July 2007 in cash: "**there is plenty of time to make profits AFTER the market has revealed that it has turned. There is no need to anticipate the reversal; that is usually a futile and costly practice**" — with the re-entry stated as a number ("I will wait for the GMI to climb back above 3"), and, in the same post, T2108 at 15 read and *declined*: "definitely in market bottoming territory. **But this is not the time to be a hero.**" An oversold reading describes a condition; it does not authorise a purchase. The screen that makes the waiting cheap is the post-decline new-high list — "the few stocks that come through a decline like this and quickly break out to new highs are the ones I want to own" — now its own section on `stock-selection.md`. Also: **the survivorship objection dated to July 2006** and stated as method ("they keep replacing underperforming stocks with better performing stocks… the list published on a particular date gives a more accurate indication"), a month before the known August statement; **a third put/call threshold** — "above 1.0" in 2012, against 1.2 in 2018 and 1.25 later that year, so the bounce level is written as a **1.0–1.25 zone** rather than a number; **the leader-on-good-news tell at its positive pole** ("when stocks surge on good earnings… we know that we are in a strong up-trend where funds and traders are buying strength"), completing a diagnostic the wiki had only in its bearish form; **what cash was actually earning** (Fidelity Cash Reserves at 4.8% in July 2006) — the only place he prices the other half of the cash decision; **why day-1 entries are hard**, admitted with the 12% he forwent ("on the first day of a new trend one does not usually believe it will last"); and **buying before the green line with a tighter stop** — MXL entered pre-GLB on the cup-and-handle pivot at 18.18 rather than the green line at 19.50, with the rule-bending named rather than presented as method. Two scans added (`monthly`-RWB doubler variant; the student bounce scan, whose GTC stop below the 30-day average ships with the list). Ledger 4,308 → 4,314.

## [2026-08-25] ingest | held-queue batch 12 — 6 long-body posts (2005-07-05, 2005-11-20, 2006-06-14, 2010-04-12, 2015-12-06, 2016-05-01). **A re-dating and an attribution correction on the wiki's most-quoted line.** "Value is a myth / stocks are only worth what someone will pay for them" was dated to a 2025 post. It is a **2006** position — "by now, everyone should see through the widely proclaimed conventional nonsense that stocks have intrinsic value. Stocks are only worth what someone else will pay for them" — and, more usefully, the companion line is **O'Neil's, quoted**: "as William O'Neil says, **all stocks are bad unless they are going up**. But I say that 'bad' stocks can make a trader a lot of money if s/he shorts them correctly." The 2025 statement is him restating a borrowed line he had been citing for nineteen years, with his own short-side corollary attached. The same post supplies the *mechanism* behind the leader-on-good-news tell rather than another instance of it: GS punished after great earnings because "**in a down-trend, all events are seen through a dark glass that is perceived to be half empty. Everyone sells quickly because they think that the next guy will sell**" — the news is constant, the interpretation is regime-dependent, which is also why the same setup carries a different base rate in a bear market. Filed as a new section on `trading-philosophy.md`. **The GMI's 2008–2010 signal record, with dates** — which `track-record.md` did not have. Defensive from 2008-09-02 (GMI 3→1) through 2008-12-30, the QQQQ falling 35% inside that stretch; an 8-day rebound to 3 that did not hold; below 3 again from 2009-01-12 to 2009-03-23. The threshold is stated plainly — "**I tend to get defensive when the GMI is less than 3**" — eighteen months *before* the two-day persistence rule, so the record is a raw score history rather than a signal history, and the page now says so. His own verdict is worth keeping for its tone: "while not perfect… past performance does not guarantee future success," with no entry prices, exit prices or return figures claimed. **The green-line retest entry, quantified.** The written GLB rules allow "wait for a re-test" in half a clause; HELE (2015) works it out — buy the bounce off the green line, stop just beneath, **risk 4–5%** — with the line doing double duty as support and invalidation, which is what keeps the risk that tight. It also reframes repeated retests as repeated entries rather than as failure. Also: **the don't-marry-a-scenario rule executed rather than stated** (2005-07-05 — SPY puts sold at a loss and longs bought the same session, with stops attached and puts kept on the weakest names: changing your mind is allowed to be partial); **a third trend-odds measurement** (81% of Nasdaq-100 components over a 6.6% index gain) with a note that his gloss — "an 81% chance of having a profit" — converts a participation rate into a per-trade probability and should not be quoted as the latter; **the primary Darvas source named** ("Pas de Dough," TIME, 25 May 1959); **a scan run over industry indexes instead of stocks**, turning a stock screen into a sector screen, with its stock-level yield stated (15 of ~5,500); **the white-space qualification** — red below blue is necessary, the gap opening is what confirms a BWR — with UUP and GLD read as a macro pair; the **down-sloping neckline** as the bearish variant, now a glossary entry; and T2108's ~90% top band corroborated a second time within a fortnight, with the useful distinction that *overbought* starts near 80 while the levels *seen at tops* are nearer 90. One flag recorded rather than smoothed: he writes in December 2015 that he is "just discovering the benefit of a monthly GMMA chart," eighteen months after publishing monthly Guppy charts of the 2000 and 2007 tops — read as when the layer entered routine use. Ledger 4,314 → 4,320.

## [2026-08-25] ingest | held-queue batch 13 — 6 long-body posts (2006-01-09, 2006-06-27, 2008-01-28, 2015-10-25, 2016-09-18, 2017-07-04). **A missing attribution on the philosophy's load-bearing claim.** `trading-philosophy.md` presents "success is determined mostly by exit rules, not entry — one could probably select stocks at random as long as losses are kept at a minimum" as his own proposition five, from November 2009. It is **Richard Dennis's**, and he credited it at the time: reviewing Michael Covel's *The Complete Turtle Trader* in January 2008, "**the most important thing I learned from this book was the mentors' primary emphasis on exits from a trade rather than entry. Dennis is quoted as basically saying one might profit by selecting positions by trial and error as long as one had a good exit strategy.**" Twenty-two months later the wording survives almost intact and the attribution is gone. He also flags the adaptation gap the 2009 version doesn't — the Turtles' rules were built for futures, "which I think can be adapted for trading equities," asserted rather than shown. **A dated contradiction in the GLB exit rule.** September 2016: "I immediately sell it if it ***trades*** back below its green line break-out point — **no exceptions**." That is the intraday trigger, and it is the opposite of the mental-stop rule the wiki documents from 2020–2023, which exists *precisely* to avoid selling on an intraday violation that closes back above the line. The same 2016 post supplies the reason it changed — "**I find that a daily chart can often lead me to be whipsawed and to sell a good stock too soon. It's like checking one's blood pressure or cholesterol too often**" — and by July 2017 the wording had already moved to "as long as it *closes* above its green line." Filed as **intraday (2016) → close-only (2017 onward)**, with the ambiguous 2018 "strict immediacy" statement placed between them rather than silently harmonised. **The GLB Tracker Table is a survivor list, and he says so** — "this list does not contain all GLB stocks that occurred during this period. It contains only those that have **held** their GLB (i.e., successful)." So it is a watchlist and cannot be used to estimate how often a GLB works; the page now says that, and records that he flags luck inside the table too (CLCD +197%, "a lucky pick"). Also: **the denominator floor began as discretion** — June 2006, declining to call component 1 positive on 9 of 15 because "the numbers here are too small," twenty months before the ≥20 rule, and his improvised version was the stricter one; **the first generation of inverse ETFs** (PSQ, SH, DOG, MYY) whose significance to him is IRA access rather than leverage, plus **product issuance as a crowding signal** ("not long after… a relevant new ETF is issued, that sector is close to a top"), a sentiment instrument that appears nowhere else in the corpus and which he applies to the launch he has just welcomed; **a GMI of 6 refused and named as psychology** — "if I was eager to trade I would have just followed the GMI's signals. But after the August flash crash, I am much more of a chicken right now than usual," stated with its counterfactual, its self-doubt ("maybe I will turn out to be a great contrary indicator!?") and its return condition, which is what makes it a rule rather than a lapse (now `trading-psychology.md` rule 11); **the QQQ-centricity blind spot demonstrated live in 2017** and named in the same sentence; **biotechs given an explicit sizing exception** (the asymmetry that makes them attractive makes a stop unreliable, so size carries the risk); and **the same breadth reading read against its own history** — 505 new highs in January 2006 versus 522 just before the August 2005 top, where the *higher* reading came with weaker supporting breadth and a month-old rally rather than a two-day-old one. Ledger 4,320 → 4,326.

## [2026-08-25] ingest | held-queue batch 14 — 6 long-body posts (2005-05-25, 2008-11-24, 2009-12-27, 2016-10-16, 2021-12-05, 2022-02-27). **The "no need to anticipate the reversal" doctrine, measured.** The July 2007 statement filed last week is an assertion; November 2008 supplies the arithmetic. Fifty-nine days into the down-trend that began 2 September 2008: "**99% of the Nasdaq 100 stocks** (all but APOL) **have declined, and 44% have declined 50% or more. Even if we had missed the initial sell signal and waited until a failed bounce on September 19, still, 99% of the Nasdaq100 component stocks have declined since then, one half by more than 41%. So you see, one could have missed the first sell signal by about 2 weeks and still have saved a lot of money.**" A two-week delay captured almost all the avoidable damage — the strongest single argument for tolerating a lagging exit signal, and the exact mirror of the entry side, where the leaders announce themselves on the new-high list *after* the turn. **And in the same post, his own oversold gauge failing, flagged in his own italics**: T2108 "rebounded from 5% to 7%, and is still in what ***used to be*** indicative of an imminent bottom." The low came four months later, so the caution was warranted; it is the clearest instance of him treating a historical threshold as provisional rather than as a rule, and `t2108.md` now records it. **Why an ATH after a decline means accumulation** — the overhead-supply argument applied to the whole market, and the best statement of it: "**stocks that fell a lot will have to overcome selling as they try to advance, as persons who rode it down and have losses try to sell out. A stock that can overcome such selling and reach an ATH is demonstrating strong buying interest**" (2022-02-27). The decline does the screening: it manufactures trapped sellers in every damaged name, so clearing that supply *and* printing a new high is evidence that cannot be faked by a quiet drift. **The pension trigger named prospectively and by component** (2021-12-05, two weeks after the November 2021 top): "**the last GMI component to turn negative will be for the weekly QQQ to close below its 30 week average. When that happens I will begin to go to cash in my primary pension accounts**" — mapping the pension onto GMI component 5 rather than onto the composite, which is why a GMI of 1 had not yet moved it. Also from that post: the **GMI-2 rose from 2 to 4 while the market fell**, purely because two daily stochastics hit very oversold levels — a construction artefact worth knowing, since the oscillator components make GMI-2 partly a *mean-reversion* gauge and therefore capable of improving as conditions deteriorate. Also: **the naive-participant tell at both poles** — an outsider asking how to short marked the March 2009 bottom, one proposing to remortgage to buy marked the 2000 top — with the epistemic frame attached, "**does this mean the market has to turn up? Not necessarily, but the market is always an assessment of competing probabilities**"; **meetup attendance as a sentiment series** (three people where eight to ten was normal), which lags by construction and therefore marks lows rather than predicting them; **TLT named as the long-rate instrument** ("how bond traders *feel* about long term interest rates") together with the best caution in the corpus about macro storytelling — TLT down, dollar up, gold down, and then "**it all fits together like a jig saw puzzle — until it doesn't**"; **the GMI's whipsaw problem noticed contemporaneously** rather than in retrospect ("this signal has recently coincided with short term bottoms rather than tops," October 2016); **a rare sentiment extreme observed and declined** (II bears ≈ bulls in February 2022, as at the 2020 bottom, but T2108 never reached single digits — sentiment does not override breadth); and **both entry types named as a pair in May 2005** ("break to new highs **or** bounce off of their support levels"), eleven years before BOS was named — what the later work adds is the *definition* of support and a mechanical trigger, not the idea. Biographical: **David**, his co-presenter and colleague of 20+ years who managed the course, ran his TA presentations and "surpassed me at running TC2000," died 2022-02-18. Ledger 4,326 → 4,332. **The long-body queue is now 13 posts from empty.**
