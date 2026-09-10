"""Fuzzy search over the cached app list (rapidfuzz)."""

from rapidfuzz import fuzz

from vent.scraper.models import App

MIN_SCORE = 60.0


def fuzzy_search(needle: str, apps: list[App], limit: int = 10) -> list[App]:
    """Return up to ``limit`` apps best matching ``needle`` by name."""
    scored = [(fuzz.WRatio(needle, app.name), app) for app in apps]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [app for score, app in scored if score >= MIN_SCORE][:limit]
