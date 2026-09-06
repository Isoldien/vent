"""Offline tests for the Steam client against the app-list fixture (Phase 3).

Currently skipped until Phase 3 implementation.
"""

import json

import pytest

from vent.scraper.apps import fetch_app_list
from vent.scraper.client import SteamClient


@pytest.mark.skip(reason="Phase 3")
def test_fetch_app_list_from_fixture(
    monkeypatch: pytest.MonkeyPatch,
    sample_app_list_path: object,
) -> None:
    raw = json.loads((sample_app_list_path).read_text())
    client = SteamClient()
    monkeypatch.setattr(client, "get_json", lambda path, params=None: raw)
    apps = fetch_app_list(client)
    assert any(app.app_id == 105600 for app in apps)
