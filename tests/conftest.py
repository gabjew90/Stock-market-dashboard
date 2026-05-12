"""Shared pytest fixtures."""
from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """An empty temporary repo root with a raw/ directory."""
    (tmp_path / "raw").mkdir()
    return tmp_path
