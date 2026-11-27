---
name: golang-performance
description: Load this skill when optimizing Go code: profiling with pprof, allocation reduction, escape analysis, string/builder tricks, and benchmarking discipline.
---

# Go Performance

## Measure first

- Never optimize on intuition. Profile: `go test -bench=. -cpuprofile=cpu.out -memprofile=mem.out ./pkg/`, then `go tool pprof cpu.out` (or `pprof -http=:8080` for the flame graph).
- Compare before/after with `benchstat old.txt new.txt` — single runs lie.
- Watch the three numbers: **time** (`-bench`), **allocs** (`-benchmem`: B/op, allocs/op), **regressions under `-race`**.

## Allocation discipline (the usual win)

- Preallocate slices when the size is known: `make([]T, 0, n)`.
- Reuse buffers via `sync.Pool` for hot paths (HTTP handlers, parsers).
- Strings: build with `strings.Builder` (preallocate `Grow`), never `s += x` in a loop.
- Avoid boxing: passing small structs by value beats interface{} when the concrete type is known at the call site.
- `fmt.Sprintf` in hot paths is slow — use strconv for scalars.

## Escape analysis

- `go build -gcflags="-m"` shows what escapes to the heap. Returning a pointer to a local forces heap allocation — return values when possible.
- Large structs passed by pointer avoid copies; small ones by value avoid indirection. Measure, don't guess.

## Concurrency perf

- Contention shows in profiles as `sync.Mutex` waits — shard the lock or use `sync.Map` only for read-heavy/write-rare cases.
- Bounded parallelism: `errgroup.SetLimit(n)` or a semaphore channel; more goroutines ≠ more throughput (context switching, cache thrash).

## I/O

- Buffer reads/writes (`bufio`) — syscall per byte is the classic mistake.
- Batch DB queries (one `WHERE id IN (...)` over N round-trips); use prepared statements (`db.Prepare` / `Stmt`).

## Rule

Optimize the hot path proven by a profile, keep the code readable, and add a benchmark so the win is locked in CI.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
