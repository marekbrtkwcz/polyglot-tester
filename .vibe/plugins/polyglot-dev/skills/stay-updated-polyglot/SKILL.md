---
name: stay-updated-polyglot
description: Load this skill when upgrading runtimes, toolchains, or dependencies in JavaScript/TypeScript, Python, or Go — official sources per language, EOL schedules, and a safe one-thing-at-a-time upgrade routine.
---

# Staying Updated (Polyglot)

## Official sources per language

- **Go**: release notes at go.dev/doc/devel/release (language changes in the "Go 1.x" section), go.dev/blog, pkg.go.dev for stdlib additions — check the stdlib before hand-rolling a helper.
- **Python**: python.org/downloads for EOL status (each 3.x gets ~5 years), What's New at docs.python.org/3/whatsnew/3.x.html (read the **Deprecated** and **Removed** sections), PEP index at peps.python.org.
- **JS/TS**: TypeScript release notes (typescriptlang.org/docs/handbook/release-notes), ECMAScript proposals at tc39.es/proposals (wait for stage 4 before relying on a feature), Node LTS schedule at nodejs.org/en/about/previous-releases, MDN and web.dev for the web platform.

## Safe upgrade routine — same shape everywhere

1. Read the changelog / migration notes for the target major **before** upgrading.
2. Upgrade **one thing at a time** (runtime → compiler → linter → deps) so failures are attributable.
3. Run the full gate after each step: tests + type check + lint.
4. Update CI matrix, Docker base image, and floor metadata (`python_requires`, `go` directive in go.mod + `go mod tidy`, `engines` in package.json) **in the same PR**.
5. Surface future breakage early: Python `-W error::DeprecationWarning`, TS `--deprecation` — on the new version in CI.

## Per-language specifics

- **Go**: since 1.21 the toolchain enforces backward compatibility — bump the `go` directive and modernize with `gopls modernize ./...` (`interface{}`→`any`, `sort.Slice`→`slices.SortFunc`, `for i := range n`); review the diff like a PR. Gate: `go build ./... && go vet ./... && go test -race -count=1 ./...`.
- **Python**: upgrade the venv first (`uv python install 3.13`), fix deprecations one category at a time; check dependency compatibility — many libs lag a release behind.
- **JS/TS**: bump Node to the current LTS, then TS, then deps; enable new strictness flags incrementally; wait for stage-4/baseline-widely-available before using new JS features, polyfill or transpile otherwise.

## Dependency hygiene (all languages)

- Monthly: outdated-deps report (`npm outdated`, `uv pip list --outdated` / `pip list --outdated`, `go list -m -u all`), review Renovate/Dependabot PRs, apply safe security fixes (`npm audit fix`, `pip-audit`, `govulncheck` — see `dependency-audit`).
- Major dep bumps: read migration guides, run E2E tests, watch the error tracker after deploy.
- Lockfiles committed; drop EOL versions from the CI matrix.

## Per-language depth

`golang-stay-updated`, `python-stay-updated`, `typescript-stay-updated`.
