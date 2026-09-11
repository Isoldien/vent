"""CLI tests (Phase 5) — fully offline, no live Steam calls."""

import sys
from pathlib import Path

from typer.testing import CliRunner

import vent.cli  # noqa: F401  (ensures the submodule is imported)
from vent.cli import prompts as prompts_mod
from vent.cli.app import app
from vent.scraper.models import App, OwnedGame

# `vent.cli` re-exports the Typer instance as `app`, shadowing the submodule
# attribute; grab the real module object from sys.modules.
app_mod = sys.modules["vent.cli.app"]

runner = CliRunner()

SAMPLE = [
    App(appid=105600, name="Terraia"),
    App(appid=730, name="Counter-Strike: Global Offensive"),
]


def _patch_flow(monkeypatch, tmp_path: Path, written: list[tuple[str, int]]) -> None:
    class FakeCache:
        def __init__(self, db_path: Path) -> None:
            self.db_path = db_path

        def ensure_populated(self, client, force: bool = False) -> None:
            return None

        def all_apps(self) -> list[App]:
            return SAMPLE

    monkeypatch.setattr(app_mod, "AppCache", FakeCache)
    monkeypatch.setattr(
        app_mod,
        "load_config",
        lambda: type(
            "Cfg",
            (),
            {"cache_path": tmp_path / "cache.db", "steam_dir": tmp_path / "steam"},
        ),
    )
    monkeypatch.setattr(app_mod, "prompt_select", lambda apps, console=None: [apps[0]])
    monkeypatch.setattr(app_mod, "confirm_add_or_continue", lambda console=None: False)

    def fake_write(steam_dir: Path, name: str, app_id: int) -> Path:
        written.append((name, app_id))
        return steam_dir / f"{name}.steam"

    monkeypatch.setattr(app_mod, "write_steam", fake_write)


def test_help_lists_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("search", "apikey"):
        assert command in result.stdout
    assert "profile" not in result.stdout


def test_confirm_add_or_continue(monkeypatch) -> None:
    monkeypatch.setattr(
        prompts_mod.Confirm, "ask", classmethod(lambda cls, *a, **k: True)
    )
    assert prompts_mod.confirm_add_or_continue() is True
    monkeypatch.setattr(
        prompts_mod.Confirm, "ask", classmethod(lambda cls, *a, **k: False)
    )
    assert prompts_mod.confirm_add_or_continue() is False


def test_prompt_select_all(monkeypatch) -> None:
    monkeypatch.setattr(
        prompts_mod.Prompt, "ask", classmethod(lambda cls, *a, **k: "all")
    )
    assert prompts_mod.prompt_select(SAMPLE) == SAMPLE


def test_prompt_select_numbered(monkeypatch) -> None:
    monkeypatch.setattr(
        prompts_mod.Prompt, "ask", classmethod(lambda cls, *a, **k: "2, 1")
    )
    assert prompts_mod.prompt_select(SAMPLE) == [SAMPLE[1], SAMPLE[0]]


def test_prompt_select_retries_on_bad_input(monkeypatch) -> None:
    answers = iter(["bogus", "99", "1"])
    monkeypatch.setattr(
        prompts_mod.Prompt,
        "ask",
        classmethod(lambda cls, *a, **k: next(answers)),
    )
    assert prompts_mod.prompt_select(SAMPLE) == [SAMPLE[0]]


def test_search_flow_writes_selected(monkeypatch, tmp_path: Path) -> None:
    written: list[tuple[str, int]] = []
    _patch_flow(monkeypatch, tmp_path, written)
    result = runner.invoke(app, ["search", "terra"])
    assert result.exit_code == 0, result.stdout
    assert written == [("Terraia", 105600)]


def test_search_flow_no_matches_exits_nonzero(monkeypatch, tmp_path: Path) -> None:
    written: list[tuple[str, int]] = []
    _patch_flow(monkeypatch, tmp_path, written)
    result = runner.invoke(app, ["search", "zzzznotarealgame"])
    assert result.exit_code == 1
    assert written == []


def test_apikey_flow_writes_selected(monkeypatch, tmp_path: Path) -> None:
    written: list[tuple[str, int]] = []
    _patch_flow(monkeypatch, tmp_path, written)
    monkeypatch.setattr(
        app_mod,
        "from_profile",
        lambda client, steamid: [
            OwnedGame(appid=730, name="Counter-Strike: Global Offensive")
        ],
    )
    monkeypatch.setattr(app_mod, "prompt_select", lambda apps, console=None: list(apps))
    result = runner.invoke(app, ["apikey"], input="12345\n")
    assert result.exit_code == 0, result.stdout
    assert written == [("Counter-Strike: Global Offensive", 730)]


def test_apikey_flow_uses_cache_name_fallback(monkeypatch, tmp_path: Path) -> None:
    written: list[tuple[str, int]] = []
    _patch_flow(monkeypatch, tmp_path, written)
    monkeypatch.setattr(
        app_mod,
        "from_profile",
        lambda client, steamid: [OwnedGame(appid=730, name=None)],
    )
    result = runner.invoke(app, ["apikey"], input="12345\n")
    assert result.exit_code == 0, result.stdout
    assert written == [("Counter-Strike: Global Offensive", 730)]
