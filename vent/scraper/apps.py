"""Fetch and normalize the Steam master app list.

Endpoint: ISteamApps/GetAppList (returns appid + name).
Implementation deferred to Phase 3.
"""

from vent.scraper.client import SteamClient
from vent.config.settings import resolve_api_key
from vent.scraper.models import App


def fetch_app_list(client: SteamClient) -> list[App]:
    """Fetch the Steam app list and return normalized App records."""
    raw_json = client.get_json(
        "ISteamApps/GetAppList/v2",
        params={"STEAM_API_KEY": resolve_api_key()}
    )
    raw_apps = raw_json.get("applist", {}).get("apps", [])
    return [App.model_validate(app) for app in raw_apps]
