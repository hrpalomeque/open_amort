# AGENTS.md

## Project overview

This repository is a Python package managed with `uv`.

- Python version: `3.14`
- Package source: `src/open_amort/`
- Tests: `tests/`

## Setup

Use `uv` for dependency and environment management.

- Sync dependencies with `uv sync --dev --frozen`
- When adding or removing dependencies, use `uv add` / `uv remove`
- Keep `uv.lock` in sync with any dependency changes
- Do not use `pip install`, `poetry`, or ad hoc virtualenv management unless the user explicitly asks for it

## Validation

Run these checks after code changes:

- `uv run pytest`

## Common commands

- Run tests: `uv run pytest`
- Run one test file: `uv run pytest tests/test_open_amort.py -q`
- Launch marimo: `uv run marimo edit`

## Change guidance

- Prefer minimal, targeted edits
- Put library code under `src/open_amort/`
- Add or update tests for behavior changes
- Avoid changing `.python-version` or `project.requires-python` unless the user requests it
