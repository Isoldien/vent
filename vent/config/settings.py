"""Configuration and secret resolution.

* cache location + freshness settings
* API key resolution from STEAM_API_KEY env / .env (optional keyring)

Implementation of ``load_config`` / ``resolve_api_key`` deferred to Phase 2.
"""

from pathlib import Path

from pydantic import BaseModel

from vent.output.paths import OUT_DIR, STEAM_DIR, CACHE_DIR


class Config(BaseModel):
    """Resolved runtime configuration."""

    cache_path: Path = CACHE_DIR
    steam_dir: Path = STEAM_DIR
    max_age_days: int = 7


def load_config() -> Config:
    """Load configuratuion, defaulting to project-local paths."""
    return Config(cache_path=CACHE_DIR, steam_dir=STEAM_DIR, max_age_days=7)



def resolve_api_key() -> str | None:
    """Return the Steam Web API key or ``None`` if unset (env / .env / keyring)."""
    env_path = Path("../../.env")
    if not env_path.exists():
        return None

    with env_path.open(mode="r", encoding="utf-8") as file:
        for env in file:
            clean_env = env.strip()
        if clean_env.startswith("STEAM_API_KEY") :
            _, _, env = clean_env.partition("=")
            return str(env.strip())
