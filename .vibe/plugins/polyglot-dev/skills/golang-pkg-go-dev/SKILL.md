---
name: golang-pkg-go-dev
description: Load this skill when exploring the Go ecosystem: where to find quality packages, how to evaluate them on pkg.go.dev, and curated categories of reliable libraries.
---

# Exploring pkg.go.dev & the Go Ecosystem

## Evaluating a package (pkg.go.dev)

Before importing, check on [pkg.go.dev](https://pkg.go.dev):

1. **Stability**: v1.x = stable API promise; v0.x = may break.
2. **Maintenance**: last commit date, open issues vs PRs, release cadence.
3. **Adoption**: importers list (who depends on it), GitHub stars as a weak signal.
4. **Dependencies**: `go mod why` / `go mod graph` after adding — a small dep tree is a feature.
5. **License**: visible on the repo; MIT/Apache/BSD are safe defaults.
6. **Security**: run `govulncheck ./...` after adding.

## Curated categories

- **Web**: `net/http` (1.22+ routing), gin, echo, chi, fiber (fasthttp-based).
- **CLI**: cobra, viper, urfave/cli.
- **Config**: viper, envconfig, koanf.
- **DB**: sqlc, sqlx, gorm, ent, pgx (Postgres driver + toolkit).
- **gRPC/RPC**: grpc-go, connectrpc (simpler HTTP-based), twirp.
- **GraphQL**: gqlgen.
- **Logging**: slog (stdlib), zap, zerolog.
- **Metrics/tracing**: OpenTelemetry.
- **Testing**: testify, goleak, testcontainers-go, gotestsum.
- **Concurrency**: errgroup (x/sync), goleak.
- **Validation**: go-playground/validator.
- **Utils**: samber/lo (see golang-samber-libs), google/uuid, fx.

## Rules

- Stdlib first — it covers more than expected (`slices`, `maps`, `cmp`, `log/slog`, `net/http` routing).
- One new dependency per PR, with the reason written down.
- Prefer packages that accept interfaces (`io.Reader`) — they compose with stdlib.
- Check [awesome-go](https://awesome-go.com) for vetted lists by category.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
