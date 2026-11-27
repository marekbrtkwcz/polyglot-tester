---
name: debugging-polyglot
description: Load this skill when diagnosing a failing test, crash, or reported defect in JavaScript, TypeScript, Python, or Go: classify the failure, build a reproduction loop, and isolate the root cause per language.
---

# Debugging (Polyglot)

## 1. Classify before touching code

Every failure is one of: product defect, test bug, environment issue,
flaky timing, or bad test data. Classify first — the rest of the loop
depends on the class. A failure that only appears under load or parallelism
is a timing/state problem; treat it as such from the start.

## 2. Reproduce

- Reduce to the smallest input and the fewest steps that still fail.
- Red on the exact symptom, not a nearby one: same command, same
  environment, same data.
- If it cannot be reproduced, say so and stop — do not "fix" what you
  cannot see fail.

## 3. Isolate — one falsifiable hypothesis per change

Change one variable at a time and re-run the reproduction after each.
Keep a note of what you ruled out. Two failed attempts of the same idea
mean the hypothesis is wrong, not that it needs a bigger hammer.

## 4. Fix at the class level

Fix the cause, not the symptom: no widened try/except, no raised timeout,
no assertion weakened to match observed behavior. If the fix cannot land
now, record the constraint — never silence the failure.

## Per language

### JavaScript / TypeScript

- Read the stack trace bottom-up; the first frame in your code is the
  entry point, not the top line.
- `TypeError: cannot read property 'x' of undefined` — trace where the
  value enters, not where it explodes.
- Async: an error in a floating (unawaited) promise vanishes silently;
  attach a `catch` or await it to surface it.
- Node: `--stack-trace-limit`, `ndb`/Chrome DevTools for breakpoints;
  log intermediate promises before blaming the framework.

### Python

- `pytest --tb=long -x` for the full failing frame; `pytest path::test`
  to run the exact failing case.
- `--pdb` drops into the failing state; `breakpoint()` in source.
- Traceback read order: innermost frame last. `raise ... from e` keeps
  the original cause visible — never swallow it with a bare `except`.
- `KeyError`/`AttributeError` mid-chain usually means a shape mismatch
  earlier: print the data at the boundary where it entered.

### Go

- `go test ./pkg/... -run TestName -count=1 -v` — one test, no cache,
  full output.
- Panics print the goroutine stack: the top frames are the runtime, your
  code starts below them.
- `errors.Is` / `errors.As` to check wrapped errors; `%w` in `fmt.Errorf`
  keeps the chain inspectable.
- Race or leak: `go test -race`, `goleak` in TestMain; a goroutine that
  never exits is a lifecycle bug, not flaky infra.

## 5. Close the loop

Add the regression test that fails without the fix, then verify the whole
affected suite (not just the new test) passes. Report: root cause, the fix,
and the test that pins it.
