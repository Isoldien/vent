"""rich-based prompt helpers.

* interactive selection menu
* add-or-continue loop for the game-search flow
* collision handling on write
"""

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from vent.scraper.models import App


def prompt_select(apps: list[App], console: Console | None = None) -> list[App]:
    """Present a menu of apps and return the user's selection(s)."""
    console = console or Console()
    if not apps:
        console.print("[yellow]Nothing to select.[/]")
        return []
    table = Table(title="Matches")
    table.add_column("#", justify="right")
    table.add_column("appID", justify="right")
    table.add_column("Name")
    for index, app in enumerate(apps, start=1):
        table.add_row(str(index), str(app.app_id), app.name)
    console.print(table)
    count = len(apps)
    while True:
        choice = (
            Prompt.ask("Select (number, comma-separated, or 'all')", default="all")
            .strip()
            .lower()
        )
        if choice in {"all", "a"}:
            return list(apps)
        try:
            indexes = [int(part) for part in choice.split(",") if part.strip()]
        except ValueError:
            console.print("[red]Enter numbers (e.g. 1,3) or 'all'.[/]")
            continue
        if not indexes or any(index < 1 or index > count for index in indexes):
            console.print(f"[red]Pick numbers between 1 and {count}.[/]")
            continue
        return [apps[index - 1] for index in indexes]


def confirm_add_or_continue(console: Console | None = None) -> bool:
    """Ask whether to search again; return True to continue searching."""
    console = console or Console()
    return Confirm.ask("[bold]Search again?[/]", default=False)
