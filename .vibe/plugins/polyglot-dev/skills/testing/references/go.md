# Go Testing (Advanced)

## Table-driven tests

The default shape for any function with multiple cases:

```go
func TestSum(t *testing.T) {
    tests := []struct {
        name string
        in   []int
        want int
    }{
        {"empty", nil, 0},
        {"positives", []int{2, 3}, 5},
        {"with negative", []int{5, -2}, 3},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // only if the test has no shared state
            if got := Sum(tt.in); got != tt.want {
                t.Errorf("Sum(%v) = %d, want %d", tt.in, got, tt.want)
            }
        })
    }
}
```

- `t.Parallel()` for independent cases; never for tests sharing files, ports, or env.
- `t.Cleanup` for teardown (runs even on failure), `t.TempDir()` for files, `t.Setenv` for env.

## testify (require/assert)

- `require` fails fast (`t.FailNow`) — for setup and invariants; `assert` continues — for multiple checks on one result.
- `require.ErrorIs(t, err, ErrNotFound)`, `assert.Equal(t, want, got)`, `assert.InDelta` for floats.

## Mocks

- Mock **interfaces you own**, at the narrowest boundary (e.g. `type UserStore interface { Get(id string) (*User, error) }`).
- Hand-written fakes are often clearer than generated mocks for small interfaces; use `github.com/stretchr/testify/mock` or `go.uber.org/mock` (gomock) for bigger ones.
- `httptest.NewServer` for HTTP dependencies — real server, real client, no mocking of the transport.

## Fuzz and property tests

```go
func FuzzParse(f *testing.F) {
    f.Add([]byte("valid input"))
    f.Fuzz(func(t *testing.T, in []byte) {
        out, err := Parse(in)
        if err == nil {
            _, err2 := Parse(out) // round-trip must not error
            if err2 != nil { t.Fatalf("round-trip failed: %v", err2) }
        }
    })
}
```

Run: `go test -fuzz=FuzzParse -fuzztime=30s ./pkg/`.

## Benchmarks

- `go test -bench=. -benchmem ./...`; compare with `benchstat` (old vs new results).
- Benchmarks belong next to the code; keep them deterministic (fixed data, no network).

## CI gate

`go test -race -count=1 ./...` — `-race` for the data race detector, `-count=1` to bypass the result cache. Add goleak in `TestMain` for packages that spawn goroutines.

## Related skills in other plugins

- `test-automation:writing-playwright-tests-best-practices`, `test-automation:api-playwright-test-developer` — Playwright UI/API test writing when the repo uses Playwright.
- `test-automation:diagnosing-test-failures`, `test-automation:stabilizing-flaky-tests` — failure classification and flake fixing.
- `qa-mcp` — Playwright MCP + Chrome DevTools MCP for live browser debugging, k6 MCP for load tests.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
