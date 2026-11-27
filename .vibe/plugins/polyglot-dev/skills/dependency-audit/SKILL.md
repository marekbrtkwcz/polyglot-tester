---
name: dependency-audit
description: Load this skill when auditing or updating project dependencies for vulnerabilities and drift in JavaScript/TypeScript, Python, or Go.
---

# Dependency Audit (Polyglot)

## Find known vulnerabilities

| Language | Command |
| --- | --- |
| JS/TS (npm) | `npm audit` / `npm audit --omit=dev` |
| JS/TS (pnpm/yarn/bun) | `pnpm audit` / `yarn audit` / `bun audit` |
| Python | `pip-audit` (install: `pip install pip-audit`); or `safety check` |
| Go | `govulncheck ./...` (install: `go install golang.org/x/vuln/cmd/govulncheck@latest`) |

- Fix **critical/high** findings first; for medium/low, check exploitability before scheduling.
- If a fix needs a major bump, weigh it: pin, replace, or accept with a dated waiver — never silently ignore.

## Check for outdated dependencies

| Language | Command |
| --- | --- |
| JS/TS | `npm outdated` / `pnpm outdated` / `bun outdated` |
| Python | `pip list --outdated` or `uv pip list --outdated` |
| Go | `go list -m -u all` |

- Update in small batches (one ecosystem area per PR), run the full test suite after each batch.
- Read the changelog of the dependency for breaking changes before bumping majors.

## Lockfiles and reproducibility

- Always commit the lockfile (`package-lock.json`, `pnpm-lock.yaml`, `uv.lock`, `go.sum`).
- CI should install from the lockfile only (`npm ci`, `uv sync --locked`, `go mod download`).

## Secrets in dependencies

- A dependency that phones home or bundles native code deserves a look: check its repo activity, maintainer, and install scripts (`postinstall`).
- Prefer lockfile + audit in CI as a recurring gate, not a one-off.
