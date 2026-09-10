"""Fetch owned games from a public profile id.

* from_profile(steam_id) - IPlayerService/GetOwnedGames

Implementation deferred to Phase 3.
"""

from vent.scraper.client import SteamClient
from vent.scraper.models import OwnedGame


def from_profile(client: SteamClient, steam_id: int) -> list[OwnedGame]:
    """Return games owned by a steam profile using API Key."""
    owned_games: list[OwnedGame] = []
    response = client.get_json(
        "IPlayerService/GetOwnedGames/v1",
        params={"steamid": steam_id, "include_appinfo": 1},
    )

    games_list = response.get("response", {}).get("games", [])

    for game in games_list:
        game_object = OwnedGame(**game)
        owned_games.append(game_object)
    # @TODO: change this to list comprehension one day
    return owned_games
