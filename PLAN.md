# vent — Build Roadmap

`vent` resolves Steam `appID`s and writes each to a `<name>.steam` file
(contents = the appID) for an ES-DE ROM library. The repo is **fully scaffolded**:
every module exists with a signature and a `raise NotImplementedError` body.
Phases below are what to *fill in*, in dependency order.

## Status legend

- `done`   — implemented and verified.
- `todo`   — not yet started (stub only).
- `skip`   — a test exists but is gated with `@pytest.mark.skip` (unskip to prove the phase).

## Dependency order

`config` / `output.paths` (P2) → `scraper` + `cache` (P3) → `fuzzy` (P4) →
`output.write` (P6) → `cli` (P5) → unskip all tests (P7) → docs / package (P8).

Note: **P6 before P5** so the CLI has a writer to call.

## Phases

### P0 init · P1 scaffold — done

Repo, git, `uv` project, package tree, `__init__` re-exports, stub signatures.

### P2 paths / config — todo

- `vent/output/paths.py` `ensure_output_dirs`
- `vent/config/settings.py` `load_config`, `resolve_api_key`
- add `tests/test_config.py`

### P3 scraper + cache — todo

- `vent/scraper/client.py` `SteamClient.get_json`
- `vent/scraper/apps.py` `fetch_app_list`
- `vent/scraper/library.py` `from_profile`, `from_api_key`
- `vent/search/cache.py` `connect`, `AppCache.ensure_populated`, `is_stale`, `all`
- unskip `tests/test_library_offline.py`

### P4 fuzzy — todo

- `vent/search/fuzzy.py` `fuzzy_search`
- unskip `tests/test_search.py`

### P6 output writer — todo

- `vent/output/write.py` `sanitize_name`, `steam_filename`, `resolve_collision`, `write_steam`
- unskip `tests/test_output.py`

### P5 CLI flow — todo

- `vent/cli/prompts.py` `prompt_select`, `confirm_add_or_continue`
- `vent/cli/app.py` `search`, `profile`, `api_key`
- optionally add `tests/test_cli.py`

### P7 tests / lint — todo

Unskip every `@pytest.mark.skip`; add the P2/P5 tests; run the full gate green.

### P8 package / docs — todo

Update README "Status" from "pending" to real usage; verify the
`vent = "vent.cli:app"` entry point + `--help`; optionally build a hatchling wheel.

## The loop (per phase)

Run `uv sync --all-groups` once, then for each function:

1. read the stub + docstring + its skipped test (the test *is* the contract).
2. replace the `raise NotImplementedError` body only; keep signature + docstring.
3. unskip the matching test (remove the `@pytest.mark.skip(...)`).
4. `uv run ruff format .` — always; the editor produces bad indents.
5. `uv run ruff check .`
6. `uv run mypy vent`
7. `uv run pytest -q`

## Invariants (do not break)

- Outputs land in project-local `output/steam/` — never a user's ROM dir.
- `.steam` files hold **only the appID** — never the API key.
- The Steam master list is cached in SQLite; tests use
  `tests/fixtures/app_list_sample.json`, never live calls.
- A green suite by omission ≠ done: unskip tests to prove a phase.
