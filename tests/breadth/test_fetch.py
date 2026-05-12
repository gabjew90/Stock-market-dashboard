from pathlib import Path

import pandas as pd

from ww.breadth.fetch import fetch_panel, normalize_for_yf, update_panel


def test_normalize_for_yf():
    assert normalize_for_yf("BRK.B") == "BRK-B"
    assert normalize_for_yf("BAC.A") == "BAC-A"
    assert normalize_for_yf("AAPL") == "AAPL"


def _fake_frame(tickers, dates, base=10.0):
    """A yfinance-style multi-ticker frame: columns = MultiIndex (ticker, field)."""
    fields = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    cols = pd.MultiIndex.from_product([tickers, fields])
    data = {}
    for i, t in enumerate(tickers):
        c = [base + i + j for j in range(len(dates))]
        data[(t, "Open")] = c; data[(t, "High")] = [x + 1 for x in c]; data[(t, "Low")] = [x - 1 for x in c]
        data[(t, "Close")] = c; data[(t, "Adj Close")] = c; data[(t, "Volume")] = [1000] * len(dates)
    return pd.DataFrame(data, index=pd.DatetimeIndex(dates), columns=cols)


def test_fetch_panel_writes_per_ticker_parquet(tmp_path):
    uni = pd.DataFrame({"ticker": ["AAA", "BBB"], "in_nyse": [True, False]})
    dates = pd.date_range("2020-01-02", periods=5, freq="B")

    def downloader(yf_tickers, **kw):
        return _fake_frame(yf_tickers, dates)

    n = fetch_panel(uni, tmp_path / "panel", downloader=downloader, batch_size=10)
    assert n == 2
    a = pd.read_parquet(tmp_path / "panel" / "AAA.parquet")
    assert list(a.columns) == ["open", "high", "low", "close", "adj_close", "volume"]
    assert len(a) == 5 and a.index[0] == pd.Timestamp("2020-01-02")


def test_fetch_panel_skips_existing_unless_force(tmp_path):
    uni = pd.DataFrame({"ticker": ["AAA"], "in_nyse": [True]})
    dates = pd.date_range("2020-01-02", periods=3, freq="B")
    calls = []

    def downloader(yf_tickers, **kw):
        calls.append(list(yf_tickers))
        return _fake_frame(yf_tickers, dates)

    fetch_panel(uni, tmp_path / "panel", downloader=downloader)
    assert calls == [["AAA"]]
    fetch_panel(uni, tmp_path / "panel", downloader=downloader)         # second run: skipped
    assert calls == [["AAA"]]
    fetch_panel(uni, tmp_path / "panel", downloader=downloader, force=True)
    assert calls == [["AAA"], ["AAA"]]


def test_fetch_panel_skips_ticker_with_no_data(tmp_path):
    uni = pd.DataFrame({"ticker": ["GOOD", "DEAD"], "in_nyse": [True, True]})
    dates = pd.date_range("2020-01-02", periods=3, freq="B")

    def downloader(yf_tickers, **kw):
        f = _fake_frame(["GOOD"], dates)            # only GOOD comes back
        return f

    n = fetch_panel(uni, tmp_path / "panel", downloader=downloader)
    assert n == 1
    assert (tmp_path / "panel" / "GOOD.parquet").exists()
    assert not (tmp_path / "panel" / "DEAD.parquet").exists()


def test_update_panel_appends_new_rows_deduped(tmp_path):
    panel = tmp_path / "panel"; panel.mkdir(parents=True)
    old = pd.DataFrame({"open": [10, 11], "high": [11, 12], "low": [9, 10], "close": [10, 11], "adj_close": [10, 11], "volume": [1, 1]},
                       index=pd.DatetimeIndex(["2020-01-02", "2020-01-03"]))
    old.to_parquet(panel / "AAA.parquet")
    uni = pd.DataFrame({"ticker": ["AAA"], "in_nyse": [True]})
    new_dates = pd.date_range("2020-01-03", periods=3, freq="B")       # overlaps 01-03, adds 01-06, 01-07

    def downloader(yf_tickers, **kw):
        return _fake_frame(yf_tickers, new_dates, base=99.0)

    update_panel(uni, panel, downloader=downloader)
    a = pd.read_parquet(panel / "AAA.parquet")
    assert list(a.index) == [pd.Timestamp("2020-01-02"), pd.Timestamp("2020-01-03"), pd.Timestamp("2020-01-06"), pd.Timestamp("2020-01-07")]
    # the overlapping 01-03 row kept the NEW value (later download wins)
    assert a.loc["2020-01-03", "close"] == 99.0
    # untouched-ticker case: a ticker the downloader returns nothing for is just skipped (no crash)
