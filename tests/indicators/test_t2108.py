import pandas as pd
import pytest

from ww.indicators.provider import DataUnavailable, StubProvider, YFinanceProvider
from ww.indicators.t2108 import t2108, t2108_from_prices


def _ohlc(closes):
    idx = pd.date_range("2020-01-01", periods=len(closes), freq="B")
    return pd.DataFrame({"open": closes, "high": closes, "low": closes, "close": [float(c) for c in closes]}, index=idx)


def test_t2108_from_prices_counts_pct_above_40d_ma():
    # AAA rising (above its 40d MA on the last day), BBB falling (below), CCC rising (above).
    aaa = _ohlc(list(range(1, 61)))                       # strictly increasing -> last close above MA
    bbb = _ohlc(list(range(60, 0, -1)))                   # strictly decreasing -> last close below MA
    ccc = _ohlc(list(range(1, 61)))
    frames = {"AAA": aaa, "BBB": bbb, "CCC": ccc}
    date = aaa.index[-1]
    pct = t2108_from_prices(frames, date, window=40)
    assert pct == pytest.approx(200 / 3)                  # 2 of 3 above -> 66.67%


def test_t2108_from_prices_skips_tickers_without_enough_history():
    long_ = _ohlc(list(range(1, 61)))
    short_ = _ohlc([1, 2, 3])                              # < window bars -> excluded from the denominator
    pct = t2108_from_prices({"L": long_, "S": short_}, long_.index[-1], window=40)
    assert pct == 100.0                                    # only L counted, and it's above its MA


def test_t2108_delegates_to_provider_pct_above_ma():
    sp = StubProvider(prices={}, pct_above_ma={(("A", "B"), 40, "2014-08-01"): 61.0})
    assert t2108(sp, "2014-08-01", universe=("A", "B"), window=40) == 61.0


def test_t2108_unavailable_with_free_provider():
    with pytest.raises(DataUnavailable):
        t2108(YFinanceProvider(), "2014-08-01", universe=("AAPL", "MSFT"))
