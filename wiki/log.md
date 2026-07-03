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
