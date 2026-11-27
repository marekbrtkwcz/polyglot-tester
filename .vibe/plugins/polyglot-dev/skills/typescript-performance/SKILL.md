---
name: typescript-performance
description: Load this skill for JS/TS performance: profiling in Node and the browser, bundle size control, memory leaks, rendering performance, and measuring before optimizing.
---

# Performance in JS/TS

## Measure first

- Profile before optimizing: Node `--cpu-prof` / `node --inspect` + Chrome DevTools; browser Performance panel and Web Vitals (LCP, INP, CLS).
- Microbenchmarks lie: use `performance.now()` loops with warmup, or `tinybench`; measure p95/p99, not just average.

## Common wins

- Avoid unnecessary work in render loops (React: `useMemo`/`useCallback` only when profiling shows a cost; memoization itself has a cost).
- Virtualize long lists; debounce/throttle input handlers and scroll/resize listeners.
- Lazy-load routes and heavy modules (`import()` dynamic); code-split by route.
- `for...of` and `map` are fine; avoid `O(n²)` scans over large arrays — use `Map`/`Set` lookups.

## Memory

- Leaks: forgotten timers/intervals, event listeners on removed nodes, closures capturing large objects, growing caches without eviction (`Map` grows forever — use LRU).
- Heap snapshots in DevTools to find retained objects; `process.memoryUsage()` in Node.

## Bundle size

- Analyze with `source-map-explorer`, `webpack-bundle-analyzer`, or `vite-bundle-visualizer`.
- Tree-shaking needs ESM and side-effect-free packages (`sideEffects: false` in package.json).
- Prefer smaller deps (date-fns over moment, etc.); check bundlephobia.

## Node specifics

- Stream large data instead of buffering (`fs.createReadStream`, `pipeline`).
- `worker_threads` for CPU-bound work off the main thread.
- Keep the event loop free: no long synchronous JSON.parse of huge payloads on hot paths.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
