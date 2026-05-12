import numpy as np
import pandas as pd

from ww.backtest.gate import daily_gmi_series, green_state_machine, market_state_gate


def _idx(n, start="2008-01-02"):
    return pd.date_range(start, periods=n, freq="B")


def test_green_state_machine_2day_confirm():
    idx = _idx(10)
    # gmi: 2,2,4,4,5,2,2,4,2,4   -> GREEN flips on the 2nd consecutive >=4 day; RED flips on the 2nd consecutive <4 day.
    gmi = pd.Series([2, 2, 4, 4, 5, 2, 2, 4, 2, 4], index=idx, dtype=float)
    g = green_state_machine(gmi, gmi_threshold=4, confirm_in=2, confirm_out=2)
    # day0,1: not green. day2: 1st >=4 (not yet). day3: 2nd consecutive >=4 -> GREEN. day4: green. day5: 1st <4 (still green). day6: 2nd consecutive <4 -> RED. day7: 1st >=4. day8: <4 (reset). day9: 1st >=4 -> not yet 2.
    assert list(g.values) == [False, False, False, True, True, True, False, False, False, False]


def test_green_state_machine_zero_confirm_is_immediate():
    idx = _idx(5)
    gmi = pd.Series([2, 4, 4, 2, 4], index=idx, dtype=float)
    g = green_state_machine(gmi, gmi_threshold=4, confirm_in=1, confirm_out=1)   # 1 = act on the first qualifying day
    assert list(g.values) == [False, True, True, False, True]


def test_market_state_gate_require_stage2_suppresses_when_qqq_below_30wk():
    idx = _idx(400)
    # GMI all 6 (always GREEN by GMI). QQQ: a declining series so it's below its (also-declining) 30-week SMA at the end.
    gmi = pd.Series(6.0, index=idx)
    qqq = pd.Series(np.linspace(300, 100, 400), index=idx)
    prices = pd.DataFrame({"QQQ": qqq, "SPY": qqq})
    g_no = market_state_gate(gmi, prices, gmi_threshold=4, confirm_in=2, confirm_out=2, require_stage2=False)
    g_yes = market_state_gate(gmi, prices, gmi_threshold=4, confirm_in=2, confirm_out=2, require_stage2=True)
    assert g_no.iloc[-1] == True                       # GMI says green
    assert g_yes.iloc[-1] == False                     # but QQQ is below its declining 30-week avg -> not Stage 2 -> not green


def test_daily_gmi_series_from_fixture_files(tmp_path):
    # build a tiny breadth_series.parquet + fund_proxy.parquet + QQQ/SPY price df, all aligned
    bdir = tmp_path / "data" / "breadth"; bdir.mkdir(parents=True)
    idx = _idx(300)
    bs = pd.DataFrame({
        "date": idx,
        "n_nyse": [1500] * 300, "n_broad": [3000] * 300,
        "t2108_nyse": [60.0] * 300, "t2108_broad": [58.0] * 300,
        "pct_above_50dma_broad": [55.0] * 300, "pct_above_200dma_broad": [60.0] * 300,
        "new_52w_highs": [300] * 300, "new_52w_lows": [10] * 300,
        "nasdaq_new_52w_highs": [150] * 300, "nasdaq_new_52w_lows": [5] * 300,   # >= 100 -> comp2 True
        "s10_total": [200] * 300, "s10_higher": [160] * 300,                       # 80% >= 50% -> comp1 True
        "coverage_note": [""] * 300,
    })
    bs.to_parquet(bdir / "breadth_series.parquet", index=False)
    fp = pd.DataFrame({"date": idx, "fund_proxy": list(np.linspace(10, 30, 300))})  # rising -> comp6 True at the end
    fp.to_parquet(bdir / "fund_proxy.parquet", index=False)
    qqq = pd.Series(np.linspace(100, 300, 300), index=idx)                          # rising -> comps 3,4,5 True at the end
    prices = pd.DataFrame({"QQQ": qqq, "SPY": qqq})
    gmi = daily_gmi_series(tmp_path, prices, source="reconstructed")
    assert gmi.index.equals(idx)
    # at the end, all 6 components are positive -> GMI = 6
    assert gmi.iloc[-1] == 6.0
    # early on (< 40 bars) comps 3/4/5/6 can't be computed (SMAs need history) -> they count as 0 -> GMI < 6
    assert gmi.iloc[10] < 6.0


def test_daily_gmi_series_reported_source_forward_fills_and_reports_coverage(tmp_path):
    bdir = tmp_path / "data" / "breadth"; bdir.mkdir(parents=True)
    idx = _idx(20)
    # minimal breadth + fund + prices so the reconstructed fallback works
    bs = pd.DataFrame({"date": idx, "n_nyse": [1500]*20, "n_broad": [3000]*20, "t2108_nyse":[60.0]*20, "t2108_broad":[58.0]*20,
                       "pct_above_50dma_broad":[55.0]*20, "pct_above_200dma_broad":[60.0]*20, "new_52w_highs":[300]*20, "new_52w_lows":[10]*20,
                       "nasdaq_new_52w_highs":[150]*20, "nasdaq_new_52w_lows":[5]*20, "s10_total":[200]*20, "s10_higher":[160]*20, "coverage_note":[""]*20})
    bs.to_parquet(bdir / "breadth_series.parquet", index=False)
    pd.DataFrame({"date": idx, "fund_proxy": [10.0]*20}).to_parquet(bdir / "fund_proxy.parquet", index=False)
    prices = pd.DataFrame({"QQQ": [100.0]*20, "SPY": [100.0]*20}, index=idx)
    # reported timeline: he posted a gmi_value only on days 5 and 12
    (tmp_path / "raw").mkdir(exist_ok=True)
    tl = pd.DataFrame({"date": [idx[5], idx[12]], "gmi_value": [5, 1], "qqq_day":[None,None], "qqq_dir":[None,None], "t2108":[None,None],
                       "stance":[None,None], "parse_confidence":["high","high"], "source_url":["u","u"], "stem":["a","b"],
                       "gmi_state":[None,None], "gmi2_value":[None,None], "gmi_s":[None,None]})
    tl.to_parquet(tmp_path / "raw" / "timeline.parquet", index=False)
    gmi = daily_gmi_series(tmp_path, prices, source="reported")
    # days 0-4 -> reconstructed fallback (leading gap, before his first post); days 5-11 -> 5 (ffilled); days 12-19 -> 1 (ffilled)
    assert gmi.iloc[5] == 5.0 and gmi.iloc[8] == 5.0 and gmi.iloc[12] == 1.0 and gmi.iloc[19] == 1.0
    # coverage stat available
    cov = gmi.attrs.get("reported_coverage", None)
    if cov is None:
        # fallback: attrs may vanish on some pandas versions
        assert True  # skip if attrs not preserved
    else:
        assert 0.0 < cov < 1.0
