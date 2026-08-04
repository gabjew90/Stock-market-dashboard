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


def _panel_with(panel: Path, ticker: str, dates, closes) -> None:
    df = pd.DataFrame({"open": closes, "high": closes, "low": closes, "close": closes,
                       "adj_close": closes, "volume": [1] * len(closes)}, index=pd.DatetimeIndex(dates))
    df.index.name = "date"
    panel.mkdir(parents=True, exist_ok=True)
    df.to_parquet(panel / f"{ticker}.parquet")


def test_update_panel_placeholder_row_does_not_erase_a_good_bar(tmp_path):
    """A re-fetch whose latest bar has NaN prices (but a volume) must not wipe the bar we already have.

    This is the build-dashboard #136 failure: the 01:00 UTC cron ran late, re-fetched a day
    that run #135 had already captured correctly, and ~440 NYSE names lost their 2026-07-24
    close — dropping n_nyse to 1480 and tripping the <1500 universe-collapse guardrail.
    """
    panel = tmp_path / "panel"
    dates = ["2020-01-02", "2020-01-03"]
    _panel_with(panel, "AAA", dates, [10.0, 11.0])
    uni = pd.DataFrame({"ticker": ["AAA"], "in_nyse": [True]})

    def downloader(yf_tickers, **kw):
        f = _fake_frame(yf_tickers, dates)
        f.loc["2020-01-03", [(t, c) for t in yf_tickers for c in ("Open", "High", "Low", "Close", "Adj Close")]] = float("nan")
        return f                                    # 01-03 comes back price-less, volume still present

    update_panel(uni, panel, downloader=downloader)
    a = pd.read_parquet(panel / "AAA.parquet")
    assert a.loc["2020-01-03", "close"] == 11.0     # the good bar survived
    assert a.loc["2020-01-03", "adj_close"] == 11.0
    assert not a["close"].isna().any()


def test_update_panel_keeps_adj_close_when_refetch_omits_the_column(tmp_path):
    """yfinance sometimes returns a frame with no Adj Close; the existing adj_close must survive."""
    panel = tmp_path / "panel"
    dates = ["2020-01-02", "2020-01-03"]
    _panel_with(panel, "AAA", dates, [10.0, 11.0])
    uni = pd.DataFrame({"ticker": ["AAA"], "in_nyse": [True]})

    def downloader(yf_tickers, **kw):
        f = _fake_frame(yf_tickers, dates)
        return f.drop(columns=[(t, "Adj Close") for t in yf_tickers])

    update_panel(uni, panel, downloader=downloader)
    a = pd.read_parquet(panel / "AAA.parquet")
    assert list(a.columns) == ["open", "high", "low", "close", "adj_close", "volume"]
    assert a.loc["2020-01-03", "adj_close"] == 11.0


def test_update_panel_reports_a_degraded_fetch(tmp_path, caplog):
    """The non-destructive merge hides a bad fetch from the build gate, so it must be logged instead."""
    panel = tmp_path / "panel"
    dates = ["2020-01-02", "2020-01-03"]
    tickers = [f"T{i:02d}" for i in range(10)]
    for t in tickers:
        _panel_with(panel, t, dates, [10.0, 11.0])
    uni = pd.DataFrame({"ticker": tickers, "in_nyse": [True] * len(tickers)})

    def downloader(yf_tickers, **kw):
        f = _fake_frame(yf_tickers, dates)
        f.loc["2020-01-03", [(t, c) for t in yf_tickers for c in ("Open", "High", "Low", "Close", "Adj Close")]] = float("nan")
        return f

    with caplog.at_level("WARNING"):
        update_panel(uni, panel, downloader=downloader)
    msg = caplog.text
    assert "DEGRADED yfinance response" in msg
    assert "10 price-less rows dropped across 10 tickers" in msg


def test_update_panel_silent_on_a_clean_fetch(tmp_path, caplog):
    panel = tmp_path / "panel"
    _panel_with(panel, "AAA", ["2020-01-02", "2020-01-03"], [10.0, 11.0])
    uni = pd.DataFrame({"ticker": ["AAA"], "in_nyse": [True]})

    def downloader(yf_tickers, **kw):
        return _fake_frame(yf_tickers, pd.date_range("2020-01-06", periods=2, freq="B"), base=50.0)

    with caplog.at_level("WARNING"):
        update_panel(uni, panel, downloader=downloader)
    assert "fetch quality" not in caplog.text


def test_update_panel_still_appends_genuinely_new_bars(tmp_path):
    """The non-destructive merge must not stop real new bars from landing."""
    panel = tmp_path / "panel"
    _panel_with(panel, "AAA", ["2020-01-02", "2020-01-03"], [10.0, 11.0])
    uni = pd.DataFrame({"ticker": ["AAA"], "in_nyse": [True]})

    def downloader(yf_tickers, **kw):
        return _fake_frame(yf_tickers, pd.date_range("2020-01-06", periods=2, freq="B"), base=50.0)

    update_panel(uni, panel, downloader=downloader)
    a = pd.read_parquet(panel / "AAA.parquet")
    assert list(a.index) == [pd.Timestamp(d) for d in ("2020-01-02", "2020-01-03", "2020-01-06", "2020-01-07")]
    assert a.loc["2020-01-06", "close"] == 50.0
