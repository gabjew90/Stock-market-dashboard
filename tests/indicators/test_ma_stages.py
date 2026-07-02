import numpy as np
import pandas as pd

from ww.indicators.ma_stages import (
    ma_alignment_4_10_30,
    sma,
    tenwk_below_thirtywk,
    weekly_stage,
    weinstein_stage_series,
)


def _weekly(closes):
    return pd.Series(closes, index=pd.date_range("2018-01-07", periods=len(closes), freq="W-SUN"), dtype=float)


def _stage_series(daily_closes):
    """Run a daily close series through the same pipeline build_market_regime.py uses:
    W-FRI weekly closes -> 10/30wk SMAs -> ffill back onto the daily index -> stages."""
    s = pd.Series(daily_closes, index=pd.date_range("2015-01-05", periods=len(daily_closes), freq="B"), dtype=float)
    wk = s.resample("W-FRI").last().dropna()
    w10 = wk.rolling(10, min_periods=10).mean().reindex(s.index, method="ffill")
    w30 = wk.rolling(30, min_periods=30).mean().reindex(s.index, method="ffill")
    return s, weinstein_stage_series(s, w10, w30)


def test_sma_matches_pandas_rolling_mean():
    s = _weekly(list(range(1, 11)))
    pd.testing.assert_series_equal(sma(s, 3), s.rolling(3).mean())


def test_stage_2_when_price_above_rising_30wk():
    closes = list(np.linspace(10, 60, 40))     # steady uptrend, 40 weeks
    assert weekly_stage(_weekly(closes)) == 2


def test_stage_4_when_price_below_declining_30wk():
    closes = list(np.linspace(60, 10, 40))     # steady downtrend
    assert weekly_stage(_weekly(closes)) == 4


def test_stage_1_when_flat_and_at_or_below_ma():
    # Use a constant series so MA is genuinely flat (slope=0), last close just below the MA
    closes = [30.0] * 50
    s = _weekly(closes)
    s.iloc[-1] = float(sma(s, 30).iloc[-1]) - 0.01   # just below flat MA
    assert weekly_stage(s) == 1


def test_stage_3_when_high_but_ma_rolling_over():
    # Long uptrend, then price flattens for enough bars that the MA slope falls to zero (topping)
    # but price is still (barely) above the lagging MA
    up = list(np.linspace(10, 60, 200))
    flat_top = [60.0] * 25   # 25 flat bars -> MA catches up and flattens, close still above MA
    s = _weekly(up + flat_top)
    assert weekly_stage(s) == 3


def test_series_stage_2_in_confirmed_uptrend():
    # Long steady rise: price above a clearly-rising 30wk, 10wk above 30wk.
    _, st = _stage_series(np.linspace(100, 300, 750))
    assert st.iloc[-1] == 2


def test_series_stage_4_after_cross_down():
    # Long decline: price below falling 30wk, 10wk below 30wk.
    _, st = _stage_series(np.linspace(300, 100, 750))
    assert st.iloc[-1] == 4


def _daily_from_weekly(weekly_values, factor):
    """A daily series that steps once per week (Fridays), like a weekly SMA ffilled onto
    a daily index. `factor` scales relative to the base weekly path."""
    widx = pd.date_range("2015-01-09", periods=len(weekly_values), freq="W-FRI")
    didx = pd.date_range(widx[0], widx[-1], freq="B")
    return (pd.Series(weekly_values, index=widx, dtype=float) * factor).reindex(didx, method="ffill")


def test_series_recovery_above_ma_without_cross_is_stage_1_not_2():
    # Price back above a rising 30wk while the 10wk is still below it. Wish confirms
    # Stage 2 only on the weekly 10>30 cross (WW 2026-05-10), so this must read
    # Stage 1 (unconfirmed recovery), not Stage 2 — the April-2026 dashboard mislabel.
    w30_path = list(100 * (1.01 ** np.arange(20)))   # +1%/wk — rising, no curl
    w30 = _daily_from_weekly(w30_path, 1.0)
    w10 = _daily_from_weekly(w30_path, 0.98)          # 10wk 2% below the 30wk: cross not confirmed
    price = _daily_from_weekly(w30_path, 1.08)        # price 8% above the 30wk
    st = weinstein_stage_series(price, w10, w30)
    assert st.iloc[-1] == 1


def test_series_curl_down_fires_stage_3_despite_long_window_slope():
    # 30wk MA rose strongly then curled down in the last 3 weeks: the trailing 8-week
    # %-change still clears +1% (base effect), but the curl guard must force Stage 3
    # even with price above the MA and the 10wk above the 30wk.
    rising = list(100 * (1.01 ** np.arange(17)))
    curl = [rising[-1] * f for f in (0.999, 0.998, 0.997)]   # three slightly-down weekly updates
    w30 = _daily_from_weekly(rising + curl, 1.0)
    w10 = _daily_from_weekly(rising + curl, 1.05)
    price = _daily_from_weekly(rising + curl, 1.10)
    w30_weekly = w30[w30.ne(w30.shift())].dropna()
    slope8 = (w30_weekly.iloc[-1] / w30_weekly.iloc[-1 - 8] - 1.0) * 100.0
    assert slope8 > 1.0                                       # long-window slope still reads "rising"
    st = weinstein_stage_series(price, w10, w30)
    assert st.iloc[-1] == 3


def test_ma_alignment_true_when_4_above_10_above_30():
    closes = list(np.linspace(10, 60, 40))
    assert ma_alignment_4_10_30(_weekly(closes)) is True


def test_ma_alignment_false_in_downtrend():
    closes = list(np.linspace(60, 10, 40))
    assert ma_alignment_4_10_30(_weekly(closes)) is False


def test_tenwk_below_thirtywk_detects_the_cross():
    s = _weekly(list(np.linspace(60, 10, 40)))
    assert tenwk_below_thirtywk(s) is True
    s2 = _weekly(list(np.linspace(10, 60, 40)))
    assert tenwk_below_thirtywk(s2) is False
