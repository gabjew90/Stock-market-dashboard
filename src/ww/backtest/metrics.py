"""Performance metrics for an equity curve, and comparison vs a benchmark. Pure pandas/numpy; no deps on the engine."""
from __future__ import annotations

import numpy as np
import pandas as pd

_TRADING_DAYS = 252


def daily_returns(equity: pd.Series) -> pd.Series:
    return equity.astype(float).pct_change().dropna()


def cagr(equity: pd.Series, *, periods_per_year: int = _TRADING_DAYS) -> float:
    eq = equity.astype(float).dropna()
    if len(eq) < 2:
        return 0.0
    years = (len(eq) - 1) / periods_per_year
    if years <= 0:
        return 0.0
    return float((eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1)


def max_drawdown(equity: pd.Series) -> float:
    eq = equity.astype(float).dropna()
    if eq.empty:
        return 0.0
    dd = eq / eq.cummax() - 1.0
    return float(dd.min())


def ann_vol(equity: pd.Series, *, periods_per_year: int = _TRADING_DAYS) -> float:
    r = daily_returns(equity)
    return float(r.std(ddof=1) * np.sqrt(periods_per_year)) if len(r) > 1 else 0.0


def sharpe(equity: pd.Series, *, periods_per_year: int = _TRADING_DAYS, rf: float = 0.0) -> float:
    r = daily_returns(equity) - rf / periods_per_year
    sd = r.std(ddof=1)
    return float(r.mean() / sd * np.sqrt(periods_per_year)) if sd > 0 else 0.0


def sortino(equity: pd.Series, *, periods_per_year: int = _TRADING_DAYS, rf: float = 0.0) -> float:
    r = daily_returns(equity) - rf / periods_per_year
    downside = r[r < 0]
    dd = downside.std(ddof=1) if len(downside) > 1 else 0.0
    return float(r.mean() / dd * np.sqrt(periods_per_year)) if dd > 0 else (float("inf") if r.mean() > 0 else 0.0)


def _long_runs(held_long: pd.Series) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Contiguous runs where held_long is True -> [(start, end), ...]."""
    s = held_long.fillna(False).astype(bool)
    runs, in_run, start = [], False, None
    prev = s.index[0]
    for ts, v in s.items():
        if v and not in_run:
            in_run, start = True, ts
        elif not v and in_run:
            in_run = False
            runs.append((start, prev))
        prev = ts
    if in_run:
        runs.append((start, prev))
    return runs


def performance(equity: pd.Series, *, signal: pd.Series | None = None, trades: pd.DataFrame | None = None,
                periods_per_year: int = _TRADING_DAYS) -> dict:
    """Headline + secondary metrics for an equity curve. If `signal` (the daily GREEN bool series) is given,
    also reports time-in-market and long-trade counts (held_long during day t = signal.shift(1))."""
    out = {
        "cagr": cagr(equity, periods_per_year=periods_per_year),
        "ann_vol": ann_vol(equity, periods_per_year=periods_per_year),
        "sharpe": sharpe(equity, periods_per_year=periods_per_year),
        "sortino": sortino(equity, periods_per_year=periods_per_year),
        "max_drawdown": max_drawdown(equity),
        "n_days": int(len(equity.dropna())),
    }
    md = out["max_drawdown"]
    out["calmar"] = float(out["cagr"] / abs(md)) if md != 0 else float("inf")
    if signal is not None:
        held = signal.reindex(equity.index).shift(1).fillna(False).astype(bool)
        # skip day-0: it is always False (no prior signal) and is a setup bar, not a trading day
        out["time_in_market"] = float(held.iloc[1:].mean()) if len(held) > 1 else float(held.mean())
        runs = _long_runs(held)
        out["n_long_trades"] = len(runs)
        out["avg_long_trade_days"] = float(np.mean([(b - a).days for a, b in runs])) if runs else 0.0
    if trades is not None and not trades.empty and "net_ret" in trades.columns:
        out["win_rate"] = float((trades["net_ret"] > 0).mean())
        out["worst_trade_net_ret"] = float(trades["net_ret"].min())
        out["best_trade_net_ret"] = float(trades["net_ret"].max())
    return out


def rolling_excess_cagr(strategy: pd.Series, benchmark: pd.Series, *, window_years: int = 5,
                        periods_per_year: int = _TRADING_DAYS) -> pd.Series:
    """Strategy CAGR minus benchmark CAGR over rolling `window_years`-windows, stamped at the window end."""
    n = window_years * periods_per_year
    idx = strategy.dropna().index.intersection(benchmark.dropna().index)
    s, b = strategy.reindex(idx), benchmark.reindex(idx)
    out = {}
    for i in range(n, len(idx)):
        win = idx[i - n : i + 1]
        out[idx[i]] = cagr(s.loc[win], periods_per_year=periods_per_year) - cagr(b.loc[win], periods_per_year=periods_per_year)
    return pd.Series(out)


def compare(strategy: pd.Series, benchmark: pd.Series, *, periods_per_year: int = _TRADING_DAYS) -> dict:
    idx = strategy.dropna().index.intersection(benchmark.dropna().index)
    s, b = strategy.reindex(idx), benchmark.reindex(idx)
    rs, rb = s.pct_change().dropna(), b.pct_change().dropna()
    j = rs.index.intersection(rb.index)
    rs, rb = rs.reindex(j), rb.reindex(j)
    diff = rs - rb
    ir = float(diff.mean() / diff.std(ddof=1) * np.sqrt(periods_per_year)) if diff.std(ddof=1) > 0 else 0.0
    up = rb > 0
    dn = rb < 0
    up_cap = float(rs[up].mean() / rb[up].mean()) if up.any() and rb[up].mean() != 0 else float("nan")
    dn_cap = float(rs[dn].mean() / rb[dn].mean()) if dn.any() and rb[dn].mean() != 0 else float("nan")
    return {
        "excess_cagr": cagr(s, periods_per_year=periods_per_year) - cagr(b, periods_per_year=periods_per_year),
        "information_ratio": ir,
        "up_capture": up_cap,
        "down_capture": dn_cap,
    }
