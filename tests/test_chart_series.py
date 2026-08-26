"""Unit tests for the candle-chart series builder in scripts/build_market_regime.py.

The full build can't run here (it needs the gitignored data/ caches), so these
exercise the pure computation: which averages are emitted, on what history, and
what happens on a session with no print.
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "build_market_regime", ROOT / "scripts" / "build_market_regime.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bmr = _load_module()


@pytest.fixture
def synth():
    """400 business days of a gently rising series, with OHLC + volume."""
    idx = pd.date_range("2020-01-01", periods=400, freq="B")
    close = pd.Series(np.linspace(100.0, 200.0, len(idx)), index=idx)
    ohlc = pd.DataFrame({
        "open": close - 0.5,
        "high": close + 1.0,
        "low": close - 1.0,
        "close": close,
        "volume": pd.Series(np.full(len(idx), 1_000_000.0), index=idx),
    }, index=idx)
    state = pd.Series(1, index=idx)
    return idx, close, ohlc, state


def test_daily_emits_every_requested_average(synth):
    idx, close, ohlc, state = synth
    out = bmr._chart_series(close, ohlc, idx, state, "2020-01-01")
    last = out["daily"][-1]
    for key in ("o", "h", "l", "cl", "v", "e21", "m30", "m50", "m200", "vm50"):
        assert key in last, f"daily row missing {key}"
        assert last[key] is not None, f"daily {key} is None on the last bar"


def test_weekly_emits_ten_and_thirty_week(synth):
    idx, close, ohlc, state = synth
    out = bmr._chart_series(close, ohlc, idx, state, "2020-01-01")
    last = out["weekly"][-1]
    for key in ("o", "h", "l", "c", "v", "m10", "m30", "vm50"):
        assert key in last, f"weekly row missing {key}"
    assert last["m10"] is not None and last["m30"] is not None


def test_moving_averages_match_an_independent_computation(synth):
    idx, close, ohlc, state = synth
    out = bmr._chart_series(close, ohlc, idx, state, "2020-01-01")
    last = out["daily"][-1]
    assert last["m30"] == pytest.approx(round(close.rolling(30).mean().iloc[-1], 2))
    assert last["m50"] == pytest.approx(round(close.rolling(50).mean().iloc[-1], 2))
    assert last["m200"] == pytest.approx(round(close.rolling(200).mean().iloc[-1], 2))
    ema = close.ewm(span=21, adjust=False, min_periods=21).mean()
    assert last["e21"] == pytest.approx(round(ema.iloc[-1], 2))


def test_averages_use_history_from_before_the_visible_window(synth):
    """The 200-day mean must be warm on the FIRST visible bar, not ramp up from it.

    Slicing before averaging would leave the first ~200 rows of the chart with a
    null 200-day line even though the underlying history is there.
    """
    idx, close, ohlc, state = synth
    start = idx[300].strftime("%Y-%m-%d")
    out = bmr._chart_series(close, ohlc, idx, state, start)
    first = out["daily"][0]
    assert first["m200"] is not None, "200-day SMA should already be warm at the window edge"
    assert first["m200"] == pytest.approx(round(close.rolling(200).mean().loc[idx[300]], 2))


def test_volume_average_is_a_50_period_mean(synth):
    idx, close, ohlc, state = synth
    vol = ohlc["volume"].copy()
    vol.iloc[-50:] = 2_000_000.0            # last 50 bars at double volume
    ohlc = ohlc.assign(volume=vol)
    out = bmr._chart_series(close, ohlc, idx, state, "2020-01-01")
    assert out["daily"][-1]["vm50"] == pytest.approx(2_000_000, rel=1e-6)


def test_missing_session_leaves_the_candle_empty_rather_than_repeating_yesterday(synth):
    """A date with no print must emit nulls, not the prior bar forward-filled —
    otherwise the renderer draws a duplicate body (and can colour it wrongly)."""
    idx, close, ohlc, state = synth
    gap = idx[-3]
    out = bmr._chart_series(close, ohlc.drop(index=gap), idx, state, "2020-01-01")
    row = next(r for r in out["daily"] if r["d"] == gap.strftime("%Y-%m-%d"))
    assert row["o"] is None and row["h"] is None and row["l"] is None and row["cl"] is None
    assert row["m30"] is not None, "MAs come from the close series and should survive the gap"


def test_weekly_volume_average_uses_weekly_totals(synth):
    idx, close, ohlc, state = synth
    out = bmr._chart_series(close, ohlc, idx, state, "2020-01-01")
    wk = out["weekly"]
    full = [w for w in wk if w["v"] == 5_000_000]      # a full 5-session week
    assert full, "expected at least one complete 5-session week"
    assert wk[-1]["vm50"] is not None


def test_both_chart_symbols_are_declared():
    assert bmr.CHART_SYMBOLS[0] == "QQQ", "QQQ must stay the default — indicators are QQQ-derived"
    assert "SPY" in bmr.CHART_SYMBOLS
    assert set(bmr._OHLC_CACHES) == set(bmr.CHART_SYMBOLS)
