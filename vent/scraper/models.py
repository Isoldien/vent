"""Steam data models (pydantic)."""

from pydantic import BaseModel, ConfigDict, Field


class App(BaseModel):
    """A Steam app (a game or other product) with its numeric id."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appid")
    name: str
    # Type of app removed for now


class OwnedGame(BaseModel):
    """A game owned by a profile, as reported by GetOwnedGames."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appid")
    name: str | None = None
    playtime_forever: int = 0


class SteamFile(BaseModel):
    """The on-disk representation of a .steam file: a single appID."""

    app_id: int

    def serialize(self) -> str:
        """Return the text written to the .steam file."""
        return str(self.app_id)
