# Safe Refactoring (Python)

## Process

1. Read the target module **and its callers/imports** (`grep` for the symbol, check `__init__.py` re-exports).
2. Confirm the test suite, mypy, and ruff are green BEFORE touching anything.
3. One transformation per step, each step green: rename → extract function → move module → change signature.
4. Never mix a refactor with a behavior change in one commit.

## Mechanical tools

- IDE/jedi or **rope** for project-wide rename and move — they update imports; never hand-edit 40 import lines.
- `ruff check --select F401,F811` after moves to catch unused/undefined imports; `mypy` to catch signature drift.

## Common safe moves

- Extract function: pull a block into a function with explicit params and return — no globals.
- Introduce a parameter object (dataclass) when a function grows past ~4 params.
- Replace conditionals with a dict dispatch / strategy objects when the branch list grows.
- Move code to the module that owns the concept; re-export in `__init__.py` if the old path is public API (then deprecate it).

## Behavior preservation

- Type hints are your safety net: `mypy --strict` before and after should show the same (zero) errors.
- Characterization tests: pin current behavior of a tricky function with tests BEFORE refactoring it, so the refactor proves it didn't change.
- Never weaken or delete a test to make the refactor pass — that's a behavior change wearing a refactor's clothes.

## When to stop

- If a step breaks the build and the fix isn't obvious in minutes, revert that step and report the state — don't pile on changes.

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
