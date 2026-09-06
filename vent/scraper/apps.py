"""Fetch and normalize the Steam master app list.

Endpoint: ISteamApps/GetAppList (returns appid + name).
Implementation deferred to Phase 3.
"""

from vent.scraper.client import SteamClient
from vent.scraper.models import App


def fetch_app_list(client: SteamClient) -> list[App]:
    """Fetch the Steam app list and return normalized App records."""
    raise NotImplementedError
