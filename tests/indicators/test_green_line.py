import pandas as pd

from ww.indicators.green_line import current_green_line, green_lines, is_green_line_breakout


def _monthly(highs, closes=None):
    idx = pd.date_range("2010-01-31", periods=len(highs), freq="ME")
    closes = closes if closes is not None else highs
    return pd.DataFrame({"high": highs, "close": closes, "low": [h * 0.9 for h in highs], "open": closes}, index=idx)


def test_green_lines_picks_ath_held_three_months():
    # Month 3 sets a new ATH of 50; months 4,5,6 stay below -> 50 is a green line.
    # Month 7 makes a new ATH of 80; months 8,9,10 stay below -> 80 is the next green line.
    highs = [10, 20, 50, 40, 45, 30, 80, 70, 60, 75, 90]
    df = _monthly(highs)
    gls = green_lines(df, min_months_held=3)
    levels = [lvl for _date, lvl in gls]
    assert 50 in levels and 80 in levels
    # 90 in the last month has not yet been held 3 months -> not a green line
    assert 90 not in levels


def test_current_green_line_is_the_most_recent_one():
    highs = [10, 20, 50, 40, 45, 30, 80, 70, 60, 75]
    cgl = current_green_line(_monthly(highs), min_months_held=3)
    assert cgl == 80


def test_no_green_line_when_always_making_new_highs():
    highs = [10, 20, 30, 40, 50, 60, 70]   # monotonic — no high ever holds for 3 months
    assert current_green_line(_monthly(highs), min_months_held=3) is None


def test_breakout_requires_close_above_the_line():
    highs = [10, 20, 50, 40, 45, 30, 48, 49]   # current green line = 50
    df = _monthly(highs, closes=[10, 20, 50, 40, 45, 30, 48, 49])
    cgl = current_green_line(df, min_months_held=3)
    assert cgl == 50
    assert is_green_line_breakout(close=51.0, green_line=cgl) is True
    assert is_green_line_breakout(close=50.0, green_line=cgl) is False   # must be strictly above
    assert is_green_line_breakout(close=49.0, green_line=cgl) is False
    assert is_green_line_breakout(close=51.0, green_line=None) is False
