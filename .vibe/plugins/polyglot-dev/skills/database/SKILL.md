---
name: database
description: Load this skill when working with databases (SQL/ORMs, N+1, Prisma, Drizzle, SQLAlchemy, Alembic, sqlc, pgx) in JavaScript/TypeScript, Python, or Go — choosing a store, writing safe queries, transactions, migrations, and connection pooling. Once the language is known, also read the matching references/ file (go.md, python.md, ts.md) for driver-, ORM-, and tool-specific depth.
---

# Database Work

## Choosing a store

- Relational (PostgreSQL default) for structured data with relations and transactions.
- Document store (MongoDB) for flexible schemas; search (Elasticsearch/OpenSearch) for full-text; cache (Redis) for hot ephemeral data; queue (RabbitMQ/SQS) for async work.
- Don't add a store because it's trendy — justify with a query/consistency need.

## Query safety (all languages)

- **Never concatenate user input into SQL.** Use parameterized queries / prepared statements / ORM bind parameters.
- Validate and constrain inputs at the boundary: types, lengths, allowed values.
- Set statement timeouts; avoid `SELECT *` on hot paths; add indexes for query predicates (verify with EXPLAIN/ANALYZE).

## Transactions

- Keep transactions short; never hold a transaction across a network call.
- Handle deadlocks and serialization failures with retry (with backoff + jitter).
- Test rollback paths, not just commit.

## Migrations

- Expand/contract: add columns/tables before code that needs them; remove after old code stops using them — never destructive in the same release as the code change.
- Every migration must be reversible or explicitly marked irreversible; test up AND down.
- Backfills: batch them, monitor load, make re-runnable (idempotent).

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | database/sql vs sqlx vs sqlc vs ORMs, pooling, transactions, migrations, query safety |
| Python | `references/python.md` | SQLAlchemy 2.x sync/async, psycopg3/asyncpg, Alembic, pooling, async traps, query safety |
| JavaScript/TypeScript | `references/ts.md` | Prisma vs Drizzle vs pg, pool sizing, transactions, migrations, N+1 |

## Pooling & ops

- Size pools conservatively; total app connections must stay under DB `max_connections`.
- Monitor: connection wait time, slow queries, lock waits, replication lag.
- Verify persisted state in tests directly in the DB (see `testing-database-state` concepts), not only via API responses.

## Related

- Knowledge `databases` — concepts plus diagnostics (EXPLAIN reading, health queries, migration verification).
