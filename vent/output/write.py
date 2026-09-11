"""Write .steam files.

Filename rule (from the live game name):
    name = game_name.strip()
    filesystem-invalid chars (/ \\ : * ? " < > |) -> "-"
    runs of whitespace -> "-"
    collapse repeated dashes and trim ends
contents = the single appID (e.g. 105600).
"""

import re
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm

from vent.scraper.models import SteamFile


def sanitize_name(name: str) -> str:
    """Return a filesystem-safe stem for ``name``.

    Invalid path characters (``/ \\ : * ? " < > |``) and whitespace runs
    become ``-``; repeated dashes collapse and ends are trimmed.
    """
    name = name.strip()
    name = re.sub(r'[/:\\*?"<>|]', "-", name)
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"-{2,}", "-", name)
    return name.strip("-")


def steam_filename(name: str) -> str:
    """Return the full ``<name>.steam`` filename for a game name."""
    return f"{sanitize_name(name)}.steam"


def resolve_collision(path: Path, console: Console | None = None) -> bool:
    """Prompt on an existing file; return True if the write should proceed."""
    if not path.exists():
        return True
    console = console or Console()
    return Confirm.ask(f"[yellow]{path} already exists.[/] Overwrite?", default=False)


def write_steam(steam_dir: Path, name: str, app_id: int) -> Path:
    """Write ``app_id`` to ``<steam_dir>/<name>.steam`` and return the path."""
    steam_dir.mkdir(parents=True, exist_ok=True)
    path = steam_dir / steam_filename(name)
    if not resolve_collision(path):
        raise FileExistsError(f"{path} already exists and overwrite was declined")
    path.write_text(SteamFile(app_id=app_id).serialize(), encoding="utf-8")
    return path
