# GraphQL in TypeScript

## Server choice

- **graphql-yoga**: modern, fetch-based, great for serverless/edge and Node.
- **Apollo Server**: mature ecosystem, plugins, persisted queries.
- **Pothos**: code-first schema builder with full type safety when your domain is already typed — schema and resolvers can't drift.
- Pick one; don't mix two servers in one process.

## Schema design

- Schema-first (SDL) for contracts shared with other teams; code-first (Pothos) for TS-only stacks.
- Design for the client: name fields after user tasks, not DB columns; keep the schema flat, use connections for lists.
- Nullability discipline: `!` only when the value is truly always present — clients rely on it.

## N+1 with dataloaders

- Every relation resolver that queries per-parent must use a `DataLoader` (batch + cache per request).
- Instantiate dataloaders per request (not module-level) or the cache leaks across requests.

## Errors

- Throw typed errors in resolvers; map them in a format function to `{ message, extensions: { code } }` — never leak stack traces or internal details.
- Partial data: return `data` with `errors` per GraphQL spec; don't fail the whole response for one field.

## Protecting the server

- Depth limit + query complexity limit (e.g. `graphql-validation-complexity` or yoga's built-in) — a deeply nested query is a DoS.
- Disable introspection in production (or gate it); disable playground/graphiql in production.
- Persisted queries / allowlist in production if clients are known.
- Auth: resolve identity in `context` from the verified token (see `auth-polyglot`); enforce field-level auth in resolvers or with a directive.

## Client side

- Codegen (graphql-codegen) from the schema so queries and types never drift; validate queries at build time.
- Normalized cache (Apollo/urql) with sensible `typePolicies`; refetch after mutations that change lists.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
