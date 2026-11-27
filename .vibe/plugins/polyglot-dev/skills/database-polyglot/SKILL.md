---
name: database-polyglot
description: Load this skill when working with databases in JavaScript/TypeScript, Python, or Go — choosing a store, writing safe queries, transactions, migrations, and connection pooling across languages.
---

# Database Work (Polyglot)

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

## Per-language quick reference

- **JS/TS**: Prisma or Drizzle (SQL-safe, typed); pg with a pool (`max` sized to ~DB connections / app instances); transactions via `$transaction` / callback API.
- **Python**: SQLAlchemy Core/ORM with `text()` bound params, psycopg3; Alembic for migrations; pool via `pool_size`/`max_overflow`.
- **Go**: sqlc (type-safe SQL) or pgx stdlib; `database/sql` pool via `SetMaxOpenConns`; transactions with `pgx.Tx` or `sql.Tx` + `defer rollback`.

## Pooling & ops

- Size pools conservatively; total app connections must stay under DB `max_connections`.
- Monitor: connection wait time, slow queries, lock waits, replication lag.
- Verify persisted state in tests directly in the DB (see `testing-database-state` concepts), not only via API responses.
