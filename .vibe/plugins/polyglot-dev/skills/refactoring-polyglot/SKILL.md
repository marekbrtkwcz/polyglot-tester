---
name: refactoring-polyglot
description: Load this skill when refactoring code in JavaScript/TypeScript, Python, or Go — test-first discipline, one transformation per green step, mechanical rename/move tooling, and never mixing a refactor with a behavior change.
---

# Safe Refactoring (Polyglot)

## The process — identical in every language

1. Read the target module **and its callers**; confirm the suite, linter, and type checker are green BEFORE touching anything.
2. If coverage is missing on the target, add **characterization tests** first — pin current behavior so the refactor proves it didn't change.
3. **One transformation per step**, each step green: rename → extract → move → change signature. Commit between steps on large refactors.
4. **Never mix a refactor with a behavior change** in one commit — that's a behavior change wearing a refactor's clothes. Never weaken or delete a test to make a refactor pass.
5. If a step breaks the build and the fix isn't obvious in minutes, revert that step and report the state.

## Rename/move with the tool, never by hand

- **Go**: `gopls rename` (or IDE), then `git grep` to confirm; `go build ./... && go vet ./... && golangci-lint run` after each step.
- **Python**: IDE/jedi or **rope** for project-wide rename and move; `ruff check --select F401,F811` + `mypy --strict` after each step.
- **JS/TS**: tsserver/IDE rename, then `tsc --noEmit` + eslint/biome; `git grep` for leftover references.

## Common safe moves (all languages)

- **Extract function/component** when a block has a name-able purpose — explicit params in, explicit return out, no globals.
- **Introduce a parameter object** (struct / dataclass / options object) when a function grows past ~4 params.
- **Replace growing if-else chains** with dict/map dispatch or strategy objects.
- **Move code to the module that owns the concept**; by feature, not by layer. Re-export at the old path if it's public API, then deprecate.
- **Delete dead code completely** — no commented-out blocks, no unused params kept "just in case".

## When NOT to refactor

- Right before a release (unless it's a bug fix).
- Without tests on the code being moved.
- "While I'm here" scope creep — unrelated cleanups go in a separate PR.

## Per-language depth

`golang-refactoring`, `python-refactoring`, `typescript-refactoring`.
