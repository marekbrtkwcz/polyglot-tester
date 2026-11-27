---
name: ci-cd-polyglot
description: Load this skill when setting up or changing CI/CD for a JS/TS, Python, or Go project — workflow structure, per-language test/lint gates, matrix builds, caching, secrets, and merge gating.
---

# CI/CD (Polyglot)

Primary target: **GitHub Actions** (see knowledge `ci-cd` for the full reference). The same shape maps to GitLab CI / other runners: jobs on fresh runners, nothing persists unless cached or uploaded as an artifact.

## Workflow anatomy

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pytest -q
```

- Trigger on `pull_request` (every change) and on `push` to `main`; use `branches:` filters so feature-branch noise stays out of the release signal.

## Per-language gates

- **JS/TS**: `npm ci` (lockfile), `tsc --noEmit`, eslint/biome, `vitest run --coverage` (or jest); Playwright: `npx playwright install --with-deps chromium`.
- **Python**: `uv sync` or `pip install -r requirements.txt` / `pip install -e .`, `ruff check`, `mypy`, `pytest -q`; matrix over supported versions (3.11–3.14).
- **Go**: `go build ./...`, `go vet ./...`, `golangci-lint run`, `go test -race -count=1 ./...`; matrix over the last two Go minors.

## Matrix builds and caching

- Matrix per language version so EOL drift is visible; drop EOL versions when they leave support.
- Cache the package manager against the lockfile (`actions/setup-node` `cache: npm`, `actions/setup-python` `cache: pip`, `actions/setup-go`); cache Playwright browsers on `~/.cache/ms-playwright`.
- Cache Go module/build cache (`~/.cache/go-build`, `GOMODCACHE`) on larger repos.

## Secrets and gating

- Secrets only via the runner's secret store (`secrets.*`) — never echoed, never in env files committed to the repo. OIDC trusted publishing for packages where available.
- Branch protection: require the CI jobs as status checks; keep a fast smoke job separate from the full suite (full on merge/nightly, smoke on PR).
- Upload test reports / coverage as artifacts on failure for debugging.

## Release automation

- Tag-triggered release workflow: build, run the full gate, draft release notes from merged PRs (release-drafter), publish.
- Version bump in the manifest (`plugin.json`, `pyproject.toml`, `go.mod` tag) together with the changelog entry in one PR — see `release-and-changelog`.

## Cross-references

- Knowledge `ci-cd` (GitHub Actions reference), `docker-polyglot` for container-based CI, `stay-updated` for keeping CI versions current.
