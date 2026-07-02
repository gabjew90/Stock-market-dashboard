import numpy as np
import pandas as pd

from ww.indicators.gmi import GMIResult, gmi
from ww.indicators.provider import StubProvider


def _uptrend_daily(n=400, lo=100, hi=300):
    idx = pd.date_range("2014-01-01", periods=n, freq="B")
    c = np.linspace(lo, hi, n)
    return pd.DataFrame({"open": c, "high": c, "low": c, "close": c}, index=idx)


def _uptrend_weekly(n=120, lo=100, hi=300):
    idx = pd.date_range("2014-01-05", periods=n, freq="W-SUN")
    c = np.linspace(lo, hi, n)
    return pd.DataFrame({"open": c, "high": c, "low": c, "close": c}, index=idx)


def test_full_gmi_six_when_everything_is_bullish():
    qd, qw, sd = _uptrend_daily(), _uptrend_weekly(), _uptrend_daily()
    fund = pd.Series(np.linspace(10, 30, 80), index=pd.date_range("2014-05-01", periods=80, freq="B"))
    sp = StubProvider(
        prices={("QQQ", "1d"): qd, ("QQQ", "1wk"): qw, ("SPY", "1d"): sd},
        nasdaq_new_highs_lows=pd.DataFrame({"new_highs": [350], "new_lows": [5]}, index=pd.to_datetime(["2014-08-01"])),
        successful_10day_new_high={"2014-08-01": (160, 200)},   # 80% >= 50% -> positive
        ibd_mutual_fund_index=fund,
    )
    r = gmi(sp, "2014-08-01")
    assert isinstance(r, GMIResult)
    assert r.score == 6
    assert r.unavailable == []
    assert all(v is True for v in r.components.values())


def test_partial_gmi_when_only_prices_available():
    qd, qw, sd = _uptrend_daily(), _uptrend_weekly(), _uptrend_daily()
    sp = StubProvider(prices={("QQQ", "1d"): qd, ("QQQ", "1wk"): qw, ("SPY", "1d"): sd})
    r = gmi(sp, "2014-08-01")
    # components 3,4,5 (QQQ daily, SPY daily, QQQ weekly) computable from prices -> True
    assert r.components["qqq_daily_trend"] is True
    assert r.components["spy_daily_trend"] is True
    assert r.components["qqq_weekly_trend"] is True
    # components 1,2,6 need breadth/fund data -> None, listed as unavailable
    for name in ("successful_10day_new_high", "new_highs_ge_100", "ibd_fund_above_50d"):
        assert r.components[name] is None
        assert name in r.unavailable
    assert r.score == 3


def test_component_1_original_2005_rule():
    qd, qw, sd = _uptrend_daily(), _uptrend_weekly(), _uptrend_daily()
    sp = StubProvider(prices={("QQQ", "1d"): qd, ("QQQ", "1wk"): qw, ("SPY", "1d"): sd},
                      successful_10day_new_high={"2014-08-01": (90, 1000)})  # 90 < 100 -> NEGATIVE under 2005 rule
    r = gmi(sp, "2014-08-01", original_rule=True)
    assert r.components["successful_10day_new_high"] is False
    # under the 2014 rule, 90/1000 = 9% < 50% -> also False; flip the test to a positive 2005 case:
    sp2 = StubProvider(prices={("QQQ", "1d"): qd, ("QQQ", "1wk"): qw, ("SPY", "1d"): sd},
                       successful_10day_new_high={"2014-08-01": (150, 1000)})  # 150 >= 100 -> POSITIVE (2005), but 15% < 50% (2014)
    assert gmi(sp2, "2014-08-01", original_rule=True).components["successful_10day_new_high"] is True
    assert gmi(sp2, "2014-08-01", original_rule=False).components["successful_10day_new_high"] is False


def test_price_components_respect_the_requested_date():
    # V-shaped series: bearish at the requested date (the bottom), bullish by the end.
    # Regression test — components 3/4/5 used to evaluate at the END of the provider's
    # series regardless of `date`, so a historical GMI borrowed today's trend.
    n = 400
    d_idx = pd.date_range("2014-01-01", periods=n, freq="B")
    c = np.concatenate([np.linspace(300, 100, n // 2), np.linspace(100, 500, n - n // 2)])
    qd = pd.DataFrame({"open": c, "high": c, "low": c, "close": c}, index=d_idx)
    bottom = d_idx[n // 2 - 1]
    w_idx = pd.date_range("2013-01-06", periods=160, freq="W-SUN")
    k = int((w_idx <= bottom).sum())
    wv = np.concatenate([np.linspace(300, 100, k), np.linspace(100, 500, 160 - k)])
    qw = pd.DataFrame({"open": wv, "high": wv, "low": wv, "close": wv}, index=w_idx)
    sp = StubProvider(prices={("QQQ", "1d"): qd, ("QQQ", "1wk"): qw, ("SPY", "1d"): qd})

    at_bottom = gmi(sp, bottom.date().isoformat())
    assert at_bottom.components["qqq_daily_trend"] is False
    assert at_bottom.components["spy_daily_trend"] is False
    assert at_bottom.components["qqq_weekly_trend"] is False

    at_end = gmi(sp, d_idx[-1].date().isoformat())
    assert at_end.components["qqq_daily_trend"] is True
    assert at_end.components["spy_daily_trend"] is True
    assert at_end.components["qqq_weekly_trend"] is True


def test_bearish_components_when_downtrend():
    dn_d = _uptrend_daily(lo=300, hi=100)
    dn_w = _uptrend_weekly(lo=300, hi=100)
    sp = StubProvider(prices={("QQQ", "1d"): dn_d, ("QQQ", "1wk"): dn_w, ("SPY", "1d"): dn_d},
                      nasdaq_new_highs_lows=pd.DataFrame({"new_highs": [20], "new_lows": [400]}, index=pd.to_datetime(["2014-08-01"])),
                      successful_10day_new_high={"2014-08-01": (10, 200)})
    r = gmi(sp, "2014-08-01")
    assert r.components["qqq_daily_trend"] is False
    assert r.components["new_highs_ge_100"] is False
    assert r.components["successful_10day_new_high"] is False
    assert r.score <= 1   # maybe ibd_fund unavailable -> None; the rest False
