---
name: golang-stay-updated
description: Load this skill when upgrading the Go toolchain or modernizing a codebase: reading release notes, bumping the go directive, and applying new language features safely.
---

# Staying Current with Go

## Upgrading the toolchain

1. Read the [release notes](https://go.dev/doc/devel/release) for the target version — the "Go 1.x" section lists language changes; "Minor changes" lists stdlib additions.
2. Bump `go` directive in `go.mod`, then `go mod tidy`.
3. Update CI (`setup-go` `go-version`) and Docker base image (`golang:1.x`) in the same PR.
4. Run the full gate: `go build ./... && go vet ./... && go test -race -count=1 ./...`.

## Compatibility promise

Since Go 1.0 the language is backwards compatible, and since Go 1.21 the toolchain enforces it: a module with `go 1.22` cannot use newer language features, and older modules keep building. Upgrade is safe — the risk is in *behavior* changes (rare, listed in release notes under "Ports"/"Runtime").

## Modernizing existing code

- Run `gopls modernize ./...` (or `go run golang.org/x/tools/gopls@latest modernize ./...`) — applies current idioms automatically:
  - `interface{}` → `any`
  - `sort.Slice` → `slices.SortFunc`
  - classic for-loops → `for i := range n`
  - `fmt.Sprintf` in hot paths → strconv where applicable
- Review the diff like any PR: modernize is mechanical, not always semantic-preserving in edge cases (e.g. loop variable capture pre-1.22).

## Staying informed

- `go.dev/blog` — release posts and deep dives.
- `go.dev/doc` — spec changes.
- `pkg.go.dev` — check stdlib additions before writing your own helper (`slices`, `maps`, `cmp`, `log/slog`, `unique`, `structs`...).
- Rule: before hand-rolling a helper, check if the current stdlib already has it.
