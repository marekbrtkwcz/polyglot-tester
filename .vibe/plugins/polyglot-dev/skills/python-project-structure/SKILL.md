---
name: python-project-structure
description: Load this skill when starting or reorganizing a Python project: src layout, pyproject.toml, uv/venv, ruff, packaging, and pre-commit hooks.
---

# Python Project Structure

## Layout

```
pyproject.toml          # all config lives here
uv.lock                 # committed
README.md
src/mypackage/          # src layout — prevents accidental import of local dir
    __init__.py
    py.typed            # marker for typed package (PEP 561)
tests/
    conftest.py
    test_foo.py
```

- src layout: `pip install -e .` then imports work from installed package, not the source dir — catches missing files in packaging.
- Flat layout acceptable for scripts/small tools.

## pyproject.toml essentials

```toml
[project]
name = "mypackage"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["httpx>=0.27"]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy", "pip-audit"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
strict = true

[tool.pytest.ini_options]
addopts = "-q --tb=short"
testpaths = ["tests"]
```

## Toolchain: uv

- `uv venv`, `uv pip install -e ".[dev]"`, `uv run pytest`, `uv sync --locked` (CI, from lockfile).
- `uv add <pkg>` / `uv remove` manage pyproject + lockfile together.
- Or stdlib: `python -m venv .venv` + `pip install -e ".[dev]"`.

## Gates

- `ruff check .` + `ruff format --check .` (apply: `ruff format .`).
- `mypy --strict src` (or configured strictness).
- `pytest --cov` in CI.
- `pre-commit` hooks (`.pre-commit-config.yaml`): ruff, ruff-format, mypy, plus `gitleaks` for secrets.

## Packaging & publishing

- Build backend: hatchling (default above) or setuptools; `uv build` → `dist/`.
- Version from `pyproject.toml` (dynamic via hatch-vcs if git-tagged).
- Publish: `uv publish` to PyPI (or TestPyPI first) with API token from env.
