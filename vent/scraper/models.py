"""Steam data models (pydantic)."""

from pydantic import BaseModel


class App(BaseModel):
    """A Steam app (a game or other product) with its numeric id."""

    app_id: int
    name: str
    type: str = "app"


class OwnedGame(BaseModel):
    """A game owned by a profile or API-key account."""

    app_id: int
    name: str | None = None
    playtime: int = 0


class SteamFile(BaseModel):
    """The on-disk representation of a .steam file: a single appID."""

    app_id: int

    def serialize(self) -> str:
        """Return the text written to the .steam file."""
        return str(self.app_id)
