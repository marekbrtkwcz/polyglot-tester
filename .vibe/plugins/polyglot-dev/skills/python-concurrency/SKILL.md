---
name: python-concurrency
description: Load this skill when writing concurrent or async Python: choosing asyncio vs threads vs processes, the GIL, task cancellation, and thread-safety.
---

# Python Concurrency

## Choose the model by the bottleneck

| Bottleneck | Model | Tools |
| --- | --- | --- |
| I/O (network, disk, DB) | **asyncio** | `async`/`await`, `asyncio.gather`, `aiohttp`, `asyncpg` |
| CPU-bound work | **processes** | `concurrent.futures.ProcessPoolExecutor`, `multiprocessing` |
| Blocking legacy libs in async code | **threads** | `asyncio.to_thread`, `ThreadPoolExecutor` |
| Simple parallel map over data | either | `ThreadPoolExecutor` (I/O) / `ProcessPoolExecutor` (CPU) |

## The GIL

- CPython's GIL means **threads don't run Python bytecode in parallel** — threads help only when waiting on I/O (the GIL is released during I/O syscalls).
- For CPU parallelism use processes (or C extensions/numpy that release the GIL).

## asyncio essentials

```python
async def main():
    results = await asyncio.gather(fetch(a), fetch(b), fetch(c))  # concurrent
    # return_exceptions=True to not fail-fast on first error


async with aiohttp.ClientSession() as session:
    ...  # one session per app
```

- One `event loop` per thread; `asyncio.run(main())` at the top level.
- Cancellation: `task.cancel()` → `asyncio.CancelledError` inside the task; use `try/finally` or `async with` for cleanup — always.
- `asyncio.create_task` for background work; keep a reference to tasks or they may be GC'd mid-flight.
- Never block the loop: no `time.sleep` (use `await asyncio.sleep`), no sync I/O — wrap with `await asyncio.to_thread(fn, ...)`.

## concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=10) as ex:
    futures = [ex.submit(work, item) for item in items]
    for f in as_completed(futures):
        result = f.result()  # raises the worker's exception here
```

- `max_workers`: I/O → 10–50; CPU → `os.cpu_count()`.
- Exceptions surface on `.result()` — handle per-future, don't let one kill the batch silently.

## Thread safety

- Shared mutable state needs `threading.Lock` (or `queue.Queue`, which is thread-safe by design — prefer it for producer/consumer).
- asyncio is single-threaded — no locks needed *within* the loop; needed only when crossing to threads.
- Globals + mutation = race in threads; pass state explicitly.

## Anti-patterns

- `asyncio.run()` called twice in one process (loop already running → error); use one loop per app or `nest_asyncio` as a last resort.
- Fire-and-forget tasks without keeping references.
- `ProcessPoolExecutor` with lambdas (not picklable) — use top-level functions.
