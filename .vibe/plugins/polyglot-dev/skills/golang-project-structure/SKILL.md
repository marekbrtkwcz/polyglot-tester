---
name: golang-project-structure
description: Load this skill when starting or reorganizing a Go project: standard layout, package naming, code style, modern Go idioms, and documentation conventions.
---

# Go Project Structure & Style

## Layout (standard Go project layout)

```
cmd/myapp/main.go        # one folder per binary
internal/                # private packages — compiler-enforced
pkg/                     # public packages other modules may import
api/                     # OpenAPI/gRPC specs
web/                     # static assets, templates
scripts/                 # build/deploy helpers
go.mod, go.sum, README.md, Makefile
```

- `internal/` is the Go compiler's visibility boundary — put anything not meant for import there.
- Flat when small: a single-package project needs no `cmd/`/`internal/` ceremony.

## Naming

- Packages: short, lowercase, single word (`http`, not `httpstuff`); no underscores.
- Exported = documented: every exported identifier needs a doc comment starting with its name (`// UserStore ...`).
- Receivers: consistent short name per type (`func (s *Server) ...`), never `this`/`self`.
- Initialisms capitalized: `ID`, `URL`, `HTTP`, `JSON` (`userID`, not `userId`).

## Modern Go idioms (check your `go` directive in go.mod)

- Go 1.22+: loop variables are per-iteration (no `it := it` dance); `min`/`max` builtins; `slices`/`maps` packages (`slices.Sort`, `maps.Clone`).
- Go 1.23+: `range` over int (`for i := range 10`), `slog` for structured logging, `omitzero` in tags.
- `any` instead of `interface{}` since 1.18.

## Style gate

- `gofmt -l .` must output nothing (CI gate); `go vet ./...` clean.
- Prefer `golangci-lint run` with a pinned config (`.golangci.yml` committed).
- Run `modernize ./...` (gopls modernize) to auto-apply new idioms.

## Documentation

- Package comment on one file per package (`doc.go`): what it is, not how.
- README: what it does, quickstart (`go run ./cmd/myapp`), config, links to API docs.
- Examples in `example_test.go` — they run as tests and appear in godoc.

## Dependencies

- `go mod tidy` after changes; commit `go.mod` + `go.sum`; CI uses `go mod download` / `go build -mod=readonly`.
- Prefer stdlib; add a dependency only with a recorded reason. Audit with `govulncheck ./...`.
