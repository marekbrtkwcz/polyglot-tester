---
name: golang-design-and-data
description: Load this skill when designing Go types and choosing patterns or data structures: structs vs interfaces, composition, common patterns, and picking the right collection.
---

# Go Design: Types, Patterns, Data Structures

## Structs vs interfaces

- **Struct for data, interface for behavior.** Define interfaces at the consumer, not the producer — accept interfaces, return structs.
- Small interfaces (1–3 methods) compose better than big ones: `io.Reader`, `http.Handler`.
- Embedding: embed for **promotion** (a `Logger` inside a `Server`), not for inheritance — beware method/field name collisions.
- Use `struct{}` (empty struct) as a set value or signal — it allocates nothing.

## Composition over inheritance

```go
type Server struct {
    db     *sql.DB
    logger *slog.Logger
    cfg    Config
}
```

Flat structs with explicit fields beat deep embedding hierarchies. If a struct has more than ~8 fields, it wants splitting.

## Patterns worth knowing

| Pattern | When | Sketch |
| --- | --- | --- |
| Functional options | Config with many optional fields | `func NewServer(opts ...Option)` with `type Option func(*Server)` |
| Repository | Isolate storage from domain | interface in domain, impl in `internal/store` |
| Middleware/chain | HTTP/gRPC cross-cutting | `func(next Handler) Handler` |
| Worker pool | Bounded parallelism | errgroup with `SetLimit` |
| Retry with backoff | Flaky external calls | `github.com/cenkalti/backoff` or hand-rolled with `time.Sleep` + jitter |
| Circuit breaker | Protect against cascading failures | `github.com/sony/gobreaker` |

## Data structures — pick by operation

- **map**: O(1) lookup by key; iterate in random order — sort keys if order matters.
- **slice**: ordered, fast append; preallocate with `make([]T, 0, n)` when n is known.
- **ring/list** (`container/ring`, `container/list`): fixed-size ring buffer, undo stacks.
- **heap** (`container/heap`): priority queues, scheduling.
- **set**: `map[T]struct{}` — no native set; that's the idiom.
- Prefer stdlib collections; reach for `golang.org/x/exp` (or stdlib `slices`/`maps` since 1.21) before third-party.

## Anti-patterns

- Interface with 10+ methods (consumer-defined interfaces stay small).
- Premature abstraction: three structs sharing a pattern > one generic base type.
- `interface{}` parameters where a concrete type or small interface works.
