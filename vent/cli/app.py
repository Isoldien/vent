"""CLI entry point and the two source flows.

Routes to:
    * search  - fuzzy-match games from the local app-list cache, then add/continue
    * apikey  - list owned games via STEAM_API_KEY, then select
"""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.prompt import Prompt

from vent.config.settings import load_config
from vent.output.write import write_steam
from vent.scraper.client import SteamClient
from vent.scraper.library import from_profile
from vent.scraper.models import App
from vent.search.cache import AppCache
from vent.search.fuzzy import fuzzy_search

from .prompts import confirm_add_or_continue, prompt_select

app = typer.Typer(
    name="vent",
    help="Resolve Steam appIDs and write .steam files for an ES-DE ROM library.",
    no_args_is_help=True,
)
console = Console()


def _write_selected(apps: list[App], steam_dir: Path) -> None:
    for selected in apps:
        path = write_steam(steam_dir, selected.name, selected.app_id)
        console.print(f"[green]wrote[/] {path}")


@app.command()
def search(
    query: Annotated[str, typer.Argument(..., help="text to fuzzy-match")],
) -> None:
    """Fuzzy-find games from the local app-list cache, then write .steam files."""
    config = load_config()
    cache = AppCache(config.cache_path)
    cache.ensure_populated(SteamClient())
    apps = cache.all_apps()
    current = query
    while True:
        matches = fuzzy_search(current, apps)
        if not matches:
            console.print(f"[red]No matches for '{current}'.[/]")
            raise typer.Exit(1)
        selected = prompt_select(matches)
        if selected:
            _write_selected(selected, config.steam_dir)
        if not confirm_add_or_continue():
            break
        current = Prompt.ask("New search text", default=current).strip()
        if not current:
            break


@app.command(name="apikey")
def api_key() -> None:
    """List own games via STEAM_API_KEY, then write .steam files."""
    steamid = typer.prompt("Your SteamID64", type=int)
    _owned_flow(steamid)


def _owned_flow(steamid: int) -> None:
    config = load_config()
    client = SteamClient()
    cache = AppCache(config.cache_path)
    cache.ensure_populated(client)
    games = from_profile(client, steamid)
    if not games:
        console.print("[red]No owned games found.[/]")
        raise typer.Exit(1)
    names = {cached.app_id: cached.name for cached in cache.all_apps()}
    apps = [
        App(
            appid=game.app_id,
            name=game.name or names.get(game.app_id) or f"app-{game.app_id}",
        )
        for game in games
    ]
    selected = prompt_select(apps)
    if selected:
        _write_selected(selected, config.steam_dir)
