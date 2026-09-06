"""Local search: fuzzy matching + SQLite cache.

Re-exports the primary public API.
"""

from .cache import AppCache
from .fuzzy import fuzzy_search

__all__ = ["AppCache", "fuzzy_search"]
