"""Tests for fuzzy search (Phase 4). Currently skipped until implemented."""

import pytest

from vent.scraper.models import App
from vent.search.fuzzy import fuzzy_search

SAMPLE = [
    App(app_id=105600, name="Terraia"),
    App(app_id=730, name="Counter-Strike: Global Offensive"),
    App(app_id=220, name="GRID Autosport"),
]


@pytest.mark.skip(reason="Phase 4")
def test_fuzzy_search_finds_terria() -> None:
    results = fuzzy_search("terra", SAMPLE, limit=3)
    assert results
    assert results[0].app_id == 105600
