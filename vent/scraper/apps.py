"""Fetch and normalize the Steam master app list.

Endpoint: IStoreService/GetAppList (returns appid + name).
"""

from vent.config.settings import resolve_api_key
from vent.scraper.client import SteamClient
from vent.scraper.models import App


def fetch_app_list(client: SteamClient) -> list[App]:
    """Fetch the Steam app list and return normalized App records.

    The endpoint requires a Steam Web API key; raises RuntimeError if
    ``STEAM_API_KEY`` is not configured.
    """
    key = resolve_api_key()
    if not key:
        raise RuntimeError(
            "STEAM_API_KEY is not set. Set the env var or add it to .env."
        )
    raw_json = client.get_json("IStoreService/GetAppList/v1", params={"key": key})
    raw_apps = raw_json.get("response", {}).get("apps", [])
    return [App.model_validate(app) for app in raw_apps]
