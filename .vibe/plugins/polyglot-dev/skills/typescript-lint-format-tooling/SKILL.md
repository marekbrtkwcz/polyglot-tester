---
name: typescript-lint-format-tooling
description: Load this skill for lint/format/type tooling in JS/TS: Biome vs ESLint+Prettier, tsconfig strictness, pre-commit hooks, and CI quality gates that can actually fail.
---

# Lint, Format & Type Tooling

## Biome (recommended for new projects)

- One tool replaces ESLint + Prettier + import sorting: `biome check` (lint+format+assist), `biome check --write` to fix.
- `biome.json` at repo root; `organizeImports` on; run `biome ci` in CI (fails on any diff/error).
- Covers JS, TS, JSON, CSS; very fast, so no reason to skip in pre-commit.

## ESLint + Prettier (when already in place)

- Flat config (`eslint.config.js`); `typescript-eslint` recommended + strict configs; `eslint-plugin-import-x` or Biome assist for import order.
- Prettier for formatting only; disable conflicting rules (`eslint-config-prettier`).
- Type-aware linting needs `projectService` — enable it, the extra rules (no-floating-promises, no-misused-promises) catch real bugs.

## Type checking

- `tsc --noEmit` as a separate script and CI step — linters don't replace it.
- Strict base config; add `noUncheckedIndexedAccess` to catch missing boundary checks.

## Hooks & CI

- Pre-commit: lint-staged (or Biome directly) + husky, or plain git hooks; keep hooks fast (<10s) or people bypass them.
- CI gate must be able to fail: `biome ci`, `tsc --noEmit`, `vitest run` — not `|| true`, not continue-on-error.
- Cache node_modules and tool caches in CI (actions/cache, pnpm store) for speed.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
