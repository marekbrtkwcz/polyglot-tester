# Go GraphQL

## Server library

- **99designs/gqlgen** — schema-first: write `.graphql`, generate type-safe resolvers. The standard choice.
- graphql-go/graphql — code-first, simpler but weaker typing.

Generate with `go run github.com/99designs/gqlgen generate` after schema changes; commit generated code or generate in CI.

## Schema design

- Design for the client: fields should map to use cases, not DB tables.
- Use `ID` scalar for identifiers, never expose raw DB ints when they leak counts.
- Connections + pagination (Relay-style `edges`/`pageInfo`) for all lists — never unbounded `[]`.
- Non-null (`!`) by default; nullable only when "absent" is meaningful.

## Resolvers & N+1

- The N+1 problem is the default failure: 100 users → 100 address queries. Fix with **dataloader** (gqlgen has `dataloader` package) — batch and cache per-request.
- Keep resolvers thin: validate input, call service layer, map to model. No business logic in resolvers.

## Errors

- Return partial data + `errors` array per GraphQL spec; gqlgen: return error from resolver, use extensions for codes (`UNAUTHENTICATED`, `BAD_USER_INPUT`).
- Never leak internal errors (stack, SQL) to clients — log full, return generic message + code.

## Security & ops

- Query depth/complexity limit (gqlgen extension or `graphql-go/handler` middleware) — otherwise one query kills the server.
- Disable introspection in production.
- Auth in a directive (`@auth(role: ADMIN)`) so it's enforced per field, not forgotten in resolvers.
- Persisted queries for known clients (faster, allowlist-only in prod).

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
