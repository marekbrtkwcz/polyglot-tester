---
name: typescript-database
description: Load this skill when working with databases from Node.js/TypeScript: Prisma vs Drizzle vs pg, connection pooling, transactions, migrations, and query safety.
---

# Databases in TypeScript/Node

## Choosing a library

- **Prisma**: full ORM with migrations and a generated type-safe client — fastest to a working schema; heavier runtime.
- **Drizzle**: SQL-like query builder with full type inference, no codegen daemon; good when you want SQL control + types.
- **pg (node-postgres)**: raw driver with a connection pool — for stored procedures, bulk ops, or when an ORM gets in the way.
- Rule: one data-access layer; app code never writes raw SQL outside it.

## Connection pooling

- Always pool: `new Pool({ max: 10 })` in pg; Prisma manages its own pool (set `connection_limit`).
- Total connections across all app instances must stay under Postgres `max_connections` (leave headroom; consider pgBouncer in transaction mode for many instances).
- Monitor pool wait time; a growing `waiting` count means the pool is too small or queries too slow.

## Query safety

- Parameterized queries only (`$1, $2` in pg; Prisma/Drizzle bind automatically). Never template user input into SQL strings.
- Validate input at the boundary with a schema (zod/valibot) before it reaches the data layer.

## Transactions

- pg: `const client = await pool.connect(); try { await client.query('BEGIN'); ... await client.query('COMMIT'); } catch { await client.query('ROLLBACK'); } finally { client.release(); }` — or a helper that does exactly this.
- Prisma: `prisma.$transaction([...])` (array, limited) or the callback form with `timeout` and `maxWait`.
- Keep transactions short; no awaits on external HTTP calls inside a transaction.

## Migrations

- Prisma Migrate / Drizzle Kit: review the generated SQL before applying; test up and down in CI on a scratch DB.
- Expand/contract: additive migration + code deploy first, cleanup migration in a later release.
- Backfills: batched, resumable, monitored; never a single giant UPDATE on a hot table.

## N+1 and reads

- Use `include`/`select` relations explicitly (Prisma) or explicit joins (Drizzle); dataloader-style batching for GraphQL resolvers.
- Add indexes for query predicates; verify with `EXPLAIN ANALYZE`, don't guess.
- Read replicas for heavy reporting queries, with lag awareness (don't read-your-write across replicas).
