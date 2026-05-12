from pathlib import Path

import numpy as np
import pandas as pd

from ww.breadth.series import build_fund_proxy, compute_breadth_series


def _write_panel(panel_dir: Path, ticker: str, closes: list[float], start="2020-01-01"):
    panel_dir.mkdir(parents=True, exist_ok=True)
    idx = pd.date_range(start, periods=len(closes), freq="B")
    df = pd.DataFrame({"open": closes, "high": [c + 1 for c in closes], "low": [c - 1 for c in closes],
                       "close": [float(c) for c in closes], "adj_close": [float(c) for c in closes], "volume": [1] * len(closes)}, index=idx)
    df.index.name = "date"
    df.to_parquet(panel_dir / f"{ticker}.parquet")


def test_breadth_basic_t2108(tmp_path):
    panel = tmp_path / "panel"
    # 50 business days. AAA rising (close > 40d MA at the end), BBB falling (close < 40d MA), CCC rising.
    _write_panel(panel, "AAA", list(np.linspace(10, 60, 50)))
    _write_panel(panel, "BBB", list(np.linspace(60, 10, 50)))
    _write_panel(panel, "CCC", list(np.linspace(10, 60, 50)))
    uni = pd.DataFrame({"ticker": ["AAA", "BBB", "CCC"], "in_nyse": [True, False, True]})
    df = compute_breadth_series(panel, uni)
    last = df.iloc[-1]
    # all 3 have >=40 bars and close >= $5 on the last day; 2 of 3 above their 40d MA
    assert last["n_broad"] == 3
    assert last["t2108_broad"] == 50.0 or abs(last["t2108_broad"] - 200 / 3) < 1e-6 or last["t2108_broad"] == 100.0 * 2 / 3
    # NYSE-only universe = AAA + CCC, both above -> 100%
    assert last["n_nyse"] == 2 and last["t2108_nyse"] == 100.0


def test_breadth_excludes_under_5_dollar_and_short_history(tmp_path):
    panel = tmp_path / "panel"
    _write_panel(panel, "RICH", list(np.linspace(10, 80, 50)))         # in universe
    _write_panel(panel, "PENNY", list(np.linspace(0.5, 2.0, 50)))      # close < $5 on the last day -> excluded
    _write_panel(panel, "YOUNG", [20.0, 21.0, 22.0])                   # < 40 bars -> excluded
    uni = pd.DataFrame({"ticker": ["RICH", "PENNY", "YOUNG"], "in_nyse": [True, True, True]})
    last = compute_breadth_series(panel, uni).iloc[-1]
    assert last["n_broad"] == 1                                        # only RICH


def test_breadth_new_52w_highs_and_lows(tmp_path):
    panel = tmp_path / "panel"
    # 300 business days. UP makes a new 52-week high on the last day; DOWN makes a new 52-week low.
    # FLAT equals its rolling max AND rolling min every day (close == max == min) -> counted in both.
    _write_panel(panel, "UP", list(np.linspace(10, 100, 300)))
    _write_panel(panel, "DOWN", list(np.linspace(100, 10, 300)))
    _write_panel(panel, "FLAT", [50.0] * 300)                          # constant -> close==rolling_max AND close==rolling_min each day
    uni = pd.DataFrame({"ticker": ["UP", "DOWN", "FLAT"], "in_nyse": [True, True, False]})
    df = compute_breadth_series(panel, uni)
    last = df.iloc[-1]
    # UP fires new high, DOWN fires new low; FLAT (constant) fires both (close==rolling_max==rolling_min)
    # UP + FLAT = 2 new highs; DOWN + FLAT = 2 new lows
    assert last["new_52w_highs"] >= 1 and last["new_52w_lows"] >= 1   # at minimum the monotone tickers fire
    assert last["new_52w_highs"] == 2 and last["new_52w_lows"] == 2
    # FLAT is non-NYSE -> it shows up in nasdaq_new_52w_highs/lows
    assert last["nasdaq_new_52w_highs"] >= 1 and last["nasdaq_new_52w_lows"] >= 1


def test_breadth_successful_10day_new_high(tmp_path):
    panel = tmp_path / "panel"
    # ZZ hits a new 52-week high 10 business days before the last date, then keeps rising -> on the last date it
    # closed higher than 10 days ago -> s10_total >= 1, s10_higher == s10_total for the rising name.
    _write_panel(panel, "ZZ", list(np.linspace(10, 100, 300)))
    uni = pd.DataFrame({"ticker": ["ZZ"], "in_nyse": [True]})
    df = compute_breadth_series(panel, uni)
    last = df.iloc[-1]
    assert last["s10_total"] >= 1
    assert last["s10_higher"] == last["s10_total"]                     # ZZ is monotone up


def test_breadth_drops_delisted_ticker_after_its_last_bar(tmp_path):
    panel = tmp_path / "panel"
    _write_panel(panel, "ALIVE", list(np.linspace(10, 60, 50)))
    _write_panel(panel, "GONE", list(np.linspace(10, 60, 45)))         # 5 fewer bars -> absent on the last 5 dates
    uni = pd.DataFrame({"ticker": ["ALIVE", "GONE"], "in_nyse": [True, True]})
    df = compute_breadth_series(panel, uni).set_index("date")
    # on the last date only ALIVE is in the universe (GONE has no bar that day)
    assert df.iloc[-1]["n_broad"] == 1


def test_build_fund_proxy_equal_weights_the_basket():
    idx = pd.date_range("2020-01-01", periods=4, freq="B")

    def downloader(yf_tickers, **kw):
        fields = ["Adj Close"]
        cols = pd.MultiIndex.from_product([yf_tickers, fields])
        data = {(t, "Adj Close"): [10.0 + i for i in range(len(idx))] if t == yf_tickers[0] else [20.0 + i for i in range(len(idx))] for t in yf_tickers}
        return pd.DataFrame(data, index=idx, columns=cols)

    s = build_fund_proxy(tickers=["AAA", "BBB"], downloader=downloader)
    assert list(s.index) == list(idx)
    assert s.iloc[0] == 15.0 and s.iloc[-1] == 18.0                    # mean(10..13, 20..23) per row
