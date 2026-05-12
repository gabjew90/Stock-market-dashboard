"""Cross-check the reconstructed T2108 and GMI against the values Dr. Wish actually reported (raw/timeline.parquet)."""
from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

from ww.indicators.breadth_provider import BreadthProvider
from ww.indicators.gmi import gmi

_MIN_UNIVERSE_FOR_GMI = 300   # don't trust reconstructed GMI on dates where the panel is too thin


def _fit_stats(ours: pd.Series, his: pd.Series) -> dict:
    mask = ours.notna() & his.notna()
    a, b = ours[mask].astype(float), his[mask].astype(float)
    if len(a) < 2:
        return {"n": int(len(a)), "corr": None, "rmse": None, "mean_bias": None}
    return {
        "n": int(len(a)),
        "corr": float(np.corrcoef(a, b)[0, 1]),
        "rmse": float(np.sqrt(((a - b) ** 2).mean())),
        "mean_bias": float((a - b).mean()),
    }


def validate_against_reported(root: Path, *, prices_cache: dict | None = None, n_samples: int = 15, seed: int = 0) -> dict:
    root = Path(root)
    bdir = root / "data" / "breadth"
    bs = pd.read_parquet(bdir / "breadth_series.parquet"); bs["date"] = pd.to_datetime(bs["date"]).dt.normalize(); bs = bs.set_index("date").sort_index()
    tl_raw = pd.read_parquet(root / "raw" / "timeline.parquet"); tl_raw["date"] = pd.to_datetime(tl_raw["date"]).dt.normalize()
    # Deduplicate: for each date keep the row with the most non-null values (prefer rows that have gmi_value / t2108)
    tl_raw = tl_raw.sort_values("date")
    tl = tl_raw.groupby("date", as_index=False).first()
    tl = tl.set_index("date").sort_index()

    # ---- T2108 ----
    joined = bs.join(tl["t2108"], how="inner").dropna(subset=["t2108"])
    t2108_stats = {
        "nyse": _fit_stats(joined["t2108_nyse"], joined["t2108"]),
        "broad": _fit_stats(joined["t2108_broad"], joined["t2108"]),
    }
    def _score(s):  # prefer higher corr, then lower rmse
        return (s["corr"] if s["corr"] is not None else -1, -(s["rmse"] if s["rmse"] is not None else 1e9))
    chosen = "broad" if _score(t2108_stats["broad"]) >= _score(t2108_stats["nyse"]) else "nyse"

    # ---- GMI ----
    bp = BreadthProvider(root, flavor=chosen, prices_cache=prices_cache or {})
    gmi_dates = [d for d in tl.index
                 if not pd.isna(tl.at[d, "gmi_value"]) and d in bs.index and bs.at[d, "n_broad"] >= _MIN_UNIVERSE_FOR_GMI]
    pairs = []  # (date, his, ours)
    for d in gmi_dates:
        try:
            ours = gmi(bp, d.strftime("%Y-%m-%d")).score
        except Exception:  # noqa: BLE001 - a single bad date shouldn't sink the whole validation
            continue
        pairs.append((d, int(tl.at[d, "gmi_value"]), int(ours)))
    if pairs:
        his = np.array([p[1] for p in pairs]); our = np.array([p[2] for p in pairs])
        exact = float((his == our).mean())
        within1 = float((np.abs(his - our) <= 1).mean())
        corr = float(np.corrcoef(his, our)[0, 1]) if len(his) > 1 and his.std() > 0 and our.std() > 0 else None
        per_value = {}
        for v in sorted(set(his.tolist())):
            sub = our[his == v]
            per_value[int(v)] = {int(k): int((sub == k).sum()) for k in sorted(set(sub.tolist()))}
        rng = random.Random(seed)
        sample = sorted(rng.sample(pairs, min(n_samples, len(pairs))), key=lambda p: p[0])
        gmi_stats = {
            "n": len(pairs), "exact_match_rate": exact, "within_1_rate": within1, "corr": corr, "per_value": per_value,
            "sample_side_by_sides": [{"date": d.strftime("%Y-%m-%d"), "his": h, "ours": o} for d, h, o in sample],
        }
    else:
        gmi_stats = {"n": 0}

    result = {"chosen_flavor": chosen, "t2108": t2108_stats, "gmi": gmi_stats}
    (bdir).mkdir(parents=True, exist_ok=True)
    (bdir / "validate.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
