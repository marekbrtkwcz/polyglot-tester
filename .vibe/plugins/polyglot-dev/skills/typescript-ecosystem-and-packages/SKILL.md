---
name: typescript-ecosystem-and-packages
description: Load this skill for the JS/TS package ecosystem: npm/pnpm/yarn choice, package.json fields, semver, publishing to npm, evaluating dependencies, and monorepo tooling.
---

# Ecosystem & Packages

## Package managers

- npm: default, largest registry; pnpm: fast, disk-efficient, strict (recommended for monorepos); yarn: modern (berry) with workspaces; bun: fast runtime+pm.
- Pick one per repo; pin via `packageManager` field + corepack. Commit the lockfile.

## package.json essentials

- `name` (scoped `@org/name` for org packages), `version` (semver), `description`, `license`, `type`, `main`/`exports`/`types`.
- `exports` map is the modern entry point: define `.` with `types`, `import`, `require` conditions; keep `main` for legacy.
- `files` whitelist what gets published; `.npmignore` only when `files` isn't used; always exclude tests/src maps unless wanted.
- `scripts`: `prepublishOnly` runs build+test before publish — use it as a gate.

## Semver

- MAJOR breaking, MINOR backwards-compatible features, PATCH fixes. `^` allows minor updates; lockfile keeps you reproducible.
- 0.x.y: anything may change at any minor. Pre-1.0 libraries should move fast to 1.0 or stay clearly experimental.

## Evaluating a dependency

- Check: weekly downloads, last publish date, open issues/PRs, maintainer org, license, bundle size (bundlephobia), CVEs (osv.dev), whether it's deprecated or superseded.
- Prefer stdlib/platform APIs first (`fetch`, `crypto.randomUUID`, `structuredClone`, `Array.prototype.at`...).

## Publishing

- `npm publish --access public` for scoped; use provenance (`--provenance` in CI with OIDC) instead of long-lived tokens.
- Tag dist-tags: `latest`, `next`, `beta`; never force-overwrite a published version — publish a patch instead.
