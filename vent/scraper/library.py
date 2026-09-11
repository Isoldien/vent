"""Fetch owned games from a public profile id.

* from_profile(steam_id) - IPlayerService/GetOwnedGames
"""

from vent.config.settings import resolve_api_key
from vent.scraper.client import SteamClient
from vent.scraper.models import OwnedGame


def from_profile(client: SteamClient, steam_id: int) -> list[OwnedGame]:
    """Return games owned by a steam profile using API Key."""
    key = resolve_api_key()
    if not key:
        raise RuntimeError(
            "STEAM_API_KEY is not set. Set the env var or add it to .env."
        )
    owned_games: list[OwnedGame] = []
    response = client.get_json(
        "IPlayerService/GetOwnedGames/v1",
        params={"steamid": steam_id, "include_appinfo": 1, "key": key},
    )

    games_list = response.get("response", {}).get("games", [])

    for game in games_list:
        game_object = OwnedGame(**game)
        owned_games.append(game_object)
    # @TODO: change this to list comprehension one day
    return owned_games
