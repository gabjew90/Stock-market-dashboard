"""Quantitative check: for each 'Day 1 of new QQQ short-term' post in 2024-2026,
test whether the announced direction is consistent with (a) QQQ close vs 10-week SMA
and (b) QQQ close vs 30-day SMA."""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "posts"

prices = pd.read_parquet(ROOT / "data" / "backtest" / "prices.parquet")
if not isinstance(prices.index, pd.DatetimeIndex):
    prices = prices.set_index(pd.to_datetime(prices.index))
prices = prices.sort_index()
qqq = prices["QQQ"].astype(float)

sma30 = qqq.rolling(30, min_periods=30).mean()
sma50 = qqq.rolling(50, min_periods=50).mean()  # ~10 weeks, daily-updating
wk_close = qqq.resample("W-FRI").last().dropna()
wk10 = wk_close.rolling(10, min_periods=10).mean()
sma10w = wk10.reindex(qqq.index, method="ffill")
# also test: 10-week SMA on weekly closes, but only including FULL prior weeks (lag by 1)
sma10w_lag = wk10.shift(1).reindex(qqq.index, method="ffill")

pat = re.compile(r"^(202[456])-(\d{2})-(\d{2}).*day-?1-of-(new-)?qqq-short-term-(up|down)", re.I)
hits = []
for p in sorted(RAW.iterdir()):
    m = pat.match(p.name)
    if not m: continue
    date = pd.Timestamp(f"{m.group(1)}-{m.group(2)}-{m.group(3)}")
    direction = m.group(5).lower()
    hits.append((date, direction, p.name[:70]))

print(f"{'POST DATE':12} {'DIR':5} {'FLIP DATE':12} {'QQQ':>8} {'30d':>7} {'50d':>7} {'10wk':>7} {'30d?':5} {'50d?':5} {'10w?':5}")
print("-" * 86)
ok = {"30d": 0, "50d": 0, "10wk": 0}
total = 0
for date, direction, name in hits:
    flip = qqq.index[qqq.index <= date][-1]
    q = qqq.loc[flip]
    m30 = sma30.loc[flip]
    m50 = sma50.loc[flip]
    mw  = sma10w.loc[flip]
    if any(pd.isna(x) for x in (m30, m50, mw)): continue
    c30  = (q > m30) if direction == "up" else (q < m30)
    c50  = (q > m50) if direction == "up" else (q < m50)
    c10w = (q > mw)  if direction == "up" else (q < mw)
    ok["30d"] += int(c30); ok["50d"] += int(c50); ok["10wk"] += int(c10w); total += 1
    print(f"{date.date()!s:12} {direction:5} {flip.date()!s:12} {q:8.2f} {m30:7.2f} {m50:7.2f} {mw:7.2f} {('Y' if c30 else '.'):5} {('Y' if c50 else '.'):5} {('Y' if c10w else '.'):5}")

print("-" * 86)
print(f"QQQ vs 30-day daily SMA: {ok['30d']}/{total} = {100*ok['30d']/total:.0f}%")
print(f"QQQ vs 50-day daily SMA: {ok['50d']}/{total} = {100*ok['50d']/total:.0f}%  (~10wk, daily-updating)")
print(f"QQQ vs weekly 10wk SMA:  {ok['10wk']}/{total} = {100*ok['10wk']/total:.0f}%")
