---
name: python
description: Toolchain and conventions for Python projects: uv/venv, pyproject.toml, pytest, ruff, mypy, and everyday commands.
display_name: Python
icon: code
---

# Python Reference

## Toolchain

- Env: **uv** (`uv venv`, `uv pip install -e ".[dev]"`, `uv run pytest`) or
  stdlib `python -m venv`. Detect from `uv.lock` / `pyproject.toml`.
- Lint/format: **ruff** (`ruff check .`, `ruff format .`).
- Types: **mypy** (`mypy --strict src` — start strict, annotate outward).
- Tests: **pytest**.

## pyproject essentials

```toml
[project]
name = "mypackage"
requires-python = ">=3.12"
dependencies = []

[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
addopts = "-q --tb=short"
```

## Conventions

- Type hints on all public functions; `dataclasses` for value objects,
  `TypedDict` for JSON shapes.
- `pathlib.Path` over `os.path` strings.
- f-strings for messages; parameterized SQL, never string-formatted.
- `contextlib` (`with`) for anything with cleanup.
- Exceptions: catch the narrowest type, add context when re-raising
  (`raise RuntimeError(f"loading config: {e}") from e`).

## Everyday commands

| Task | uv |
|---|---|
| sync deps | `uv sync` |
| run tests | `uv run pytest` |
| lint | `uv run ruff check .` |
| format | `uv run ruff format .` |
| typecheck | `uv run mypy src` |

## Gotchas

- Mutable default args (`def f(items=[])` → `None` + `items or []`).
- Late-binding closures in loops (bind with default arg or `functools.partial`).
- `is` only for identity/`None`; `==` for values.
- Beware shadowing stdlib names (`type.py`, `json.py` in a package root).

## Official sources

- https://www.python.org — downloads, release schedule, PSF.
- https://docs.python.org/3/ — language reference + stdlib docs (start here).
- https://docs.python.org/3/whatsnew/ — per-version changes; read before upgrading.
- https://peps.python.org/pep-0008/ — style guide (PEP 8).
- https://peps.python.org/pep-0020/ — Zen of Python (`import this`).
- https://pypi.org — package index (pair with the `python-ecosystem` skill for evaluating packages).
