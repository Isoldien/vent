"""Fuzzy search over the cached app list (rapidfuzz).

Implementation deferred to Phase 4.
"""

from vent.scraper.models import App


def fuzzy_search(needle: str, apps: list[App], limit: int = 10) -> list[App]:
    """Return up to ``limit`` apps best matching ``needle`` by name."""
    raise NotImplementedError
