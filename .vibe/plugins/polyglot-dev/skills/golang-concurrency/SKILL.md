---
name: golang-concurrency
description: Load this skill when writing or reviewing concurrent Go code: goroutines, channels, sync primitives, errgroup, context cancellation, and leak prevention.
---

# Go Concurrency

## Rules of thumb

- **Goroutines are cheap, leaks are not**: every goroutine must have a guaranteed exit. If you can't name who stops it, don't start it.
- **Channels over shared memory when ownership transfers**; `sync.Mutex` when state is shared. Pick one per variable and comment it.
- A channel must have a **single closer** (`close(ch)` by the sender only), and closing happens exactly once.

## Patterns

```go
// Worker pool with errgroup + context cancellation
func processAll(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    for _, it := range items {
        it := it // pre-1.22; unnecessary since Go 1.22
        g.Go(func() error {
            return process(ctx, it) // ctx cancelled on first error
        })
    }
    return g.Wait() // first error wins, others see cancelled ctx
}
```

- `errgroup.WithContext` cancels siblings on first error — the standard fan-out shape.
- `sync.WaitGroup` only when errors don't matter; prefer errgroup when they do.
- Fan-in: one goroutine per source writing to a shared channel, closed after `wg.Wait()`.
- `select` with `default` = non-blocking try; with `ctx.Done()` = cancellable wait. Never `select {}` (blocks forever).

## Context

- Pass `ctx` as the **first parameter**; store it in structs only for request-scoped services, never in data/config structs.
- Check `ctx.Err()` at loop tops and before expensive work; don't check after every line.
- Never `context.Background()` inside a library function that received a ctx.

## Leaks and races

- Run `go test -race ./...` in CI — always.
- Detect leaks in tests: `go.uber.org/goleak` in `TestMain`, or compare `runtime.NumGoroutine()` before/after.
- Common leak: goroutine blocked on send to a channel nobody reads after the receiver gave up (ctx done) — always pair sends with `select { case ch <- v: case <-ctx.Done(): }`.

## Anti-patterns

- Starting a goroutine per request without a bound (use a semaphore channel or errgroup `SetLimit`).
- Sharing a loop variable in a closure (fixed in Go 1.22 — know your module's `go` directive).
- `time.Sleep` in code to "wait for" a goroutine — use a channel/WaitGroup.
