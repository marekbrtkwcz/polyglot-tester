---
name: python-ecosystem
description: Load this skill when choosing Python libraries: how to evaluate a package on PyPI, and curated picks by category (HTTP, CLI, data, testing, utils).
---

# Python Ecosystem & Library Selection

## Evaluating a PyPI package

1. **Maintenance**: last release date, commit activity, issue response time on GitHub.
2. **Adoption**: dependents (libraries.io / PyPI stats), downloads trend.
3. **Quality signals**: typed (py.typed), tests in CI, `ruff`/`mypy` clean, changelog, license (MIT/Apache/BSD).
4. **Size of dependency tree**: `uv pip tree` / `pipdeptree` after adding — a small tree is a feature.
5. **Security**: `pip-audit` after adding; check for known CVEs.
6. Stdlib first: check what 3.12+ already covers before adding anything.

## Curated picks by category

- **HTTP client**: `httpx` (sync+async, HTTP/2) — over `requests` for new code.
- **CLI**: `typer` (type-hint based, great DX) or `click`; stdlib `argparse` for zero-dep scripts.
- **Config/settings**: `pydantic-settings` (env + files + validation).
- **Data validation**: `pydantic` v2.
- **Data processing**: `polars` (fast DataFrames) over pandas for new analytics; `pandas` when ecosystem matters.
- **Testing**: `pytest`, `pytest-asyncio`, `respx` (httpx mocking), `hypothesis`, `mutmut`.
- **HTTP mocking**: `respx` (httpx), `responses` (requests).
- **Templating**: Jinja2 (autoescape on).
- **Task queue**: `celery`, `arq`, `dramatiq`.
- **Utils**: `more-itertools`, `python-dateutil` (careful), `rich` (CLI output), `tenacity` (retry), `cachetools`.
- **Date/time**: stdlib `datetime`/`zoneinfo` — avoid `pytz`.
- **Serialization**: stdlib `json`; `orjson` for speed; msgpack via `msgpack` when needed.

## Dependency hygiene

- Lock everything: `uv.lock` or `requirements.txt` with hashes (`pip-compile --generate-hashes`); CI installs with `--require-hashes` / `uv sync --locked`.
- One new dependency per PR with the reason written; review its tree.
- `pip-audit` + `bandit` in CI as recurring gates.
- Awesome-python lists for vetted options by category.
