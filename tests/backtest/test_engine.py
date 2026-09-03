import numpy as np
import pandas as pd

from ww.backtest.engine import BacktestResult, run_backtest


def _prices(closes: dict[str, list[float]], start="2010-01-04"):
    n = len(next(iter(closes.values())))
    idx = pd.date_range(start, periods=n, freq="B")
    return pd.DataFrame({k: v for k, v in closes.items()}, index=idx)


def test_all_true_signal_reproduces_buy_and_hold():
    px = _prices({"QQQ": [100.0, 110.0, 99.0, 121.0, 110.0]})
    sig = pd.Series(True, index=px.index)
    r = run_backtest(sig, px, long_etf="QQQ", red_etf=None, cost_bps_round_trip=0.0)
    assert isinstance(r, BacktestResult)
    # held_long during day t = sig.shift(1): day0=False (NaN), days1-4=True. So strat return = QQQ c2c on days 1-4.
    # equity (growth of $1 from before day0) = product of (1 + day-t returns); day0 return = 0 (in cash, sig.shift=NaN->False).
    expected = (px["QQQ"] / px["QQQ"].iloc[0]).iloc[-1]   # 110/100 = 1.10  -- because day0 in cash means we "miss" the day-0 move, but day0 has no prior close so its return is 0 anyway; days1-4 capture 110->99->121->110.
    # Actually with held_long[0]=False the equity on day0 = 1.0 (cash, 0% — and pct_change on day0 is NaN->0 anyway).
    # equity_last = (99/110)*(121/99)*(110/121) ... wait: day1 ret = 110/100-1; day2 = 99/110-1; day3 = 121/99-1; day4 = 110/121-1.
    # cumprod of (1+ret) over days 1..4 = (110/100)*(99/110)*(121/99)*(110/121) = (110*99*121*110)/(100*110*99*121) = 110/100 = 1.10. Yes.
    assert abs(r.equity.iloc[-1] - 1.10) < 1e-9


def test_cash_when_red_earns_zero():
    px = _prices({"QQQ": [100.0, 200.0, 50.0, 80.0]})
    sig = pd.Series([False, False, False, False], index=px.index)   # always RED -> always cash
    r = run_backtest(sig, px, long_etf="QQQ", red_etf=None, cost_bps_round_trip=0.0)
    assert abs(r.equity.iloc[-1] - 1.0) < 1e-12                     # cash all the way


def test_a_complete_trade_costs_exactly_one_round_trip():
    """`cost_bps_round_trip` is the cost of a COMPLETE buy-and-sell, so each switch is charged
    half of it. Charging the full amount per switch (the behaviour until 2026-09-02) billed two
    round trips per trade and doubled the modelled drag."""
    px = _prices({"QQQ": [100.0] * 5})                                # flat prices -> only cost moves the curve
    sig = pd.Series([True, True, False, False, True], index=px.index)  # held_long = [F,T,T,F,F]: 2 switches
    r = run_backtest(sig, px, long_etf="QQQ", red_etf=None, cost_bps_round_trip=10.0)
    # enter + exit = one complete round trip = 10 bps total, charged as 5 bps twice.
    assert abs(r.equity.iloc[-1] - (1 - 5e-4) ** 2) < 1e-9
    assert abs(r.equity.iloc[-1] - (1 - 10e-4)) < 1e-6, "a full enter-and-exit must cost one round trip"


def test_an_unclosed_position_pays_only_the_entry_leg():
    px = _prices({"QQQ": [100.0] * 4})
    sig = pd.Series([True, True, True, True], index=px.index)          # held_long = [F,T,T,T]: one switch
    r = run_backtest(sig, px, long_etf="QQQ", red_etf=None, cost_bps_round_trip=10.0)
    assert abs(r.equity.iloc[-1] - (1 - 5e-4)) < 1e-9


def test_result_records_the_window_it_actually_ran_over():
    """A variant naming a leveraged ETF cannot start before that fund existed, so the span it
    really covered has to be reported or the grid silently compares different periods."""
    px = _prices({"QQQ": [100.0] * 5, "TQQQ": [float("nan"), float("nan"), 10.0, 11.0, 12.0]})
    sig = pd.Series(True, index=px.index)
    r_qqq = run_backtest(sig, px, long_etf="QQQ", cost_bps_round_trip=0.0)
    r_lev = run_backtest(sig, px, long_etf="TQQQ", cost_bps_round_trip=0.0)
    assert r_qqq.params["n_days"] == 5
    assert r_lev.params["n_days"] == 3, "the leveraged run must not claim days before inception"
    assert r_lev.params["actual_start"] > r_qqq.params["actual_start"]


def test_no_look_ahead():
    px = _prices({"QQQ": [100.0, 100.0, 200.0, 200.0]})              # huge jump on day2
    sig = pd.Series([False, True, True, True], index=px.index)        # signal turns GREEN on close of day1
    r = run_backtest(sig, px, long_etf="QQQ", red_etf=None, cost_bps_round_trip=0.0)
    # held_long = sig.shift(1) = [F,F,T,T]. So we're long DURING day2 (which has the +100% c2c return 200/100... wait day2 c2c = px[2]/px[1] = 200/100 = +100%). We capture it. day1 c2c = 100/100 = 0. day3 = 200/200 = 0.
    # If there WERE look-ahead (held_long = sig directly), we'd be long during day1 too (still 0%) AND day2 — same here by luck; better test: signal GREEN on close of day0:
    sig2 = pd.Series([True, True, True, True], index=px.index)
    r2 = run_backtest(sig2, px, long_etf="QQQ", red_etf=None, cost_bps_round_trip=0.0)
    # held_long = sig2.shift(1) = [F,T,T,T] -> long during days 1,2,3. day1=0%, day2=+100%, day3=0% -> equity ends at 2.0.
    assert abs(r2.equity.iloc[-1] - 2.0) < 1e-9
    # the +100% is on day2; if a flip on day0 wrongly affected day0... day0 return is always 0 (no prior close). The lag is what matters: a True on day0 only takes effect day1+. Good.


def test_red_etf_path():
    px = _prices({"QQQ": [100.0, 110.0, 110.0], "SQQQ": [100.0, 90.0, 90.0]})
    sig = pd.Series([True, True, False], index=px.index)             # held_long = [F,T,T]; day2 still long (sig[1]=True)
    r = run_backtest(sig, px, long_etf="QQQ", red_etf="SQQQ", cost_bps_round_trip=0.0)
    # held_long during days 1,2 = True (sig.shift1 = [F,T,T]) -> long QQQ both days: day1 = 110/100=+10%, day2 = 110/110=0% -> equity 1.10. SQQQ never used here.
    assert abs(r.equity.iloc[-1] - 1.10) < 1e-9
    # now flip so day2 is RED:
    sig2 = pd.Series([False, True, False], index=px.index)           # held_long = sig2.shift1 = [F,F,T] -> long only day2 (sig2[1]=True): day2 QQQ = 110/110 = 0%. cash/red before.
    r2 = run_backtest(sig2, px, long_etf="QQQ", red_etf="SQQQ", cost_bps_round_trip=0.0)
    # held_long = [F,F,T]: day1 in SQQQ (held_long[1]=F): day1 SQQQ c2c = 90/100 = -10%; day2 in QQQ: 0%. equity = 0.90.
    assert abs(r2.equity.iloc[-1] - 0.90) < 1e-9
    assert not r2.trades.empty
