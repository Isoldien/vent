# AGENTS.md

Guidance for working in this repo. Verify against `pyproject.toml` first.

## Project

`vent` — a `uv`-managed Python CLI that resolves Steam `appID`s and writes each to a
`<name>.steam` file (contents = the appID) for an ES-DE ROM library.
Native **Linux / macOS**; **Windows via WSL2**. Currently a **prototype**: module
bodies are Phase-gated stubs that `raise NotImplementedError`.

## Commands (always `uv run`)

- **Gotcha:** default `uv sync` installs runtime deps only. Lint/type/test tooling
  lives in the `dev` group — run `uv sync --all-groups` first.
- Order: **format -> check -> typecheck -> test -> run**:
  ```sh
  uv run ruff format . && uv run ruff check .
  uv run mypy vent
  uv run pytest -q                          # whole suite
  uv run pytest -k test_steam_filename      # one test by name
  uv run vent --help                        # CLI (OK after plain `uv sync`)
   ```

## Conventions & gotchas

- **Indentation is 4 spaces (no tabs).** The Write editor step repeatedly produces
  3-space / mixed indents that break `ruff` and `mypy` — always run
  `uv run ruff format .` after writing files.
- **Outputs are project-local:** `.steam` files go to `output/steam/` (gitignored).
  Never write into a user's ROM / ES-DE directory.
- **Filename rule** (from the live Steam `name`): `:` -> `-`, whitespace run -> `-`,
  collapse repeats, trim ends (`Counter-Strike: Global` -> `Counter-Strike-Global`).
- **Secrets:** API key comes from `STEAM_API_KEY` (env / `.env`, optional `keyring`).
  It must never be written into a `.steam` file — that file holds only the appID.
- **Offline design:** the Steam master list (`ISteamApps/GetAppList`) is fetched once
  and cached in SQLite so fuzzy search is offline. That endpoint is often **blocked in
  sandboxed networks** — tests use `tests/fixtures/app_list_sample.json`, never live calls.
- **Windows native** `C:\...\ROMs` / `ES-DE\ROMs` handling is out of scope for now;
  rely on WSL2.

## Architecture (`vent/`, grouped by concern)

- `cli/` user-facing typer commands + rich prompts · `scraper/` Steam acquisition
  (client/apps/library/models, pydantic) · `search/` local lookup (fuzzy + SQLite cache)
  · `output/` paths + `.steam` writer · `config/` settings + secret resolution.
- Sub-package `__init__.py` re-exports the public API; import from the package
  (e.g. `from vent.search import fuzzy_search`, `from vent.cli import app`).

## Phases (build is gated — do not assume logic exists)

0 init · 1 scaffold · 2 paths/config · 3 scraper+cache · 4 fuzzy · 5 CLI flow ·
6 output writer · 7 tests/lint · 8 package/docs.

Tests for unimplemented phases are `@pytest.mark.skip`, so the suite is green **by
omission** — a passing run does not mean a phase is done.

## Notes

- Renamed `esde-steam` -> `vent`, remove affiliation to the frontend. This is only a appID scraper (code namespace is `vent`;
  still targets the ES-DE `.steam`/ROM convention).
- No CI / pre-commit / `opencode.json` config present.
