---
name: golang-context
description: Load this skill when working with context in Go: cancellation, deadlines, values, and the rules that keep request-scoped data flowing correctly.
---

# Go Context

## The four rules

1. `ctx` is always the **first parameter**: `func Do(ctx context.Context, ...) `.
2. Never store ctx in a struct field of a long-lived object — pass it per call. (Request-scoped services may hold it; data structs never.)
3. Never pass `nil` ctx — use `context.Background()` or `TODO()` at the top level.
4. Cancellation must be **propagated**: check `ctx.Err()` in loops and pass ctx to every blocking call.

## Creating contexts

- `context.Background()` — top of main, tests, init.
- `context.TODO()` — when unsure which ctx fits (placeholder, find it later with grep).
- `context.WithCancel` — explicit stop signal (cleanup, shutdown).
- `context.WithDeadline` / `WithTimeout` — every external call gets a timeout: `ctx, cancel := context.WithTimeout(ctx, 5*time.Second); defer cancel()`.

## Values: use sparingly

- `ctx.Value(key)` for **request-scoped** data only (request ID, auth principal) — never for optional parameters (use real params).
- Always use a **custom key type** to avoid collisions: `type ctxKey string; const requestIDKey ctxKey = "requestID"`.
- Retrieval: `v, ok := ctx.Value(key).(string)` — type-assert with ok, never blind-assert.

## Patterns

```go
select {
case result := <-ch:
    return result, nil
case <-ctx.Done():
    return nil, ctx.Err() // context.Canceled or context.DeadlineExceeded
}
```

- HTTP: `r.Context()` carries the request's ctx — derive from it, don't replace it.
- Shutdown: `signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)` (Go 1.16+) — clean server shutdown.

## Anti-patterns

- Storing ctx in a struct that outlives the request (leaks, stale cancellation).
- Using values for config/dependencies — that's what constructor params are for.
- Ignoring `ctx.Err()` after a blocking call returns an error — check which one fired.
