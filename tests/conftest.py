"""Shared pytest fixtures."""

from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def sample_app_list_path() -> Path:
    """Path to the offline app-list JSON fixture."""
    return FIXTURES / "app_list_sample.json"
