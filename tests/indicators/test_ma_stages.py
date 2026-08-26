import numpy as np
import pandas as pd

from ww.indicators.ma_stages import (
    _slope_state_weekly,
    classify_stage,
    is_stage2,
    ma_alignment_4_10_30,
    sma,
    stage_series,
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


# ---------------------------------------------------------------------------
# Stage 4 needs BOTH of his conditions (WW 2015-09-20):
#   "When the 10 week average falls below the 30 week average *and* the 30 week
#    average turns down, that index is in a Stage 4 down-trend."
# ---------------------------------------------------------------------------

def test_stage_4_needs_the_falling_average_not_just_the_cross():
    """A sharp drop puts price and the 10wk under a 30wk that is still rising. That is a
    Stage-4 *setup*, not Stage 4 - the average has not turned down."""
    w30_path = list(100 * (1.01 ** np.arange(20)))    # still rising +1%/wk
    w30 = _daily_from_weekly(w30_path, 1.0)
    w10 = _daily_from_weekly(w30_path, 0.97)          # 10wk below 30wk: the cross HAS fired
    price = _daily_from_weekly(w30_path, 0.90)        # price 10% below the 30wk
    st = weinstein_stage_series(price, w10, w30)
    assert st.iloc[-1] != 4, "the 30-week is still rising - his second condition is unmet"
    assert st.iloc[-1] == 3


def test_stage_4_when_both_conditions_are_met():
    w30_path = list(100 * (0.99 ** np.arange(20)))    # falling ~1%/wk
    w30 = _daily_from_weekly(w30_path, 1.0)
    w10 = _daily_from_weekly(w30_path, 0.97)
    price = _daily_from_weekly(w30_path, 0.90)
    st = weinstein_stage_series(price, w10, w30)
    assert st.iloc[-1] == 4


# ---------------------------------------------------------------------------
# Stage 1 - "consolidating near or below its 30-week average after a prior
# decline. The average is roughly flat."
# ---------------------------------------------------------------------------

def test_stage_1_for_a_flat_average_with_price_below_it():
    """The base. Before the three-way slope was restored this produced Stage 4, because
    'flat' and 'falling' were the same boolean."""
    w30_path = [100.0] * 20                            # dead flat
    w30 = _daily_from_weekly(w30_path, 1.0)
    w10 = _daily_from_weekly(w30_path, 0.98)           # 10wk still below: no cross back yet
    price = _daily_from_weekly(w30_path, 0.97)         # price just under the flat average
    st = weinstein_stage_series(price, w10, w30)
    assert st.iloc[-1] == 1


def test_stage_1_for_a_recovery_above_a_still_falling_average():
    """Price back above the 30-week while the average still falls and the 10wk has not
    crossed back - the May-2009 shape. Topping is the one thing this is not."""
    w30_path = list(100 * (0.99 ** np.arange(20)))
    w30 = _daily_from_weekly(w30_path, 1.0)
    w10 = _daily_from_weekly(w30_path, 0.95)
    price = _daily_from_weekly(w30_path, 1.12)         # 12% above the falling average
    st = weinstein_stage_series(price, w10, w30)
    assert st.iloc[-1] == 1


def test_a_flat_average_is_never_stage_4():
    """The regression that motivated the three-way slope: with a boolean 'rising?' test,
    every flat-average day fell through to the falling branch."""
    w30 = _daily_from_weekly([100.0] * 20, 1.0)
    w10 = _daily_from_weekly([100.0] * 20, 0.98)
    for factor in (0.90, 0.97, 1.0):
        st = weinstein_stage_series(_daily_from_weekly([100.0] * 20, factor), w10, w30)
        assert st.iloc[-1] != 4, f"flat average must not read Stage 4 (price factor {factor})"


# ---------------------------------------------------------------------------
# One rule, three callers.
# ---------------------------------------------------------------------------

def test_weekly_stage_and_stage_series_cannot_disagree():
    """`ww compute` (weekly_stage) and the dashboard (stage_series) route through the same
    classify_stage(). They used to be separate implementations agreeing on only 85% of weeks."""
    rng = np.random.default_rng(0)
    path = 100 * np.exp(np.cumsum(rng.normal(0.001, 0.03, 400)))
    s = pd.Series(path, index=pd.date_range("2015-01-04", periods=400, freq="W-SUN"), dtype=float)
    for cut in range(60, len(s), 17):
        window = s.iloc[:cut]
        series_call = stage_series(window, sma(window, 10), sma(window, 30)).iloc[-1]
        assert weekly_stage(window) == series_call, f"disagreement at week {cut}"


def test_is_stage2_is_the_stage_series_definition():
    _, st = _stage_series(np.linspace(100, 300, 750))
    s = pd.Series(np.linspace(100, 300, 750), index=pd.date_range("2015-01-05", periods=750, freq="B"), dtype=float)
    wk = s.resample("W-FRI").last().dropna()
    w10 = wk.rolling(10, min_periods=10).mean().reindex(s.index, method="ffill")
    w30 = wk.rolling(30, min_periods=30).mean().reindex(s.index, method="ffill")
    pd.testing.assert_series_equal(is_stage2(s, w10, w30), st == 2)


def test_stage_series_is_a_sequential_application_of_classify_stage():
    """stage_series() must be exactly classify_stage() walked forward with the prior bar - no
    second copy of the rule, which is how the earlier Stage-2 definitions drifted apart."""
    rng = np.random.default_rng(7)
    path = 100 * np.exp(np.cumsum(rng.normal(0.0, 0.035, 900)))
    s = pd.Series(path, index=pd.date_range("2010-01-04", periods=900, freq="B"), dtype=float)
    wk = s.resample("W-FRI").last().dropna()
    w10 = wk.rolling(10, min_periods=10).mean().reindex(s.index, method="ffill")
    w30 = wk.rolling(30, min_periods=30).mean().reindex(s.index, method="ffill")
    st = stage_series(s, w10, w30)

    w30_weekly = w30[w30.ne(w30.shift())].dropna()
    slope = _slope_state_weekly(w30_weekly, slope_window_weeks=8, flat_band_pct=1.0,
                                curl_window_weeks=2).reindex(s.index, method="ffill").fillna(0).astype(int)
    above = (s > w30).fillna(False).astype(bool)
    ten = (w10 > w30).fillna(False).astype(bool)
    deep = (s < w30 * 0.95).fillna(False).astype(bool)
    shallow = ~deep.rolling(5, min_periods=1).max().astype(bool)
    prior = 0
    seen = set()
    for i in range(len(s)):
        args = dict(above_30wk=bool(above.iloc[i]), slope=int(slope.iloc[i]),
                    ten_above_thirty=bool(ten.iloc[i]), shallow_below=bool(shallow.iloc[i]),
                    prior_stage=prior)
        prior = classify_stage(**args)
        assert prior == int(st.iloc[i]), f"row {i}: {args}"
        seen.add((args["above_30wk"], args["slope"], args["ten_above_thirty"]))
    assert len(seen) >= 6, f"weak coverage - only exercised {len(seen)} input combinations"


def test_a_flat_average_reads_as_topping_after_an_advance_and_basing_after_a_decline():
    """The same instantaneous reading, opposite meanings - which is why prior_stage exists."""
    common = dict(above_30wk=False, slope=0, ten_above_thirty=False, shallow_below=True)
    assert classify_stage(**common, prior_stage=2) == 3      # flattening out of an advance = top
    assert classify_stage(**common, prior_stage=3) == 3      # still topping
    assert classify_stage(**common, prior_stage=4) == 1      # flattening out of a decline = base
    assert classify_stage(**common, prior_stage=1) == 1      # still basing
