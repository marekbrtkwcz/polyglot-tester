---
name: unit-testing-polyglot
description: Load this skill when writing unit tests in JavaScript/TypeScript, Python, or Go — the fast, isolated layer: structure, assertions, mocks/doubles, deterministic data, and running just one test. For suite-level concerns — framework choice, structure across layers, coverage — prefer testing.
---

# Unit Testing (Polyglot)

Unit tests: no network, no DB, no filesystem, no clock — pure logic, milliseconds each.

## JS/TS (Vitest / Jest)

```ts
import { describe, it, expect, vi } from 'vitest';

describe('price', () => {
  it('applies the discount', () => {
    expect(applyDiscount(100, 10)).toBe(90);
  });
});
```

- Mock modules with `vi.mock('./api')`, not by rewiring imports; inject dependencies where possible (cleaner than mocks).
- `vi.useFakeTimers()` for time; restore in `afterEach`.
- Run one test: `vitest -t 'applies the discount'`; watch mode `vitest` locally.

## Python (pytest)

```python
def test_apply_discount():
    assert apply_discount(100, 10) == 90
```

- Plain `assert` — pytest rewrites it with useful diffs; fixtures for setup (`@pytest.fixture`), `parametrize` for cases, `monkeypatch` for env/attrs.
- Run one test: `pytest -k apply_discount`; `-x` to stop at first failure.

## Go (stdlib testing)

```go
func TestApplyDiscount(t *testing.T) {
    cases := []struct{ price, pct, want int }{{100, 10, 90}, {0, 10, 0}}
    for _, c := range cases {
        t.Run(fmt.Sprintf("%d/%d", c.price, c.pct), func(t *testing.T) {
            if got := applyDiscount(c.price, c.pct); got != c.want {
                t.Errorf("got %d, want %d", got, c.want)
            }
        })
    }
}
```

- Table-driven is the idiom; `t.Parallel()` for independent cases; `t.Cleanup` for teardown; `httptest.NewServer` for HTTP handlers.
- Run one test: `go test -run TestApplyDiscount ./...`; `-count=1` to bypass cache; `-race` in CI.

## Rules that apply everywhere

- Test behavior through the public interface, not internals.
- One behavior per test; name states the outcome.
- Deterministic: fixed data (factories), no real clock/network, unique values per test.
- A test that cannot fail proves nothing — assert a real observable outcome.
- Fast feedback: keep the unit layer under a few seconds; slow integration belongs in the integration layer.

## Related

- `testing` — the full strategy: levels, runner choice, coverage that means something.
- Knowledge `testing` — determinism rules, flake policy, and the command reference.
