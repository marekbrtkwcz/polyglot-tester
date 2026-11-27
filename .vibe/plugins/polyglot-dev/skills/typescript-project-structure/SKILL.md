---
name: typescript-project-structure
description: Load this skill for JS/TS project layout and toolchain: package.json hygiene, tsconfig, monorepos (npm/pnpm workspaces, Nx, Turborepo), lint/format gates, and folder conventions.
---

# Project Structure & Toolchain (JS/TS)

## Package hygiene

- Commit the lockfile; `package-lock.json` (npm), `pnpm-lock.yaml`, or `yarn.lock`.
- Scripts for everything repeatable: `dev`, `build`, `test`, `lint`, `typecheck`, `format`.
- `engines` field for required Node version; `packageManager` field pins npm/pnpm/yarn + version (corepack).
- `type: module` for ESM; be deliberate about ESM vs CJS interop (`exports` map with `types`/`import`/`require` conditions).

## tsconfig

- Extend a shared base (`@tsconfig/node20`, `@tsconfig/strictest`) instead of hand-rolling.
- `moduleResolution: "bundler"` for app code, `"node16"/"nodenext"` for published libraries.
- Project references (`references` + `composite`) for monorepo type-checking speed.

## Monorepos

- npm/pnpm/yarn workspaces for simple cases; pnpm preferred (strict node_modules, fast).
- Nx or Turborepo when you need caching, task graphs, affected-only runs.
- Shared code in `packages/`; apps in `apps/`; internal packages never published (`private: true`).

## Folder convention

```text
src/
  features/<name>/   # vertical slice: component + logic + tests
  shared/            # ui, lib, hooks, utils used across features
  app/ or main.ts    # composition root, wiring
tests/ or e2e/       # integration & E2E
```

## Gates

- Lint + format + typecheck in pre-commit (lint-staged / husky) and CI; Biome for new projects (one tool for lint+format), ESLint+Prettier when already set up.
- `tsc --noEmit` in CI; tests in CI; fail on `console.error` in app code where a logger exists.
