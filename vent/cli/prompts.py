"""rich-based prompt helpers.

* interactive selection menu
* add-or-continue loop for the game-search flow
* collision handling on write

Implementation is deferred to Phase 5.
"""

from rich.console import Console

from vent.scraper.models import App


def prompt_select(apps: list[App], console: Console | None = None) -> list[App]:
    """Present a menu of apps and return the user's selection(s)."""
    raise NotImplementedError


def confirm_add_or_continue(console: Console | None = None) -> bool:
    """Ask whether to search again; return True to continue searching."""
    raise NotImplementedError
