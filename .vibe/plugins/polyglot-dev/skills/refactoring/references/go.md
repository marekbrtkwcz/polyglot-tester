# Go Refactoring

## The discipline

1. **Green tests first.** No refactor without a suite that passes. If coverage is missing on the target, add characterization tests (pin current behavior) before touching anything.
2. **Small steps, compiling always.** Each step must build and pass tests — git commit between steps when the refactor is large.
3. **Rename with the tool, not by hand.** `gopls rename` (or your IDE) updates all references; `git grep` afterwards to confirm nothing was missed.

## Common refactors

- **Extract function**: when a block has a name-able purpose; pass only the variables it needs, return what callers need.
- **Extract type**: when the same 3+ fields travel together — replace field groups with a struct.
- **Introduce interface**: at the boundary you want to mock/test — define it where it's consumed.
- **Split package**: when a package has two reasons to change; move by feature, not by layer (`internal/user` not `internal/models` + `internal/handlers`).
- **Replace if-else chains with map/polymorphism**: `map[string]Handler` dispatch beats 6 `if`s.

## Mechanical safety

- `gofmt -l .`, `go vet ./...`, `golangci-lint run` after each step.
- `go build ./...` must stay green — never commit a broken intermediate state.
- Delete dead code completely — no commented-out blocks, no unused params kept "just in case" (use `_` only at interface boundaries).

## When NOT to refactor

- Right before a release unless it's a bug fix.
- Without tests on the code being moved.
- "While I'm here" scope creep — separate PR for unrelated cleanups.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
