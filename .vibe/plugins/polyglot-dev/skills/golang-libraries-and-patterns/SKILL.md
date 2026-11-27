---
name: golang-libraries-and-patterns
description: Load this skill when choosing libraries or patterns in Go: CLI, config, HTTP/gRPC, logging, DI, functional helpers, and observability — with when-to-use guidance.
---

# Go Libraries & Patterns

Choose by fit, not popularity. Default to stdlib; add a library when it saves real complexity.

## CLI apps

- **spf13/cobra** for multi-command CLIs (`myapp serve`, `myapp migrate`) with flags and help generation; stdlib `flag` for single-command tools.
- **spf13/viper** for layered config (flags > env > file > defaults) — or stdlib + `os.Getenv` when config is trivial.

## APIs

- REST: stdlib `net/http` (Go 1.22+ has method+path routing: `mux.HandleFunc("GET /users/{id}", h)`) for simple services; **gin/echo/chi** when you want middleware ecosystems.
- gRPC: `google.golang.org/grpc` + protobuf; generate with `protoc` (buf recommended); interceptors for auth/logging.
- OpenAPI: generate server stubs (oapi-codegen) or validate requests against the spec in CI.

## Logging & observability

- **log/slog** (stdlib, 1.21+): structured logging, levels, handlers — the default choice.
- Metrics/tracing: **OpenTelemetry** (`go.opentelemetry.io/otel`) — one standard for metrics, traces, logs.

## Dependency injection

- Small apps: explicit constructor functions (`NewServer(db, cfg)`) — idiomatic Go, no framework.
- Large apps: **google/wire** (compile-time, generated code) or **uber/fx** (runtime, app lifecycle). Don't hand-roll a container.

## Functional helpers

- **samber/lo**: `lo.Map`, `lo.Filter`, `lo.GroupBy`, `lo.KeyBy` — use for collection transforms; don't re-implement.
- stdlib first: `slices`/`maps` cover many cases since 1.21.

## Error & result handling

- Keep `error` returns idiomatic; libraries like **samber/oops** add stack traces/attributes when you need richer errors — optional, not a replacement for `%w`.

## Data access

- **database/sql** + driver for simple cases; **sqlx** for struct scanning convenience; **gorm/ent/sqlc** for larger apps — sqlc (generate Go from SQL) is the safest for complex queries.

## Testing companions

- **stretchr/testify** (require/assert/mock), **go.uber.org/goleak**, **httptest** (stdlib), **testcontainers-go** for real DB/queue in integration tests.

## Rule

Every added dependency: recorded reason in the PR, license check, `govulncheck` clean, and a plan for updates (`go list -m -u all` in CI).

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
