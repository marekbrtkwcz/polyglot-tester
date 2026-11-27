---
name: performance
description: Load this skill when optimizing code in JavaScript/TypeScript, Python, or Go — measure-first discipline, per-language profiling tools, common wins, and locking the result with benchmarks in CI. Once the language is known, also read the matching references/ file (go.md, python.md, ts.md) for profiler- and tool-specific depth.
---
# Performance

## Measure first — always

Never optimize on intuition. Profile the real workload, optimize the proven hot path, and lock the win with a benchmark in CI.

- **JS/TS**: Node `--cpu-prof` / `--inspect` + DevTools; browser Performance panel and Web Vitals (LCP, INP, CLS); `performance.now()` loops with warmup or `tinybench`; measure p95/p99, not averages.
- **Python**: `python -m cProfile -s cumulative`, `timeit`/`pyperf` for micro-benchmarks, `memory_profiler`/`tracemalloc` for memory.
- **Go**: `go test -bench=. -benchmem -cpuprofile=cpu.out -memprofile=mem.out`, `go tool pprof` (or `pprof -http=:8080` flame graph); compare runs with `benchstat old.txt new.txt` — single runs lie.

## Common wins per language

- **JS/TS**: avoid work in render loops (`useMemo` only when profiling shows a cost), virtualize long lists, debounce/throttle handlers, lazy-load routes (`import()`), code-split, `Map`/`Set` instead of `O(n²)` scans, stream large data instead of buffering, `worker_threads` for CPU-bound work.
- **Python**: algorithm/data structure first (`set`/`dict` O(1) vs list O(n), no `O(n²)` loops), `functools.lru_cache(maxsize=...)` on pure functions, comprehensions/genex, `__slots__`, `"".join(...)`, local-variable binding in hot loops, batch DB queries, connection pooling. CPU-bound → numpy/pandas/polars or processes; I/O-bound → asyncio/threads.
- **Go**: preallocate slices (`make([]T, 0, n)`), `strings.Builder` with `Grow` (never `s += x` in a loop), `sync.Pool` for hot-path buffers, `strconv` over `fmt.Sprintf`, escape analysis (`-gcflags="-m"`), `bufio` for I/O, prepared statements, batch `WHERE id IN (...)`, bounded parallelism (`errgroup.SetLimit`).

## Memory

- **JS/TS**: heap snapshots to find retained objects; leaks = forgotten timers/listeners, closures capturing large objects, unbounded `Map` caches (use LRU).
- **Python**: `tracemalloc`, `__slots__`, genex over lists.
- **Go**: `-benchmem` B/op and allocs/op; watch heap profiles.

## Cross-language rules

- Algorithmic complexity beats micro-optimization in every language — an `O(n²)` loop is slow everywhere.
- Fix N+1 query patterns before profiling code.
- Keep the event loop / hot path free of large synchronous work (huge JSON.parse, blocking I/O).
- Bundle size matters for JS/TS: analyze with bundle visualizers, tree-shake (ESM + `sideEffects: false`), prefer smaller deps.
- Add the benchmark to CI so the improvement can't silently regress.

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | pprof profiling, allocation reduction, escape analysis, string/builder tricks, benchmarks |
| Python | `references/python.md` | cProfile, memory profiling, caching, data structure choices, when to leave CPython |
| JavaScript/TypeScript | `references/ts.md` | Node and browser profiling, bundle size, memory leaks, rendering performance, measure-first |
