# Testing Command Reference

Companion to the testing knowledge: how to run exactly one test, read
coverage that answers a question, and prove the suite is order-independent.

## Run exactly one test

| Runner | One test | By name pattern |
| --- | --- | --- |
| pytest | `pytest tests/test_x.py::test_y` | `pytest -k "discount and not bulk"` |
| Vitest | `vitest run tests/x.test.ts` | `vitest run -t "discount"` |
| Jest | `jest path/to/x.test.ts` | `jest -t "discount"` |
| Go | `go test ./pkg/` | `go test -run TestDiscount ./pkg/` |

## Coverage that answers a question

- pytest: `pytest --cov=src --cov-report=term-missing` — missing lines per
  module, not a global number.
- Vitest: `vitest run --coverage`; Jest: `jest --coverage` — read the
  uncovered lines of the files the change touched.
- Go: `go test -coverprofile=cover.out ./...` then
  `go tool cover -func=cover.out` (per-function) or `-html=cover.out`.
- Gate on the lines the change touched (diff coverage); a global percentage
  hides an untested diff behind old code.

## Prove order-independence

- pytest: `pytest-randomly` shuffles every run and prints its seed;
  `-p no:randomly` disables it when isolating a failure.
- Vitest: `vitest run --sequence.shuffle` (seed printed, `--sequence.seed`
  to reproduce).
- Go: `go test -shuffle=on ./...` — built into the toolchain.
- A test that only passes in one order is a flake with a reproducible
  trigger: fix the shared state, do not pin the order.

## Watch mode while developing

- Vitest: `vitest` (watch by default); Jest: `jest --watch`.
- pytest: `ptw` (pytest-watcher) re-runs on save.
- Go: no built-in watcher — run on save via the IDE or `entr`.

## When a test fails intermittently

- Reproduce the trigger, not the symptom: run the same test in a loop
  (`pytest --count 50` with pytest-repeat, or a shell loop) before touching
  the test; then fix the cause — timing, shared state, order, external dep.
