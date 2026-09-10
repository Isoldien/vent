"""CLI entry point and the three source flows.

Routes to:
    * search  - fuzzy-match games from the local app-list cache, then add/continue
    * profile - list owned games from a public Steam profile id, then select
    * apikey  - list owned games via STEAM_API_KEY, then select

Implementation is deferred to Phase 5.
"""

from typing import Annotated

import typer

app = typer.Typer(
    name="vent",
    help="Resolve Steam appIDs and write .steam files for an ES-DE ROM library.",
    no_args_is_help=True,
)


@app.command()
def search(
    query: Annotated[str, typer.Argument(..., help="text to fuzzy-match")],
) -> None:
    """Fuzzy-find games from the local app-list cache, then write .steam files."""
    raise NotImplementedError

@app.command(name="apikey")
def api_key() -> None:
    """List own games via STEAM_API_KEY, then write .steam files."""
    raise NotImplementedError
