import pandas as pd
import pytest

from ww.indicators.provider import DataProvider, DataUnavailable, StubProvider


def _ohlc(idx, closes):
    return pd.DataFrame({"open": closes, "high": closes, "low": closes, "close": closes, "volume": [1] * len(closes)}, index=idx)


def test_stub_provider_returns_injected_prices():
    idx = pd.date_range("2020-01-01", periods=5, freq="D")
    df = _ohlc(idx, [1.0, 2.0, 3.0, 4.0, 5.0])
    sp = StubProvider(prices={("AAPL", "1d"): df})
    out = sp.prices("AAPL", "1d")
    pd.testing.assert_frame_equal(out, df)


def test_stub_provider_missing_prices_raises_keyerror():
    sp = StubProvider(prices={})
    with pytest.raises(KeyError):
        sp.prices("AAPL", "1d")


def test_stub_provider_breadth_methods_default_to_unavailable():
    sp = StubProvider(prices={})
    with pytest.raises(DataUnavailable):
        sp.nasdaq_new_highs_lows("2020-01-01", "2020-02-01")
    with pytest.raises(DataUnavailable):
        sp.pct_above_ma(["AAPL"], 40, "2020-01-15")
    with pytest.raises(DataUnavailable):
        sp.ibd_mutual_fund_index("2020-01-01", "2020-02-01")


def test_stub_provider_can_supply_breadth_fixtures():
    s = pd.Series([6.0], index=pd.to_datetime(["2008-10-06"]))
    sp = StubProvider(prices={}, pct_above_ma={(("AAPL",), 40, "2008-10-06"): 6.0}, ibd_mutual_fund_index=s)
    assert sp.pct_above_ma(("AAPL",), 40, "2008-10-06") == 6.0
    pd.testing.assert_series_equal(sp.ibd_mutual_fund_index("2008-01-01", "2008-12-31"), s)


def test_dataprovider_is_abstract():
    with pytest.raises(TypeError):
        DataProvider()  # abstract — cannot instantiate
