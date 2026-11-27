---
name: testing-polyglot
description: Load this skill when writing or running tests in JavaScript, TypeScript, Python, or Go: framework choice, structure, deterministic test data, running commands, and coverage.
---

# Testing (Polyglot)

## Choose the runner the repo already has

Detect before creating: look for config files — `vitest.config.ts` /
`playwright.config.ts` (JS/TS), `pyproject.toml` with pytest config (Python),
`*_test.go` files (Go). Never introduce a second framework alongside an
existing one.

## JavaScript / TypeScript

- Default runner: **Vitest** for units, **Playwright** for E2E/API.
- One behavior per test; name describes the observable outcome.
- Async assertions: always `await`; never `setTimeout` sleeps — use fake
  timers or auto-waiting assertions.
- Coverage: `vitest run --coverage`.

```ts
import { describe, it, expect } from "vitest";

describe("sum()", () => {
  it("adds two numbers", () => {
    expect(sum(2, 3)).toBe(5);
  });
});
```

## Python

- **pytest** with `tmp_path`, `monkeypatch`, `capsys` built-ins over
  hand-rolled fixtures.
- `pytest -q` to run; `-k name` to filter; `--lf` for last-failed.
- Type hints in test code; dataclasses for fixtures.
- Coverage: `pytest --cov=mypackage --cov-report=term-missing`.

```python
def test_sum():
    assert sum([2, 3]) == 5
```

## Go

- Table-driven subtests with `t.Run`, `t.Parallel` for independent cases.
- `go test ./...` runs everything; `-run TestName` filters; `-race` and
  `-count=1` belong in CI.
- Use `t.Cleanup` for teardown, `t.TempDir` for files, `t.Setenv` for env.

```go
func TestSum(t *testing.T) {
    tests := []struct{ name string; a, b, want int }{
        {"positive", 2, 3, 5},
        {"zero", 0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            if got := Sum(tt.a, tt.b); got != tt.want {
                t.Errorf("Sum(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

## Cross-language rules

- Test through public interfaces, not implementation details.
- Deterministic data: fixed seeds, no `Date.now()`/`time.Now()` in assertions
  — inject the clock.
- Each test cleans up its own state; no shared mutable fixtures.
- Boundary cases: empty, one, many, zero/negative, unicode, max sizes.
- A test that cannot fail proves nothing: every test must assert a real
  observable outcome.

## Related skills in other plugins

- `test-automation:writing-playwright-tests-best-practices`, `test-automation:api-playwright-test-developer` — Playwright UI/API test writing when the repo uses Playwright.
- `test-automation:diagnosing-test-failures`, `test-automation:stabilizing-flaky-tests` — failure classification and flake fixing.
- `qa-mcp` — Playwright MCP + Chrome DevTools MCP for live browser debugging, k6 MCP for load tests.
