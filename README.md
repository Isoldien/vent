# vent

CLI to resolve Steam `appID`s and write them into `.steam` files for an
ES-DE ROM library.

## Install (uv)

```sh
uv sync --all-groups
uv run vent --help
```

## Usage

```sh
uv run vent search <query>    # fuzzy-find games from the local app-list cache
uv run vent profile <id>      # list owned games from a public Steam profile id
uv run vent apikey            # list owned games via STEAM_API_KEY
```

## Status

Prototype / CLI. Module logic is scaffolded (Phase 1) — implementation is
pending.
