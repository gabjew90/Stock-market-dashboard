import numpy as np
import pandas as pd

from ww.indicators.wgb import wgb_trailing_stop, weekly_green_bars


def _weekly_ohlc(closes, lows=None, highs=None):
    idx = pd.date_range("2020-01-05", periods=len(closes), freq="W-SUN")
    closes = [float(c) for c in closes]
    lows = [float(x) for x in (lows if lows is not None else [c * 0.97 for c in closes])]
    highs = [float(x) for x in (highs if highs is not None else [c * 1.02 for c in closes])]
    return pd.DataFrame({"open": closes, "high": highs, "low": lows, "close": closes}, index=idx)


def test_no_wgb_in_a_pure_downtrend():
    df = _weekly_ohlc(list(np.linspace(60, 10, 40)))
    assert weekly_green_bars(df).empty


def test_wgb_fires_on_a_pullback_bounce_inside_an_uptrend():
    # 35 weeks of steady uptrend, then a pullback week whose low pierces the 4wk avg
    # but whose close recovers above it, close > prior close, 4wk avg still rising.
    up = list(np.linspace(10, 50, 35))
    closes = up + [50.5]                       # week 36: close above prior, above the (rising) 4wk avg
    df = _weekly_ohlc(closes)
    # force week 36's low to dip to/just below its 4wk SMA of closes
    a4_last = pd.Series(closes, dtype=float).rolling(4).mean().iloc[-1]
    df.iloc[-1, df.columns.get_loc("low")] = a4_last - 0.01
    wgbs = weekly_green_bars(df)
    assert df.index[-1] in wgbs.index
    # the WGB row records that week's low for the trailing stop
    assert wgbs.loc[df.index[-1], "low"] == a4_last - 0.01


def test_wgb_requires_close_above_prior_close():
    up = list(np.linspace(10, 50, 35))
    closes = up + [49.0]                        # week 36 close is BELOW prior week's 50 -> condition C>C1 fails
    df = _weekly_ohlc(closes)
    a4_last = pd.Series(closes, dtype=float).rolling(4).mean().iloc[-1]
    df.iloc[-1, df.columns.get_loc("low")] = a4_last - 0.01
    assert df.index[-1] not in weekly_green_bars(df).index


def test_trailing_stop_is_low_of_most_recent_wgb():
    up = list(np.linspace(10, 50, 35))
    closes = up + [50.5]
    df = _weekly_ohlc(closes)
    a4_last = pd.Series(closes, dtype=float).rolling(4).mean().iloc[-1]
    df.iloc[-1, df.columns.get_loc("low")] = a4_last - 0.01
    assert wgb_trailing_stop(df) == a4_last - 0.01
    # no WGBs -> no stop
    assert wgb_trailing_stop(_weekly_ohlc(list(np.linspace(60, 10, 40)))) is None
