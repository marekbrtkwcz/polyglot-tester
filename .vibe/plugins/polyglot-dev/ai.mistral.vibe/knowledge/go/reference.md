# Go Diagnostics Reference

Companion to the `debugging-polyglot` skill: the commands that answer
"where does it break".

## Pin down a failure

| Question | How |
|---|---|
| One test, full output? | `go test ./pkg/... -run TestName -count=1 -v` |
| Cache lying to you? | `-count=1` — the default cache can hide a fix |
| Data race? | `go test -race ./...` (always on in CI) |
| Where is the CPU time? | `go test -cpuprofile=cpu.out ./pkg/ && go tool pprof cpu.out` |
| Goroutine leak? | `goleak` in `TestMain`; `runtime.NumGoroutine()` before/after |

## Tooling

- Debugger: `dlv test ./pkg/` (breakpoints: `break fn`, `continue`,
  `print x`, `goroutines`).
- Why is this slow? `pprof` web/serve for CPU, `-memprofile` for
  allocations; `-bench` + `-benchmem` for microbenchmarks.
- `go vet ./...` and `golangci-lint run` catch whole bug classes
  (printf mismatches, lost locks) before debugging starts.

## Reading a panic

- The runtime frames are at the top; your code starts below them.
- "panic: assignment to entry in nil map" → `make()` missing at the
  declaration site, not the write site.
- Deadlock detected: look for `sync.Mutex` held across a call that takes
  it again, or a channel nobody sends on/receives from.
