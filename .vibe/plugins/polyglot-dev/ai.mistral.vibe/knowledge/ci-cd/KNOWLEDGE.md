---
name: ci-cd
description: CI/CD with GitHub Actions: workflows, jobs, matrix builds, caching, secrets, and gating merges on checks.
display_name: CI/CD
icon: workflow
---

# CI/CD Reference (GitHub Actions)

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

- `on.push.branches` limits when push runs fire; `pull_request` fires for PRs.
- Each job runs on a fresh runner; nothing persists unless cached or uploaded as an artifact.

## Matrix builds

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13", "3.14"]
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

## Caching

- `actions/setup-python` caches pip automatically when a lockfile/requirements file is present (`cache: pip`).
- `actions/setup-node` caches npm/pnpm/yarn with `cache:` + lockfile.
- Playwright browsers: `npx playwright install --with-deps chromium` (cache via `actions/cache` on `~/.cache/ms-playwright`).

## Secrets and permissions

- Secrets via `secrets.NAME` in `env` or step `with` — never hardcode tokens.
- Set least-privilege permissions: `permissions: { contents: read }` at workflow or job level.
- Gate merges: in repo Settings → Branches → require status checks; mark slow jobs as non-blocking.

## Useful patterns

- Fail on test failure even when the runner exits 0: assert on the report file, not the exit code.
- Upload artifacts on failure for debugging: `actions/upload-artifact@v4` with `if: failure()`.
- Reusable workflows: `jobs.<id>.uses: org/repo/.github/workflows/x.yml@main`.
- Concurrency: cancel superseded runs on the same PR:
  `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }`.
