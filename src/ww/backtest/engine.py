"""A minimal daily long/cash backtest simulator. The position held DURING day t is the GREEN signal as of t-1
(the standard 1-day-lag execution model — realistic 'trade at next open' simplified to close-to-close), with the
round-trip cost deducted on the day a switch takes effect. No look-ahead, by construction."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class BacktestResult:
    equity: pd.Series                     # growth of $1, daily (1.0 the day before the first return)
    daily_return: pd.Series               # daily net return of the strategy
    signal: pd.Series                     # the GREEN bool series used (aligned to equity.index)
    trades: pd.DataFrame                  # cols: side, entry_date, exit_date, days, entry_px, exit_px, gross_ret, net_ret
    long_etf: str = "QQQ"
    red_etf: str | None = None
    cost_bps_round_trip: float = 5.0
    params: dict = field(default_factory=dict)


def run_backtest(
    signal: pd.Series,
    prices: pd.DataFrame,
    *,
    long_etf: str = "QQQ",
    red_etf: str | None = None,
    cost_bps_round_trip: float = 5.0,
    start: str | None = None,
    end: str | None = None,
) -> BacktestResult:
    """`prices` = wide close-price DataFrame (must contain `long_etf`, and `red_etf` if given). `signal` = daily bool
    (True => be long the long_etf). Returns a BacktestResult. Cash (red_etf=None) earns 0%."""
    cols = [long_etf] + ([red_etf] if red_etf else [])
    px = prices[cols].copy().dropna()
    idx = px.index
    if start:
        idx = idx[idx >= pd.Timestamp(start)]
    if end:
        idx = idx[idx <= pd.Timestamp(end)]
    px = px.loc[idx]
    sig = signal.reindex(idx).ffill().fillna(False).astype(bool)

    long_ret = px[long_etf].pct_change().fillna(0.0)
    red_ret = px[red_etf].pct_change().fillna(0.0) if red_etf else pd.Series(0.0, index=idx)

    held_long = sig.shift(1).fillna(False).astype(bool)         # position DURING day t
    strat_ret = long_ret.where(held_long, red_ret)

    switched = held_long.ne(held_long.shift(1))
    switched.iloc[0] = False                                     # day 0 has no prior state to switch from in-period
    # a switch = sell old + buy new = one round-trip's worth of cost
    cost = pd.Series(0.0, index=idx)
    cost.loc[switched] = cost_bps_round_trip / 1e4
    net_ret = strat_ret - cost
    equity = (1.0 + net_ret).cumprod()

    # trade log: contiguous runs of held_long (True = a 'long' trade in long_etf; False = a 'red'/'cash' leg)
    rows = []
    cur = held_long.iloc[0]
    seg_start = idx[0]
    prev_ts = idx[0]

    def _close_seg(side_long: bool, a: pd.Timestamp, b: pd.Timestamp):
        asset = long_etf if side_long else (red_etf or "CASH")
        if asset == "CASH":
            entry_px = exit_px = float("nan"); gross = 0.0
        else:
            entry_px = float(px.loc[a, asset]); exit_px = float(px.loc[b, asset]); gross = exit_px / entry_px - 1.0
        net = gross - (cost_bps_round_trip / 1e4 if side_long or asset != "CASH" else 0.0)   # one round-trip per traded leg; CASH leg costs nothing
        rows.append({"side": ("long" if side_long else ("red" if red_etf else "cash")), "asset": asset,
                     "entry_date": a, "exit_date": b, "days": (b - a).days,
                     "entry_px": entry_px, "exit_px": exit_px, "gross_ret": gross, "net_ret": net})

    for ts in idx[1:]:
        v = held_long.loc[ts]
        if v != cur:
            _close_seg(bool(cur), seg_start, prev_ts)
            cur, seg_start = v, ts
        prev_ts = ts
    _close_seg(bool(cur), seg_start, idx[-1])
    trades = pd.DataFrame(rows)

    return BacktestResult(equity=equity, daily_return=net_ret, signal=sig, trades=trades,
                          long_etf=long_etf, red_etf=red_etf, cost_bps_round_trip=cost_bps_round_trip,
                          params={"start": start, "end": end})
