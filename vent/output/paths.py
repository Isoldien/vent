"""Locate and (idempotently) create the output directories.

Outputs are project-relative and never touch the user's ROM folders:

<project_root>/output/steam/<Name>.steam
<project_root>/output/cache/cache.db

``PROJECT_ROOT`` is resolved from the source tree when available (walking up
from ``vent/output/paths.py`` three levels, validated by a ``pyproject.toml``
marker); when installed as a wheel it falls back to the current directory so
outputs never land in ``site-packages``.
"""

from pathlib import Path


def _project_root() -> Path:
    candidate = Path(__file__).resolve().parent.parent.parent
    if (candidate / "pyproject.toml").is_file():
        return candidate
    return Path.cwd()


PROJECT_ROOT: Path = _project_root()
OUT_DIR: Path = PROJECT_ROOT / "output"
STEAM_DIR: Path = OUT_DIR / "steam"
CACHE_DIR: Path = OUT_DIR / "cache"
CACHE_DB: Path = CACHE_DIR / "cache.db"


def cache_dir() -> Path:
    """Ensure the cache directory exists and return its path."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR


def cache_db() -> Path:
    """Ensure the cache database file exists and return its path."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DB.touch()
    return CACHE_DB


def steam_dir() -> Path:
    """Ensure the output dir exists and return where .steam files are written."""
    STEAM_DIR.mkdir(parents=True, exist_ok=True)
    return STEAM_DIR


def ensure_output_dirs() -> tuple[Path, Path]:
    """Create the output structure, returning ``(steam_dir, cache_dir)``."""
    return steam_dir(), cache_dir()
