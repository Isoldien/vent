"""SQLite-backed cache of the Steam app list.

Stores appid → {name, type} plus a fetch timestamp so the master list can be
populated once and searched offline. Implementation deferred to Phase 3.
"""

import sqlite3
from pathlib import Path

from vent.scraper.client import SteamClient
from vent.scraper.models import App

TABLE = "apps"


def connect(db_path: Path) -> sqlite3.Connection:
    """Open (creating if needed) the SQLite connection for caching."""
    #TODO: i think this how you do it 
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error:
        print(f"Database connection error: {db_path}")
        raise


class AppCache:
    """Manage the cached app list."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def ensure_populated(self, client: SteamClient, force: bool = False) -> None:
        """Populate the cache from the Steam app list unless stale/forced."""
        raise NotImplementedError

    def is_stale(self, max_age_days: int = 7) -> bool:
        """Return True if the cache is missing or older than ``max_age_days``."""
        raise NotImplementedError

    def all_apps(self) -> list[App]:
        """Return every cached app."""
        raise NotImplementedError
