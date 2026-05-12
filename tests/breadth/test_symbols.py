from pathlib import Path

import httpx
import pandas as pd

from ww.breadth.symbols import build_universe, download_symbol_files

FIXTURES = Path(__file__).parent / "fixtures"


def test_build_universe_keeps_only_common_stocks_on_nasdaq_nyse_amex(tmp_path):
    # copy the fixture into a symbol-files dir
    sf = tmp_path / "symbol_files"
    sf.mkdir()
    (sf / "nasdaqtraded.txt").write_text((FIXTURES / "nasdaqtraded_sample.txt").read_text(encoding="utf-8"), encoding="utf-8")
    uni = build_universe(sf)
    tickers = set(uni["ticker"])
    assert tickers == {"AA", "AAPL", "MSFT", "CATX", "BRK.B"}      # AAA(ETF), ZTEST(test), BAC^B(preferred), F.WS(warrant), FOO(notes) all dropped
    assert set(uni.columns) >= {"ticker", "name", "listing_exchange", "in_nyse"}
    assert uni.set_index("ticker").loc["AA", "in_nyse"] is True or uni.set_index("ticker").loc["AA", "in_nyse"] == True   # NYSE
    assert uni.set_index("ticker").loc["AAPL", "in_nyse"] == False                                                       # Nasdaq
    assert uni.set_index("ticker").loc["CATX", "in_nyse"] == False                                                       # NYSE American (A) -> not "in_nyse" (we reserve in_nyse for N)


def test_build_universe_strips_the_trailer_line(tmp_path):
    sf = tmp_path / "symbol_files"; sf.mkdir()
    (sf / "nasdaqtraded.txt").write_text((FIXTURES / "nasdaqtraded_sample.txt").read_text(encoding="utf-8"), encoding="utf-8")
    uni = build_universe(sf)
    assert not uni["ticker"].astype(str).str.startswith("File Creation Time").any()


def test_download_symbol_files_writes_and_caches(tmp_path):
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        return httpx.Response(200, text="Nasdaq Traded|Symbol|...\nY|AA|Alcoa Corporation Common Stock |N| |N|100|N||AA|AA|N\n")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    sf = tmp_path / "symbol_files"
    download_symbol_files(sf, client=client)
    assert (sf / "nasdaqtraded.txt").exists()
    assert len(calls) == 1
    # second call without refresh: no new HTTP
    download_symbol_files(sf, client=client)
    assert len(calls) == 1
    # with refresh=True: re-downloads
    download_symbol_files(sf, client=client, refresh=True)
    assert len(calls) == 2
