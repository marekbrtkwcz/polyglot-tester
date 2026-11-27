---
name: golang-samber-libs
description: Load this skill when considering samber's utility libraries in Go: lo (collections), oops (rich errors), do (DI), mo (monads/Optional), hot (hot reload), ro (read-only pipes) — what each is for and when to skip it.
---

# samber's Go Libraries — When Each Earns Its Place

All by the same author, all small and composable. Rule: reach for them when the alternative is a hand-rolled loop you've written three times.

## lo — collection helpers (`github.com/samber/lo`)

The main one. `lo.Map`, `lo.Filter`, `lo.Find`, `lo.GroupBy`, `lo.KeyBy`, `lo.Uniq`, `lo.Chunk`...

```go
names := lo.Map(users, func(u User, _ int) string { return u.Name })
adults := lo.Filter(users, func(u User, _ int) bool { return u.Age >= 18 })
```

- Check stdlib `slices`/`maps` first (1.21+) — they cover sort, contains, clone, delete.
- Generic, zero-dependency, well-tested. Use freely for transforms.

## oops — structured errors (`github.com/samber/oops`)

Adds attributes, stack traces, and error chaining beyond `%w`:

```go
return oops.Errorf("payment failed").
    With("user_id", id).
    With("amount", amount).
    Wrap(err)
```

Use when errors cross a service boundary and you need structured context in logs. Don't use for simple internal wrapping — `%w` is enough.

## do — dependency injection (`github.com/samber/do`)

Service locator / DI container. Prefer explicit constructors; use `do` when the graph is deep and wiring by hand is error-prone. Pairs with `samber/do` scopes for request-scoped services.

## mo — monads / Optional (`github.com/samber/mo`)

`mo.Option[T]` (Some/None), `mo.Result[T, E]`. Useful at boundaries where "absent" is a real state (config, cache) — but Go's `value, ok` idiom and error returns usually suffice. Use when chaining several fallible lookups.

## hot — hot reload (`github.com/samber/hot`)

Reload config/code without restarting a dev process. Dev-tooling only, never production logic.

## ro — read-only pipes (`github.com/samber/ro`)

Reactive-style chaining over values (`ro.Pipe`) — niche; evaluate against plain functions before adopting.

## Verdict

- **Adopt**: `lo` (everyday), `oops` (service boundaries).
- **Situational**: `do` (big graphs), `mo` (optional-heavy code).
- **Niche/dev-only**: `hot`, `ro`.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
