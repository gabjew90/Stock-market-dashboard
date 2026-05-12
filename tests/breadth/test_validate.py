import json
from pathlib import Path

import numpy as np
import pandas as pd

from ww.breadth.validate import validate_against_reported


def _setup(tmp_path: Path):
    bdir = tmp_path / "data" / "breadth"; bdir.mkdir(parents=True)
    dates = pd.date_range("2014-01-06", periods=40, freq="B")
    # our reconstruction: t2108_broad tracks "his" closely; t2108_nyse a bit off
    his_t2108 = np.linspace(40, 80, 40)
    bs = pd.DataFrame({
        "date": dates, "n_nyse": [1500] * 40, "n_broad": [3000] * 40,
        "t2108_nyse": his_t2108 + 8.0, "t2108_broad": his_t2108 + 1.0,
        "pct_above_50dma_broad": his_t2108, "pct_above_200dma_broad": his_t2108,
        "new_52w_highs": [300] * 40, "new_52w_lows": [10] * 40,
        "nasdaq_new_52w_highs": [150] * 40, "nasdaq_new_52w_lows": [5] * 40,
        "s10_total": [200] * 40, "s10_higher": [170] * 40, "coverage_note": [""] * 40,
    })
    bs.to_parquet(bdir / "breadth_series.parquet", index=False)
    fp = pd.DataFrame({"date": pd.date_range("2013-06-01", periods=300, freq="B"), "fund_proxy": [10.0 + i * 0.1 for i in range(300)]})
    fp.to_parquet(bdir / "fund_proxy.parquet", index=False)
    # his reported timeline: he gave a t2108 on every other date, and a gmi_value on every date (all 6, fully bullish)
    rows = []
    for i, d in enumerate(dates):
        rows.append({"date": d, "t2108": float(his_t2108[i]) if i % 2 == 0 else None,
                     "gmi_value": 6, "gmi_state": "Green", "gmi2_value": None, "gmi_s": None,
                     "qqq_day": None, "qqq_dir": None, "stance": None, "parse_confidence": "high",
                     "source_url": "u", "stem": f"2014-{i:02d}"})
    (tmp_path / "raw").mkdir(exist_ok=True)
    pd.DataFrame(rows).to_parquet(tmp_path / "raw" / "timeline.parquet", index=False)
    # fully-bullish price caches so the reconstructed GMI is 6 on every date
    def up(n, lo, hi, freq):
        idx = pd.date_range("2010-01-01" if freq == "B" else "2010-01-03", periods=n, freq=freq)
        c = [lo + (hi - lo) * j / (n - 1) for j in range(n)]
        return pd.DataFrame({"open": c, "high": c, "low": c, "close": c, "adj_close": c, "volume": [1] * n}, index=idx)
    cache = {("QQQ", "1d"): up(1200, 50, 400, "B"), ("SPY", "1d"): up(1200, 50, 400, "B"), ("QQQ", "1wk"): up(300, 50, 400, "W-SUN")}
    return tmp_path, cache


def test_validate_picks_better_t2108_flavor_and_writes_json(tmp_path):
    root, cache = _setup(tmp_path)
    result = validate_against_reported(root, prices_cache=cache)
    assert result["chosen_flavor"] == "broad"                       # broad is +1 bias vs nyse's +8
    assert "t2108" in result and "broad" in result["t2108"] and "nyse" in result["t2108"]
    assert result["t2108"]["broad"]["rmse"] < result["t2108"]["nyse"]["rmse"]
    assert -2.0 < result["t2108"]["broad"]["mean_bias"] < 2.0
    vj = json.loads((root / "data" / "breadth" / "validate.json").read_text(encoding="utf-8"))
    assert vj["chosen_flavor"] == "broad"


def test_validate_gmi_agreement(tmp_path):
    root, cache = _setup(tmp_path)
    result = validate_against_reported(root, prices_cache=cache)
    g = result["gmi"]
    assert g["n"] == 40                                             # 40 dates with a reported gmi_value that are also in our series
    assert g["exact_match_rate"] == 1.0                             # fully-bullish fixture: ours is 6 on every date, he said 6
    assert g["within_1_rate"] == 1.0
    assert 0 <= len(g["sample_side_by_sides"]) <= 20
    assert "per_value" in g                                          # the "when he said N, ours was: ..." breakdown
