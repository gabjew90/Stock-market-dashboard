import numpy as np
import pandas as pd

from ww.backtest.metrics import compare, max_drawdown, performance


def _equity(returns):
    idx = pd.date_range("2010-01-01", periods=len(returns) + 1, freq="B")
    eq = pd.Series([1.0] + list((1 + pd.Series(returns)).cumprod()), index=idx)
    return eq


def test_max_drawdown():
    eq = pd.Series([1.0, 1.2, 0.9, 1.5, 1.2, 1.0], index=pd.date_range("2010-01-01", periods=6, freq="B"))
    # peak 1.5 -> trough 1.0  => -33.3%
    assert abs(max_drawdown(eq) - (-((1.5 - 1.0) / 1.5))) < 1e-12


def test_performance_on_a_flat_then_doubling_curve():
    # 252 business days at 0% then 252 at a daily rate that doubles -> ~1 year flat, 1 year +100% => ~2y, CAGR ~41.4%
    daily_up = 2 ** (1 / 252) - 1
    eq = _equity([0.0] * 252 + [daily_up] * 252)
    p = performance(eq, periods_per_year=252)
    assert abs(p["cagr"] - (2 ** (1 / 2) - 1)) < 1e-3        # ~0.4142
    assert p["max_drawdown"] == 0.0                           # never declined
    assert p["calmar"] == float("inf") or np.isinf(p["calmar"])
    assert p["ann_vol"] > 0


def test_performance_time_in_market_and_trades():
    eq = _equity([0.01, 0.0, 0.0, -0.005, 0.0, 0.0])
    sig = pd.Series([True, True, False, False, True, False, False], index=eq.index)  # held_long-during-day = sig.shift(1)
    p = performance(eq, signal=sig, periods_per_year=252)
    # held_long during days 1..6 = sig.shift(1) = [NaN,T,T,F,F,T,F] -> on days with a value: T,T,F,F,T,F -> 3 of 6 in-market
    assert abs(p["time_in_market"] - 0.5) < 1e-9
    # switches in held_long: F->T (day1, initial entry... held_long day0=NaN), T->F (day3), F->T (day5), T->F (day6) -> count the True-runs as trades: [T,T] then [T] -> 2 long trades
    assert p["n_long_trades"] == 2


def test_performance_sharpe_sortino_signs():
    rng = np.random.default_rng(0)
    rets = rng.normal(0.0005, 0.01, 600)                      # positive drift
    p = performance(_equity(rets), periods_per_year=252)
    assert p["sharpe"] > 0 and p["sortino"] > 0
    rets2 = rng.normal(-0.0005, 0.01, 600)                    # negative drift
    p2 = performance(_equity(rets2), periods_per_year=252)
    assert p2["sharpe"] < 0


def test_compare_excess_and_info_ratio():
    rng = np.random.default_rng(42)
    base_rets = rng.normal(0.001, 0.01, 300)
    strat_rets = base_rets + rng.normal(0.0005, 0.001, 300)   # consistently beats benchmark + noise -> IR > 0
    base = _equity(base_rets)
    strat = _equity(strat_rets)
    c = compare(strat, base)
    assert c["excess_cagr"] > 0
    assert c["information_ratio"] > 0
    # up-capture vs a positive-drift benchmark: strat consistently beats -> up_capture > 1
    assert c["up_capture"] > 1.0
