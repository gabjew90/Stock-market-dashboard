"""The degraded-tail guard: don't append a session the upstream feed hasn't published.

Regression for 2026-09-02, when Yahoo had not posted the session for the market but 283
stray tickers reported a bar. n_nyse came back 283 against a normal ~1,920, T2108 read
39% off 15% of the universe, and the deploy failed on the freshness guardrail instead of
simply shipping the previous good day.
"""
import pandas as pd

from ww.breadth.series import drop_degraded_tail


def _series(coverage, start="2026-06-01"):
    idx = pd.bdate_range(start, periods=len(coverage))
    return pd.DataFrame({"date": idx, "n_broad": coverage, "t2108_broad": [50.0] * len(coverage)})


def test_drops_the_collapsed_final_session():
    df = _series([3000] * 40 + [283])
    kept, dropped = drop_degraded_tail(df)
    assert len(kept) == 40
    assert dropped == [str(df["date"].iloc[-1].date())]


def test_keeps_a_healthy_final_session():
    df = _series([3000] * 40 + [2950])
    kept, dropped = drop_degraded_tail(df)
    assert len(kept) == 41 and dropped == []


def test_keeps_an_ordinary_dip_that_is_not_a_collapse():
    """Holidays and thin sessions shrink coverage a little; only a collapse counts."""
    df = _series([3000] * 40 + [2100])          # 70% of normal - still usable
    kept, dropped = drop_degraded_tail(df)
    assert dropped == [] and len(kept) == 41


def test_never_touches_history_only_the_tail():
    """The mistake this guard must never repeat: a mid-series dip is data, not damage."""
    cov = [3000] * 20 + [200] + [3000] * 20     # one bad day in the middle, healthy end
    df = _series(cov)
    kept, dropped = drop_degraded_tail(df)
    assert dropped == []
    assert len(kept) == len(df), "a healthy final session must protect everything before it"


def test_early_history_with_a_legitimately_smaller_universe_is_untouched():
    """The reconstructed universe grows over time - 2008 sits near 900 against ~1,900 now.
    An absolute floor would delete eleven years of real history; the test is relative."""
    cov = list(range(900, 900 + 400 * 4, 4))    # steadily growing, never collapsing
    df = _series(cov, start="2008-02-29")
    kept, dropped = drop_degraded_tail(df)
    assert dropped == [] and len(kept) == len(df)


def test_drops_a_multi_day_outage_while_the_norm_still_holds():
    df = _series([3000] * 40 + [100] * 3)
    kept, dropped = drop_degraded_tail(df)
    assert len(dropped) == 3 and len(kept) == 40


def test_drops_at_most_max_drop_rows():
    df = _series([3000] * 40 + [100] * 8)
    kept, dropped = drop_degraded_tail(df, max_drop=5)
    assert len(dropped) == 5, "the cap must bound the damage even in a sustained outage"
    assert len(kept) == len(df) - 5


def test_a_sustained_outage_eventually_becomes_the_norm():
    """A documented limit, not an accident. Once degraded sessions outnumber the lookback
    window they ARE the local norm and the relative test stops firing. That is acceptable
    because the guard runs per-update against a stored series whose earlier rows are good:
    each run drops its own bad day and the series simply stops advancing. It also means the
    guard can never mistake a long, real change in universe size for an outage."""
    df = _series([3000] * 40 + [100] * 25)
    kept, dropped = drop_degraded_tail(df)
    assert dropped == []


def test_handles_short_and_empty_input():
    kept, dropped = drop_degraded_tail(pd.DataFrame())
    assert kept.empty and dropped == []
    kept, dropped = drop_degraded_tail(_series([3000]))
    assert dropped == [] and len(kept) == 1


def test_missing_coverage_column_is_a_no_op():
    df = _series([3000] * 10).drop(columns=["n_broad"])
    kept, dropped = drop_degraded_tail(df)
    assert dropped == [] and len(kept) == 10


def test_the_2026_09_02_shape_end_to_end():
    """The real numbers from the failure."""
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-08-26", "2026-08-27", "2026-08-28",
                                "2026-08-31", "2026-09-01", "2026-09-02"]),
        "n_broad": [4700, 4690, 4685, 4680, 4675, 634],
        "n_nyse": [1930, 1926, 1923, 1923, 1922, 283],
    })
    kept, dropped = drop_degraded_tail(df, lookback=5)
    assert dropped == ["2026-09-02"]
    assert kept["date"].max() == pd.Timestamp("2026-09-01")
    assert int(kept["n_nyse"].min()) >= 1922
