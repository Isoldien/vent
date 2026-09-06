"""Write .steam files.

Filename rule (from the live game name):
    name = game_name.strip()
    name = name.replace(":", "-")
    runs of whitespace -> "-"
    collapse repeated dashes and trim ends
contents = the single appID (e.g. 105600).

Implementation deferred to Phase 6.
"""

from pathlib import Path

from rich.console import Console


def sanitize_name(name: str) -> str:
    """Return a filesystem-safe stem for ``name`` (colons->'-', whitespace->'-')."""
    raise NotImplementedError


def steam_filename(name: str) -> str:
    """Return the full ``<name>.steam`` filename for a game name."""
    raise NotImplementedError


def resolve_collision(path: Path, console: Console | None = None) -> bool:
    """Prompt on an existing file; return True if the write should proceed."""
    raise NotImplementedError


def write_steam(steam_dir: Path, name: str, app_id: int) -> Path:
    """Write ``app_id`` to ``<steam_dir>/<name>.steam`` and return the path."""
    raise NotImplementedError
