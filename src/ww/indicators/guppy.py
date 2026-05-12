"""GMMA/Guppy — placeholder, implementation in Task 6."""
from __future__ import annotations
import pandas as pd

SHORT_PERIODS = (3, 5, 8, 10, 12, 15)
LONG_PERIODS = (30, 35, 40, 45, 50, 60)

def gmma(close: pd.Series, *, short_periods=SHORT_PERIODS, long_periods=LONG_PERIODS) -> pd.DataFrame:
    raise NotImplementedError

def rwb_state(close: pd.Series, *, short_periods=SHORT_PERIODS, long_periods=LONG_PERIODS) -> str:
    raise NotImplementedError

def red_line_count(close: pd.Series, *, short_periods=SHORT_PERIODS) -> int:
    raise NotImplementedError
