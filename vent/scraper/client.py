"""HTTP client for the Steam interfaces.

Wraps a requests.Session with auth-key handling.
"""

from typing import Any

from requests import Session


class SteamClient:
    """Make authenticated Steam API requests, returning parsed JSON.

    Uses the IStoreService interface; the old ISteamApps/GetAppList method
    has been removed by Steam.
    """

    def __init__(
        self,
        session: Session | None = None,
        base_url: str = "https://api.steampowered.com",
        timeout: float = 15.0,
    ) -> None:
        self.session = session or Session()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_json(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """GET {path} under base_url with {params} and return parsed JSON."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return data
