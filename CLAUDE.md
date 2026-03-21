# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the project
uv run python main.py

# Run tests
uv run pytest

# Run a single test
uv run pytest path/to/test_file.py::test_name

# Lint
uv run ruff check .

# Format
uv run ruff format .
```

## Project

This is an Othello (Reversi) game project in early development. The entry point is `main.py`. Dependencies are managed with `uv` (see `pyproject.toml`).

# Making code changes

* Consult [REQUIREMENTS.md](docs/REQUIREMENTS.md), [ARCHITECTURE.md](docs/ARCHITECTURE.md) and [CODE_STRUCTURE.md](docs/CODE_STRUCTURE.md) before making changes,
in order to guide where/how changes should be made.
* Respect the architecture described in ARCHITECTURE.md.
  * Changes to the architecture need to be proposed to and agreed with by the human.
  * Only propose such changes if it is necessary to avoid a major issue. 
    * Add the proposal to [ARCHITECTURE.md](docs/ARCHITECTURE.md) in this case,
    then let the human know they need to review it. 
* Use Test Driven Development.
* Keep UI classes (`ui/`) as thin as possible — rendering and event forwarding only. Any logic that can be tested should live in `game/` or `ai/`, not in UI classes.
* Run `uv run ruff format .` after making changes.
* Run `uv run mypy . --exclude .venv` after making changes and fix any type errors before proceeding.
* Once changes have been made, update CODE_STRUCTURE.md, and [CHANGELOG.md](docs/CHANGELOG.md)
  * CHANGELOG entries must include the date, time, and timezone in the heading, e.g. `2026-03-19 23:34 GMT — Description`
  * Always use GMT as the timezone
* Ensure [README.md](README.md) is kept up to date too.

# Executing code

* All python code should be executed using `uv run`
