"""Configuration and secret resolution.

* cache location + freshness settings
* API key resolution from ``STEAM_API_KEY`` (env first, then ``.env``; an
optional ``keyring`` extra is planned)
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

    for key, value in _parse_env_file(env_path).items():
        if key == "STEAM_API_KEY" and value:
            return value
    return None


def _parse_env_file(env_path: Path) -> dict[str, str]:
    """Parse a ``.env`` file into a dict of key/value pairs.

    Tolerates comments, blank lines, ``export`` prefixes, spaces around ``=``,
    and single/double-quoted values.
    """
    values: dict[str, str] = {}
    with env_path.open(mode="r", encoding="utf-8") as file:
        for line in file:
            clean = line.strip()
            if not clean or clean.startswith("#") or "=" not in clean:
                continue
            key, _, value = clean.partition("=")
            if key.startswith("export "):
                key = key[len("export ") :]
            key = key.strip()
            if not key:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
            values[key] = value
    return values
