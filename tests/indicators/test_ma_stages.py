import numpy as np
import pandas as pd

from ww.indicators.ma_stages import ma_alignment_4_10_30, sma, tenwk_below_thirtywk, weekly_stage


def _weekly(closes):
    return pd.Series(closes, index=pd.date_range("2018-01-07", periods=len(closes), freq="W-SUN"), dtype=float)


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
