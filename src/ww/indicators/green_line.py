"""Green Line Breakouts (Dr. Wish): placeholder — implementation in Task 3."""
from __future__ import annotations
import pandas as pd

def green_lines(monthly: pd.DataFrame, *, min_months_held: int = 3) -> list:
    raise NotImplementedError

def current_green_line(monthly: pd.DataFrame, *, min_months_held: int = 3):
    raise NotImplementedError

def is_green_line_breakout(*, close: float, green_line) -> bool:
    raise NotImplementedError
