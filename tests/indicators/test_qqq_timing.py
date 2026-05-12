import numpy as np
import pandas as pd

from ww.indicators.qqq_timing import short_term_trend, trend_day_count


def _close(values):
    return pd.Series([float(v) for v in values], index=pd.date_range("2024-01-01", periods=len(values), freq="B"))


def test_uptrend_when_close_above_30d_sma():
    assert short_term_trend(_close(list(np.linspace(100, 200, 80)))) == "up"


def test_downtrend_when_close_below_30d_sma():
    assert short_term_trend(_close(list(np.linspace(200, 100, 80)))) == "down"


def test_day_count_counts_days_since_the_last_flip():
    # 50 days down (close below rising-from-above... actually falling) then 10 days up
    closes = list(np.linspace(200, 120, 50)) + list(np.linspace(120, 170, 10))
    s = _close(closes)
    assert short_term_trend(s) == "up"
    # the up-trend is young — at most 10 days
    n = trend_day_count(s)
    assert 1 <= n <= 10
