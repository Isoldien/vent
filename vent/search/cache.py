"""SQLite-backed cache of the Steam app list.

Stores appid → {name, type} plus a fetch timestamp so the master list can be
populated once and searched offline. Implementation deferred to Phase 3.
"""

import sqlite3
import time
from pathlib import Path

from vent.scraper.apps import fetch_app_list
from vent.scraper.client import SteamClient
from vent.scraper.models import App

TABLE = "apps"


def connect(db_path: Path) -> sqlite3.Connection:
    """Open (creating if needed) the SQLite connection for caching."""
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
        self._init_db()

    def _init_db(self) -> None:
        conn = connect(self.db_path)
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS apps (
                    appid INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def is_stale(self, max_age_days: int = 7) -> bool:
        """Return True if the cache is missing or older than ``max_age_days``."""
        if not self.db_path.exists():
            return True
        conn = connect(self.db_path)
        try:
            row = conn.execute(
                "SELECT value FROM metadata WHERE key = 'fetched_at'"
            ).fetchone()
            if row is None:
                return True
            fetched_at = float(row[0])
            age_seconds = time.time() - fetched_at
            max_age_seconds = max_age_days * 86400
            return age_seconds > max_age_seconds
        finally:
            conn.close()

    def ensure_populated(self, client: SteamClient, force: bool = False) -> None:
        """Populate the cache from the Steam app list unless stale/forced."""
        if not force and not self.is_stale():
            return
        apps = fetch_app_list(client)
        conn = connect(self.db_path)
        try:
            conn.execute("DELETE FROM apps")
            for app in apps:
                conn.execute(
                    "INSERT OR REPLACE INTO apps (appid, name) VALUES (?, ?)",
                    (app.app_id, app.name),
                )
            conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES ('fetched_at', ?)",
                (str(time.time()),),
            )
            conn.commit()
        finally:
            conn.close()

    def all_apps(self) -> list[App]:
        """Return every cached app."""
        conn = connect(self.db_path)
        try:
            rows = conn.execute("SELECT appid, name FROM apps").fetchall()
            return [App(appid=appid, name=name) for appid, name in rows]
        finally:
            conn.close()
