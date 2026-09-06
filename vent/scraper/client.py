"""HTTP client for the Steam interfaces.

Wraps a requests.Session with auth-key handling.
"""

from typing import Any

from requests import Session


class SteamClient:
    """Make authenticated/unauthenticated Steam API requests."""

    def __init__(
        self,
        session: Session | None = None,
        base_url: str = "https://api.steampowered.com",
    ) -> None:
        self.session = session or Session()
        self.base_url = base_url.rstrip("/")

    def get_json(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """GET {path} under base_url with {params} and return parsed JSON."""
        raise NotImplementedError
