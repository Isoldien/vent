"""Configuration and secret resolution.

* cache location + freshness settings
* API key resolution from ``STEAM_API_KEY`` (env first, then ``.env``; keyring is
a planned extension)
"""

import os
from pathlib import Path

from pydantic import BaseModel

from vent.output.paths import CACHE_DB, PROJECT_ROOT, STEAM_DIR


class Config(BaseModel):
    """Resolved runtime configuration."""

    cache_path: Path = CACHE_DB
    steam_dir: Path = STEAM_DIR
    max_age_days: int = 7


def load_config() -> Config:
    """Load configuration, defaulting to project-local paths."""
    return Config(cache_path=CACHE_DB, steam_dir=STEAM_DIR, max_age_days=7)


def resolve_api_key() -> str | None:
    """Return the Steam Web API key or ``None`` if unset.

    Resolution order: ``STEAM_API_KEY`` env var, then ``<project>/.env``.
    An empty value resolves to ``None``.
    """
    key = os.environ.get("STEAM_API_KEY")
    if key and key.strip():
        return key.strip()

    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return None

    with env_path.open(mode="r", encoding="utf-8") as file:
        for line in file:
            clean = line.strip()
            if clean.startswith("STEAM_API_KEY="):
                _, _, value = clean.partition("=")
                return value.strip() or None
    return None
