"""Summary counts over the raw-sources index."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from ww.corpus.index import read_posts_jsonl


def corpus_stats(root: Path) -> dict:
    records = read_posts_jsonl(Path(root) / "raw" / "posts.jsonl")
    if not records:
        return {"total_posts": 0}

    dates = sorted(r.date for r in records)
    return {
        "total_posts": len(records),
        "date_range": (dates[0], dates[-1]),
        "by_kind_guess": dict(Counter(r.kind_guess for r in records)),
        "by_tier": dict(Counter(r.tier for r in records)),
        "ingested": sum(1 for r in records if r.ingested),
        "posts_with_charts": sum(1 for r in records if r.chart_count > 0),
        "total_chart_images": sum(len(r.chart_image_urls) for r in records),
    }
