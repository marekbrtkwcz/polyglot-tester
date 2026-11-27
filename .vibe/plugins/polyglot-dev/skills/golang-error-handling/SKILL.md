---
name: golang-error-handling
description: Load this skill when writing or reviewing error handling in Go: wrapping with context, sentinel errors, errors.Is/As, and API error design. If the language is not Go, prefer python-error-handling or typescript-error-handling.
---

# Go Error Handling

## The core rules

- **Check every error.** Ignoring one (`_ = err`) is a bug, not a style choice.
- **Wrap with context, not replacement**: `fmt.Errorf("reading config: %w", err)` — the `%w` verb keeps the chain inspectable.
- **Wrap at the layer that knows the "what"**, not the "where": the low layer says *what failed*, the caller adds *what it was doing*.

## Sentinel errors vs typed errors

- Sentinel (`var ErrNotFound = errors.New("not found")`) for **expected, programmatic** cases the caller may branch on.
- Typed errors (custom struct implementing `Error()`) when the caller needs **payload** (e.g. which field, which ID).
- Match with `errors.Is(err, ErrNotFound)` / `errors.As(err, &target)` — never `err == ErrNotFound` after wrapping, never string matching.

```go
func GetUser(id string) (*User, error) {
    u, err := db.Find(id)
    if errors.Is(err, sql.ErrNoRows) {
        return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
    }
    if err != nil {
        return nil, fmt.Errorf("looking up user %s: %w", id, err)
    }
    return u, nil
}
```

## Designing an API's errors

- Return `nil` error only on success; return zero value + non-nil error otherwise.
- One sentinel per distinguishable condition; document them on the function.
- Don't leak internals: wrap internal errors, but return a stable sentinel for the public contract.
- `panic` only for truly unrecoverable programmer errors (nil map on init) — never for request/IO failures.

## Anti-patterns

- `if err != nil { return err }` everywhere without adding context — the trace becomes useless.
- Logging AND returning the error (double handling) — return it, let the top layer log once.
- `errors.New(fmt.Sprintf(...))` — use `fmt.Errorf` without `%w` when no wrap is needed.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
