"""Locate and create the output directory.

Outputs are project-relative and never touch the user's ROM folders:

<project_root>/output/steam/<Name>.steam

``PROJECT_ROOT`` is resolved from the source tree: walking up from this file
(``vent/output/paths.py``) three levels reaches the project root.
Implementation of ``ensure_output_dirs`` is deferred to Phase 2.
"""

from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
OUT_DIR: Path = PROJECT_ROOT / "output"
STEAM_DIR: Path = OUT_DIR / "steam"
CACHE_DIR: Path = OUT_DIR / "cache" / "cache.db"

def cache_dir() -> Path:
    """Ensure cache folder exists with cache.db then return where it is stored"""
    CACHE_DIR.parent.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.touch()
    return CACHE_DIR

def steam_dir() -> Path:
    """Ensure directory exists and return where .steam files are written"""
    STEAM_DIR.mkdir(parents=True, exist_ok=True)
    return STEAM_DIR


def ensure_output_dirs() -> Path:
    """Create output/ and output/steam by returning steam_dir()"""
    return steam_dir(), cache_dir()
