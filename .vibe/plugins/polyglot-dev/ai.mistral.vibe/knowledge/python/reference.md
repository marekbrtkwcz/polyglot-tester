# Python Diagnostics Reference

Companion to the `debugging-polyglot` skill: the commands that answer
"where does it break".

## Pin down a failure

| Question | How |
|---|---|
| Full failing frame? | `pytest --tb=long -x` |
| One case only? | `pytest tests/test_x.py::test_name -v` |
| What is the state at failure? | `pytest --pdb`, or `breakpoint()` in source |
| Slowest tests? | `pytest --durations=10` |
| Is the data wrong or the code? | Print/assert the data at the boundary where it enters |

## Tooling

- `python -m pdb script.py` for non-test scripts (`b` break, `n` next,
  `p` print, `c` continue, `u`/`d` frame up/down).
- `python -X dev` enables dev mode: warnings shown, asyncio debug on.
- `PYTHONWARNINGS=error` turns ignored warnings into visible failures.

## Reading a traceback

- Innermost frame is **last**: read upward to find your call chain.
- `raise X from e` preserves the cause chain — the original error is at
  the bottom; never replace it with a bare message.
- `KeyError`/`IndexError` mid-chain: check the data shape at the
  producing function, not the consuming one.
- `ImportError` only in CI: usually an uninstalled/extra dependency or a
  different Python version.

## Everyday commands

- Sync env from lockfile (CI): `uv sync --locked --frozen`; locally `uv sync`.
- Fast test loops: `pytest -q -k name`, `pytest --lf` (last failed), `pytest -x`.
- Lint/format gate: `ruff check .` and `ruff format --check .` (apply with `ruff format .`).
- Types: `mypy --strict src` (incremental by default; `mypy --no-incremental` for a clean run).
- Coverage: `pytest --cov=mypackage --cov-report=term-missing`.

## CI debugging (Python)

- Version mismatch: CI uses the `setup-python` version — mirror it locally with `uv python install <ver>`.
- Missing dep in CI: the package's extras (`pip install -e ".[dev]"` / `uv sync --extra dev`).
- Vulnerability gate: `pip-audit` (or `uv run pip-audit`) in a separate CI job so it never blocks the test job.
