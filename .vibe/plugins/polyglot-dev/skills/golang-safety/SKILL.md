---
name: golang-safety
description: Load this skill when hardening Go code against panics, races, nil dereferences, and integer issues: defensive patterns that keep a service alive.
---

# Go Safety (Runtime Robustness)

## Panics

- A panic in an HTTP handler kills the connection; in a goroutine it **crashes the whole process**. Recover at the top of every goroutine and every server handler:

```go
func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                log.Printf("panic: %v\n%s", rec, debug.Stack())
                http.Error(w, "internal error", 500)
            }
        }()
        handle(w, r)
    })
}
```

- Prefer returning errors over panicking in libraries; panic only for unrecoverable invariant violations.

## Nil safety

- Nil map **read** is fine, nil map **write** panics → always `make()` before writing.
- Nil pointer method calls panic → check receivers: `if s == nil { return ErrNil }` on exported methods of pointer types.
- Nil slice is fine (len 0, append works); nil interface ≠ typed nil — `var w io.Writer = (*bytes.Buffer)(nil)` is NOT nil; check with reflection only if you must, better: avoid returning typed nils.

## Data races

- `go test -race ./...` and `go build -race` — run in CI, always.
- A race is any unsynchronized access where at least one is a write. `go vet` catches some copylocks cases.
- Rule: one goroutine owns a variable; communicate via channels, or guard with `sync.Mutex`/`atomic`.
- `atomic.Int64` etc. (1.19+) for counters; `atomic.Pointer[T]` for lock-free swaps.

## Integer & overflow

- Conversions truncate silently: `int32(bigInt)` wraps. Check ranges before converting (`math.MaxInt32`).
- `len()` returns int — on 32-bit platforms huge slices overflow; fine on 64-bit, but don't assume.
- Division by zero panics for ints — validate denominators from input.

## Input limits

- Cap everything from outside: body size (`http.MaxBytesReader`), slice lengths, string lengths, recursion depth in parsers.
- Validate at the boundary; internal code can then trust the data.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
