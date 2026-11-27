---
name: testing
description: Testing strategy across JavaScript/TypeScript, Python, and Go: test levels, runner choice per repo, deterministic data, flakiness, and coverage that means something.
display_name: Testing
icon: flask
---

# Testing Reference (Polyglot)

## Test levels

- **Unit**: pure logic, fast, no I/O — the bulk of the suite.
- **Integration**: module boundaries, DB, HTTP — real dependencies or containers.
- **E2E**: user-visible flows through the real stack — few, slow, high signal.

## Runner per language

- **JS/TS**: Vitest (Vite projects, Jest-compatible API), Jest, or `node:test` for zero-dep libs; Playwright Test for E2E/API.
- **Python**: pytest — fixtures, parametrize, monkeypatch; hypothesis for property-based.
- **Go**: stdlib `testing` — table-driven subtests, `t.Parallel`, `t.Cleanup`, fuzzing.

## Determinism rules

- No sleeps/wait-for-it in tests — use polling with timeout or framework waits.
- Fixed clocks and seeded randomness (fake timers, `random.seed`, fixed UUID source).
- Unique test data per test (factories + unique suffixes) so parallel workers never collide; clean up in teardown even on failure.
- Tests must pass shuffled and in parallel — run the suite that way in CI once.

## Flakiness

- A flake is a bug report, not a retry excuse: diagnose root cause (timing, shared state, order, external dep).
- Quarantine only with an owner and an expiry date; a retry in CI must never mask a real failure.

## Coverage

- Gate on diff coverage (lines the change touched), not global percentage.
- Mutation testing (Stryker for JS/TS) reveals tests that execute code without asserting it.

## Official sources

- pytest: docs.pytest.org · hypothesis: hypothesis.readthedocs.io · fast-check: github.com/dubzzz/fast-check · Playwright: playwright.dev · Go testing: go.dev/doc/tutorial/add-a-test
