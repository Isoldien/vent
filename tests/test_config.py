"""Tests for Phase 2: output paths + config / secret resolution."""

from pathlib import Path

import pytest

from vent.config import settings
from vent.config.settings import Config, load_config, resolve_api_key
from vent.output.paths import (
    CACHE_DB,
    STEAM_DIR,
    cache_db,
    cache_dir,
    ensure_output_dirs,
    steam_dir,
)


def test_ensure_output_dirs_returns_tuple() -> None:
    steam, cache = ensure_output_dirs()
    assert isinstance(steam, Path)
    assert isinstance(cache, Path)
    assert steam.is_dir()
    assert cache.is_dir()


def test_steam_dir_is_idempotent() -> None:
    first = steam_dir()
    second = steam_dir()
    assert first == second
    assert first.is_dir()


def test_cache_db_creates_parent_and_file() -> None:
    db = cache_db()
    assert db.is_file()
    assert db.parent.is_dir()
    assert db.name == "cache.db"


def test_cache_dir_does_not_touch_file() -> None:
    assert cache_dir().is_dir()


def test_load_config_defaults() -> None:
    cfg = load_config()
    assert isinstance(cfg, Config)
    assert cfg.max_age_days == 7
    assert cfg.steam_dir == STEAM_DIR
    assert cfg.cache_path == CACHE_DB


def test_resolve_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STEAM_API_KEY", "  secret123   ")
    assert resolve_api_key() == "secret123"


def test_resolve_api_key_empty_env_falls_through(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("STEAM_API_KEY", "")
    monkeypatch.setattr(settings, "PROJECT_ROOT", tmp_path)
    assert resolve_api_key() is None


def test_resolve_api_key_from_dotenv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("STEAM_API_KEY", raising=False)
    (tmp_path / ".env").write_text(
        "# comment\nSTEAM_API_KEY=abc\nOTHER=1\n", encoding="utf-8"
    )
    monkeypatch.setattr(settings, "PROJECT_ROOT", tmp_path)
    assert resolve_api_key() == "abc"


def test_resolve_api_key_missing_dotenv_none(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("STEAM_API_KEY", raising=False)
    monkeypatch.setattr(settings, "PROJECT_ROOT", tmp_path)
    assert resolve_api_key() is None
