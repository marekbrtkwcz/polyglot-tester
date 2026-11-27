---
name: typescript-async-concurrency
description: Load this skill for async JavaScript/TypeScript: the event loop, promises, async/await pitfalls, parallelism vs sequential awaits, cancellation with AbortController, and worker threads.
---

# Async & Concurrency in JS/TS

## Event loop basics

- JS is single-threaded: one call stack, one event loop. Long synchronous work blocks everything (UI, timers, I/O callbacks).
- `setTimeout(fn, 0)` is not "next tick" — it's a macrotask with a minimum delay; `queueMicrotask` runs before the next macrotask.

## Promises

- A promise is created hot (executor runs immediately) — don't create promises you won't use.
- `Promise.all` fails fast on first rejection; `Promise.allSettled` waits for all (use for independent best-effort calls).
- `Promise.race` for timeouts: `Promise.race([work, timeout])`.
- Avoid the classic bug: `await` inside `forEach` doesn't serialize — use `for...of` with `await`, or `Promise.all` with `map`.

```ts
// wrong: sequential intent, parallel execution, unhandled rejections
const results = [];
items.forEach(async (item) => { results.push(await save(item)); });

// right: parallel
const results = await Promise.all(items.map(save));

// right: sequential when order/rate matters
for (const item of items) { await save(item); }
```

## Cancellation

- Use `AbortController`/`AbortSignal` for fetch and anything cancellable; pass the signal down.
- Check `signal.aborted` in long loops; rethrow `DOMException` named `AbortError` untouched.

## Concurrency control

- Limit parallelism with a small pool helper (e.g. `p-limit`) — unbounded `Promise.all` over thousands of items exhausts sockets/memory.

## Worker threads (Node)

- `node:worker_threads` for CPU-bound work; communicate via `postMessage` (structured clone).
- Keep workers small and stateless; a worker pool for repeated tasks.
- Browser: `Worker` for the same purpose; `SharedArrayBuffer` only with COOP/COEP headers.

## Timers

- Always `clearTimeout`/`clearInterval` on cleanup paths.
- `setInterval` drifts; for periodic work prefer recursive `setTimeout`.
