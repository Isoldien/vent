"""Configuration and secret resolution.

* cache location + freshness settings
* API key resolution from STEAM_API_KEY env / .env (optional keyring)

Implementation of ``load_config`` / ``resolve_api_key`` deferred to Phase 2.
"""

from pathlib import Path

from pydantic import BaseModel

from vent.output.paths import OUT_DIR, STEAM_DIR


class Config(BaseModel):
    """Resolved runtime configuration."""

    cache_path: Path = OUT_DIR / "cache.db"
    steam_dir: Path = STEAM_DIR
    max_age_days: int = 7


def load_config() -> Config:
    """Load configuration, defaulting to project-local paths."""
    raise NotImplementedError


def resolve_api_key() -> str | None:
    """Return the Steam Web API key or ``None`` if unset (env / .env / keyring)."""
    raise NotImplementedError
