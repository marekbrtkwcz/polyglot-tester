---
name: databases
description: Database work across stacks: SQL fundamentals, PostgreSQL operations, migrations discipline, transactions, indexing, and per-language drivers and ORMs.
display_name: Databases
icon: database
---

# Databases Reference

## SQL fundamentals

- Parameterized queries only — never string-concatenated SQL.
- Transactions: keep short, no network calls inside, handle deadlocks with retry.
- Indexes on predicate columns; verify with `EXPLAIN ANALYZE`, don't guess.
- Normalize for integrity, denormalize deliberately for read performance.

## PostgreSQL everyday ops

- `psql` basics: `\dt`, `\d table`, `\x` expanded output; `EXPLAIN (ANALYZE, BUFFERS)` for slow queries.
- `pg_dump`/`pg_restore` for backups; test restores, not just backups.
- Connections: pool in the app (pgBouncer for many app instances); `max_connections` is a server budget shared by all clients.

## Migrations discipline

- Expand/contract: deploy additive migration first, code second, removal last — never destructive in the same release.
- Test up AND down; backfills batched and idempotent.
- Tools: Alembic (Python), Prisma Migrate / Drizzle (JS/TS), golang-migrate / atlas (Go).

## Per-language drivers/ORMs

- **JS/TS**: `pg` + pool, Prisma, Drizzle, Knex — all support bound parameters.
- **Python**: psycopg3, SQLAlchemy 2.x (`text()` with binds), asyncpg for asyncio.
- **Go**: pgx (preferred) or `database/sql`; sqlc for type-safe generated queries.

## Official sources

- PostgreSQL docs: postgresql.org/docs · EXPLAIN: postgresql.org/docs/current/using-explain.html · SQLAlchemy: docs.sqlalchemy.org · psycopg: psycopg.org · pgx: github.com/jackc/pgx · Prisma: prisma.io/docs · Drizzle: orm.drizzle.team · Alembic: alembic.sqlalchemy.org · golang-migrate: github.com/golang-migrate/migrate
