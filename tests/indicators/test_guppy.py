import numpy as np
import pandas as pd

from ww.indicators.guppy import gmma, red_line_count, rwb_state

SHORT = (3, 5, 8, 10, 12, 15)


def _close(values):
    return pd.Series([float(v) for v in values], index=pd.date_range("2020-01-01", periods=len(values), freq="D"))


def test_gmma_has_twelve_columns():
    g = gmma(_close(list(np.linspace(10, 100, 200))))
    assert len(g.columns) == 12
    # short EMAs come first, in order
    assert list(g.columns)[:6] == [f"ema{p}" for p in SHORT]


def test_rwb_state_in_a_long_uptrend():
    assert rwb_state(_close(list(np.linspace(10, 100, 250)))) == "RWB"


def test_rwb_state_in_a_long_downtrend():
    assert rwb_state(_close(list(np.linspace(100, 10, 250)))) == "BWR"


def test_rwb_state_transition_when_bands_overlap():
    # Long uptrend, then a sharp decline, then a bounce — the bounce interrupts the falling condition
    # so it's neither RWB nor BWR (bands still separated but direction is unclear)
    up = list(np.linspace(10, 100, 200))
    down = list(np.linspace(100, 40, 30))
    bounce = [50.0] * 10   # bounce breaks the "all EMAs falling" condition
    vals = up + down + bounce
    assert rwb_state(_close(vals)) == "transition"


def test_red_line_count_full_in_uptrend_zero_in_downtrend():
    assert red_line_count(_close(list(np.linspace(10, 100, 250)))) == 6
    assert red_line_count(_close(list(np.linspace(100, 10, 250)))) == 0
