"""MA stages (Weinstein) — placeholder, implementation in Task 4."""
from __future__ import annotations
import pandas as pd

def sma(close: pd.Series, window: int) -> pd.Series:
    raise NotImplementedError

def weekly_stage(weekly_close: pd.Series, *, ma_window: int = 30) -> int:
    raise NotImplementedError

def ma_alignment_4_10_30(weekly_close: pd.Series) -> bool:
    raise NotImplementedError

def tenwk_below_thirtywk(weekly_close: pd.Series) -> bool:
    raise NotImplementedError
