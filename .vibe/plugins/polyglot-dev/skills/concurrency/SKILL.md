---
name: concurrency
description: Load this skill when writing or reviewing concurrent or async code in JavaScript/TypeScript, Python, or Go — goroutines, channels and errgroup; asyncio vs threads vs processes; the event loop, promises and AbortController; cancellation and leak prevention. Once the language is known, also read the matching references/ file (go.md, python.md, ts.md) for language-specific depth.
---

# Concurrency & Async

- Concurrency bugs are timing bugs: keep shared state small and explicit; prefer message passing or immutable data over shared mutable state.
- Every long-running operation gets a cancellation path (context, task cancellation, AbortController) — fire-and-forget work leaks.
- Prove it under stress: race detectors, stress loops, and leak checks (goroutine dumps, pending task counts, open handles).

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | goroutines, channels, sync primitives, errgroup, context cancellation, leak prevention |
| Python | `references/python.md` | asyncio vs threads vs processes, the GIL, task cancellation, thread-safety |
| JavaScript/TypeScript | `references/ts.md` | event loop, promises, async/await pitfalls, parallelism vs sequential awaits, AbortController, worker threads |
