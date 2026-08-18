---
title: "WW 2007-09-17 — IBD100 survivorship bias; even leaders follow the index trend"
type: source-summary
updated: 2026-08-12
sources: [raw/posts/2007-09-17-gmi-5-ibd100-stocks-not-good-for-buy-and-hold.md]
---

# WW 2007-09-17 — IBD100 survivorship bias; even leaders follow the index trend

**Source:** [GMI: 5; IBD100 stocks not good for buy-and-hold](../../raw/posts/2007-09-17-gmi-5-ibd100-stocks-not-good-for-buy-and-hold.md) · [original](https://wishingwealthblog.com/2007/09/gmi-5-ibd100-stocks-not-good-for-buy-and-hold/) · tier: teaching

## What it covers

A sceptical audit of his own primary candidate pool. Dr. Wish criticises the **survivorship bias** in IBD's published performance figures, then measures the lists himself and reaches the conclusion that underwrites his whole market-state approach: entry date beats stock selection. Also corroborates the **30-day average** as the basis for the GMI's daily-trend components.

## Key claims

- **The bias, named:** "IBD continually drops poor performers from the index, thus biasing the results heavily toward the positive. And a lot of new stocks may be substituted each week." He measures the *original* published lists instead.
- **The measurement:** only about half the stocks in each list closed higher than on their publication date. The two outliers are the point — only **31%** of the 7/16 list were higher (that list was published at the top of the summer rally), while **82%** of the 8/20 list were (published as the Nasdaq 100 bottomed).
- **The conclusion, his emphasis:** "**even the fate of the IBD100 stocks is largely determined by the trend of the relevant market index**, here the Nasdaq100. This is the reason why I always trade consistent with the trend of the market, as measured by the GMI."
- **Leadership decays:** "the further back one goes, the less likely are the IBD100 stocks to be near their 52 week highs. After about 4 months, the IBD100 stock lists tend to look a lot like the stocks in the Nasdaq100 or S&P500." Hence: "not good candidates for a long term buy-and-hold strategy. Then again, neither are most stocks."
- **The 30-day average drives the GMI's daily-trend component:** "the 30 day average (red line) appears to be reversing to the up-side... I will look for support of the QQQQ at the 30 day average, currently at 47.90. **Several closes below the 30 day would decrease the GMI**." This is direct evidence that the QQQQ/SPY daily-trend components are 30-day-average tests — the reconstruction in `src/ww/indicators/gmi.py` had treated that as an unverified proxy.
- Breadth warning at GMI 5: only 82 new 52-week highs against 90 new lows.

## Feeds wiki pages

- [gmi.md](../methodology/gmi.md) — the 30-day average as the daily-trend component (corroborates the code's proxy)
- [stock-selection.md](../methodology/stock-selection.md) — IBD100 survivorship-bias caveat; leadership decay after ~4 months; entry date over selection
- [timeline.md](../history/timeline.md) — September 2007

## Sources

- [GMI: 5; IBD100 stocks not good for buy-and-hold](../../raw/posts/2007-09-17-gmi-5-ibd100-stocks-not-good-for-buy-and-hold.md)
