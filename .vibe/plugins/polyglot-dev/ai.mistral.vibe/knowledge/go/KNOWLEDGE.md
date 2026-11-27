---
name: go
description: Toolchain and conventions for Go projects: go.mod, table-driven tests, error wrapping, golangci-lint, and everyday commands.
display_name: Go
icon: code
---

# Go Reference

## Toolchain

- One toolchain per module: `go mod init`, `go get`, `go mod tidy`.
- Format: `gofmt` (or `go fmt ./...`); vet: `go vet ./...`.
- Lint: **golangci-lint** (`golangci-lint run`) as the CI gate.
- Test/build cache: use `-count=1` to bypass the test cache in CI.

## Conventions

- Errors are values: check every one, wrap with context
  (`fmt.Errorf("reading config: %w", err)`).
- Interfaces belong to the consumer; keep them small (1–2 methods).
- Accept interfaces, return structs.
- `context.Context` as the first parameter on anything that does I/O.
- Exported identifiers get doc comments starting with the name.

## Everyday commands

| Task | Command |
|---|---|
| build | `go build ./...` |
| test | `go test ./...` |
| test (CI) | `go test -race -count=1 ./...` |
| vet | `go vet ./...` |
| lint | `golangci-lint run` |
| tidy | `go mod tidy` |

## Gotchas

- Loop variable capture in closures — fine since Go 1.22, a bug before it;
  check the module's `go` directive.
- `nil` map write panics; initialize with `make`.
- `append` to a slice shared by another slice mutates the shared backing
  array.
- Every goroutine needs a defined lifecycle; a leaked goroutine is a bug,
  not a style issue.
- `time.After` in a loop leaks timers until they fire; use `NewTimer` +
  `Reset`.

## Official sources

- https://go.dev — downloads, tour, blog, release notes.
- https://go.dev/doc/effective_go — Effective Go (read before writing idiomatic Go).
- https://go.dev/ref/spec — the language specification.
- https://pkg.go.dev — standard library + package docs (evaluate third-party packages here).
- https://go.dev/doc/devel/release — per-version release notes; read before upgrading the toolchain.
- https://github.com/golang/go/wiki/CodeReviewComments — code review guidelines.
