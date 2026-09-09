"""Fetch owned games from a public profile id or an API-key account.

* from_profile(steam_id)   - IPlayerService/GetOwnedGames (public profile)
* from_api_key(account_id) - IPlayerService/GetOwnedGames (own account)

Implementation deferred to Phase 3.
"""

from vent.scraper.client import SteamClient
from vent.scraper.models import OwnedGame


def from_profile(client: SteamClient, steam_id: int) -> list[OwnedGame]:
    """Return games owned by a steam profile using API Key."""
    client.get_json(
        "IPlayerService/GetOwnedGames/v1",
        params={"steamid": steam_id, "include_appinfo": True},
    )
    raise NotImplementedError
