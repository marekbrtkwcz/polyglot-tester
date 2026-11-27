# CI/CD Diagnostics Reference

Companion to the workflow skills: the commands that answer "why did CI fail".

## Reading a failing run

| Question | Where |
| --- | --- |
| Which step failed? | Workflow run page → job → step annotation |
| Full log of one step? | Click the step → "Raw logs" |
| Why did my check not run? | `on:` triggers — push to non-listed branch, or `paths:` filter |
| Was it my change? | Re-run on the base commit: `gh run rerun <id>` after `git checkout` of base, or compare with main's latest run |

## Local reproduction

- `act` (nektos/act) runs workflows locally: `act push` / `act pull_request`.
- Or replicate the steps: same OS image (ubuntu-latest), same setup actions, same commands.
- Environment differences are the top cause: missing system deps → add `--with-deps` or a step `apt-get install`.

## Common failure classes

- **Runner exits 0 but tests failed** — the tool swallowed the exit code (e.g. JMeter); assert on the report file.
- **Flaky only in CI** — parallelism, timing, missing warm cache; add retries for infra steps only, never to mask a real failure.
- **Permission denied on push** — `permissions:` block too narrow; check workflow vs job level.
- **Secret not found** — secrets are per-environment; PRs from forks don't get secrets (use `pull_request_target` only with care).
- **Cache poisoning** — cache key too broad; include the lockfile hash in the key.

## Useful CLI

- `gh run list --workflow=CI` — recent runs.
- `gh run view <id> --log-failed` — failed step logs only.
- `gh api repos/:owner/:repo/actions/runs/:id/jobs` — job-level detail.
