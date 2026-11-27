---
name: feature-workflow
description: Load this skill when implementing a new feature, bug fix, or refactor in JavaScript, TypeScript, Python, or Go. Covers the end-to-end delivery loop: understand, plan, test-first implement, verify, review, and hand off. For just the review step prefer code-review-polyglot; for just the refactor mechanics prefer refactoring-polyglot.
---

# Feature Workflow (Polyglot)

A language-agnostic delivery loop. Use the knowledge folders
`polyglot-dev:javascript-typescript`, `polyglot-dev:python`, and
`polyglot-dev:go` for language-specific commands and conventions.

## 1. Understand

- Read the relevant code and its callers before changing anything.
- Identify the language, runtime, package manager, and test runner actually
  used in this repo — do not assume.
- State the deliverable in one sentence: what behavior changes, what stays
  intact.

## 2. Plan

- List the files to touch and the behavior each change produces.
- Decide the test level: unit for logic, integration for boundaries, E2E only
  for user-visible flows.
- For a bug fix, write the failing test first (see the `testing-polyglot`
  skill).

## 3. Implement

- Make the smallest coherent change; preserve public interfaces unless the
  task requires changing them.
- Match the repo's existing style: naming, imports, error handling, typing
  strictness (TS strict flags, Python type hints, Go idiom).
- No speculative abstractions, no defensive branches unrelated to the task.

## 4. Verify

Run the checks that can actually fail because of this change:

| Language | Format/Lint | Type check | Tests |
| --- | --- | --- | --- |
| JS/TS | `biome check .` (or repo linter) | `tsc --noEmit` | `npm test` / `bun test` |
| Python | `ruff check .` / `ruff format --check .` | `mypy --strict` (if configured) | `pytest` |
| Go | `gofmt -l .` | `go vet ./...` | `go test ./...` |

- Read the output; a green exit code with skipped tests is not verification.
- Distinguish your failure from a pre-existing or environmental one before
  fixing.

## 5. Review

Run the `code-review-polyglot` checklist on the diff before handing off.

## 6. Hand off

- Commit with a message describing the behavior change, not the activity.
- Summarize: what changed, what was verified (with the actual command and
  result), what remains unverified and why.
