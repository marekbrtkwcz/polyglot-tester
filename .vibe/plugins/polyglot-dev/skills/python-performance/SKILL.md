---
name: python-performance
description: Load this skill when optimizing Python: profiling with cProfile, memory profiling, caching, data structure choices, and knowing when to leave CPython.
---

# Python Performance

## Measure first

- `python -m cProfile -s cumulative script.py` — sort by cumulative time, find the hot spot.
- `python -m timeit -s "setup" "stmt"` for micro-benchmarks; compare with `pyperf` for reliable numbers.
- Memory: `memory_profiler` (`@profile` decorator + `mprof run`), `tracemalloc` for allocation traces.
- Rule: optimize the measured hot path, keep a benchmark test to lock the win.

## Common wins

- **Algorithm/data structure first**: `set`/`dict` lookup O(1) vs list O(n); avoid O(n²) loops — `any(x in big_list ...)` inside a loop is the classic.
- Caching: `functools.lru_cache`/`cache` on pure functions; cache expensive I/O at the boundary.
- Comprehensions and generator expressions over explicit loops (faster, less memory with genex).
- `__slots__` on dataclasses/classes with many instances — cuts memory and attribute lookup.
- Join strings with `"".join(...)` — not `+=` in a loop (quadratic due to immutability).
- Local variable binding in hot loops (`append = list.append`).

## I/O and concurrency

- I/O bound → asyncio or threads (see `python-concurrency`); batch DB queries (`WHERE id IN (...)`), use connection pooling.
- Release the GIL in C extensions; for CPU-bound work use processes or libraries that do (numpy, pandas, polars).

## When to leave CPython

- PyPy for long-running CPU-bound services; Cython/numba for numeric kernels; Rust/C extensions via PyO3/maturin for hot functions.
- Don't prematurely — profile first, and 90% of "slow Python" is an O(n²) or an N+1 query.

## Anti-patterns

- Optimizing without a profile.
- `lru_cache` on functions with mutable/unhashable args (crashes or wrong results) — or unbounded growth (use `maxsize`).
- Micro-optimizing cold code; readability wins outside hot paths.
