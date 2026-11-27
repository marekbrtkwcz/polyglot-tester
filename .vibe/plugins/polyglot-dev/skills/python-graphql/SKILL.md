---
name: python-graphql
description: Load this skill when building GraphQL APIs in Python: choosing Strawberry, Ariadne or Graphene, schema design, resolvers, DataLoader for N+1, typed errors, depth/complexity limits, and testing. If the language is not Python, prefer golang-graphql or typescript-graphql.
---

# Python GraphQL

## Server library

- **Strawberry** — the standard choice: the schema is defined as Python types and annotations, resolvers are typed, DataLoader is built in, and it plugs into FastAPI, Django or Flask via ASGI/WSGI.
- **Ariadne** — schema-first (SDL strings), a good fit when the schema is an explicit frontend contract.
- **graphene** — older and Django-coupled; prefer Strawberry for new code.

```python
import strawberry


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID) -> User | None:
        return await db.get_user(id)
```

## Schema design

- Design for the client: fields should map to use cases, not DB tables.
- Use the `ID` scalar for identifiers — never expose raw DB ints when they leak row counts.
- Relay-style connections (`edges`/`pageInfo`) with pagination for all lists — never an unbounded list.
- Non-null by default (non-`Optional` return); nullable only when "absent" is meaningful.

## Resolvers & N+1

- N+1 is the default failure mode: 100 users → 100 address queries. Fix it with **DataLoader** (`strawberry.dataloader.DataLoader`) — it batches and caches per request.
- Keep resolvers thin: validate input, call the service layer, map to the output type. No business logic in resolvers.

## Errors

- Follow the spec: partial data plus an `errors` array. In Strawberry, raise from the resolver and map to a code via a custom error presenter (`extensions={"code": "UNAUTHENTICATED"}`).
- Never leak internals (stack traces, SQL) to clients — log the full error, return a generic message plus a code.

## Security & ops

- Enforce a query depth/complexity limit (Strawberry extension or a validation rule) — one deeply nested query is a DoS.
- Disable introspection in production.
- Auth per field, not per resolver: Strawberry permission classes (`IsAuthenticated`, role checks) so a new field cannot forget it.
- Persisted queries for known clients: faster, and an allowlist in production.

## Testing

- Test resolvers as plain async functions against an in-memory test DB (pytest + anyio, or httpx against the ASGI app).
- Assert on the `errors` array shape, and on DataLoader batching by counting the queries issued.

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
- `python-web-and-apis` — HTTP framework choice (FastAPI/Django/Flask), REST endpoints, background tasks.
- `api-design-polyglot` — cross-language API design rules when the API is GraphQL.
