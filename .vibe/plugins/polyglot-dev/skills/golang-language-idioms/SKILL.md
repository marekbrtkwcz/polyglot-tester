---
name: golang-language-idioms
description: Load this skill when writing idiomatic Go at the language level: guard clauses and control flow, declarations (var vs :=, iota, shadowing), generics, and function style (ordering, signatures, Stringer).
---

# Go Language Idioms

## Control flow

- **Guard clauses**: handle the error/edge case first, then the happy path at zero indentation.

```go
// bad: nested
if err == nil {
    if x > 0 {
        doThing()
    }
}
// good: guard
if err != nil { return err }
if x <= 0 { return nil }
doThing()
```

- No `else` after a `return`/`panic`/`continue` — return early, drop the else.
- `switch true` is fine when conditions are expressions; prefer `switch x { case ... }` when comparing one value.
- `switch` cases don't fall through (no `break` needed); explicit `fallthrough` exists but is rare — avoid.
- Defer for cleanup in the function that acquires the resource.

## Declarations

- `:=` inside functions (short, scoped); `var` at package level, for zero-value init, or when you need a specific type (`var buf bytes.Buffer` vs `buf := new(bytes.Buffer)` — prefer the first).
- Package-level: group with `const ( ... )` / `var ( ... )`; iota for enums:

```go
const (
    StatusPending iota // 0
    StatusActive       // 1 — implicit repeat, don't re-write iota
    StatusDone
)
```

- **Shadowing is legal and dangerous**: `if err := f(); err != nil` inside a scope shadows the outer err — after the if, the outer err is unchanged. Check with `go vet` (shadow check is opt-in) and by reading.
- Don't declare variables you don't use — compiler enforces it, which is a feature.

## Generics (Go 1.18+)

- Use when the same logic is truly type-independent: containers, `lo`-style helpers, `min`/`max`.
- Constraints: `any` (no constraint), `comparable` (== allowed), custom (`interface{ ~int | ~string }` — tilde for underlying types).
- Pitfalls: no type-specific methods on type params; no reflection-free type switch on T; instantiation cost at compile time.
- Don't generic-ify what one concrete type serves — YAGNI applies to types too.
- `any` for "accept anything"; generics when you need to **relate** types (e.g. `func Map[T, R](s []T, f func(T) R) []R`).

## Functions

- Order in a file: exported API first, then unexported helpers; related functions together.
- Signatures: params grouped by type (`a, b int`, not `a int, b int`); return values named only for documentation or multiple same-type returns (`(n int, err error)`).
- Variadic last: `func F(prefix string, items ...string)`.
- `Stringer`: `func (s Status) String() string { ... }` — used by fmt, logging, errors. Keep it total (no panics).
- Methods on value vs pointer receiver: pointer when the method mutates or the struct is large; be **consistent per type** (vet's copylocks catches mixing on mutexes).
