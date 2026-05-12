"""QQQ short-term timing — placeholder, implementation in Task 6."""
from __future__ import annotations
import pandas as pd

def short_term_trend(daily_close: pd.Series, *, window: int = 30) -> str:
    raise NotImplementedError

def trend_day_count(daily_close: pd.Series, *, window: int = 30) -> int:
    raise NotImplementedError
