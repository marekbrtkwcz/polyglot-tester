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

## ORM vs raw SQL

- ORM when the domain model is rich and queries are mostly CRUD by object graph; raw SQL (or a query builder) for reporting, bulk updates, and anything with complex joins/aggregations.
- Hybrid is normal: ORM for the hot path, hand-written parameterized SQL for the heavy queries — keep both behind one data-access layer.
- Never let the ORM generate queries you haven't reviewed on hot paths (`EXPLAIN ANALYZE` the generated SQL).

## ORM patterns & pitfalls

- Patterns: Data Mapper (SQLAlchemy ORM, Drizzle, sqlc — preferred) vs Active Record (Django ORM, Prisma to a degree, GORM) — Data Mapper keeps domain logic out of the persistence layer.
- **N+1**: always eager-load relations that are accessed in a loop (dataloaders in GraphQL, `select_related`/`prefetch_related` in Django, `joinedload`/`preload` in SQLAlchemy/GORM, `Include` in EF).
- Lazy loading in a loop is the classic silent perf bug — make loading explicit.
- Unit of Work / session lifecycle: one session/transaction per request or use case; dispose it in teardown, even on error.
- Migrations must match the ORM models — generate from models, review the diff, never hand-edit generated migrations blindly.

## Per-language drivers/ORMs

- **JS/TS**: `pg` + pool, Prisma, Drizzle, Knex — all support bound parameters.
- **Python**: psycopg3, SQLAlchemy 2.x (`text()` with binds), asyncpg for asyncio.
- **Go**: pgx (preferred) or `database/sql`; sqlc for type-safe generated queries.

## Official sources

- PostgreSQL docs: postgresql.org/docs · EXPLAIN: postgresql.org/docs/current/using-explain.html · SQLAlchemy: docs.sqlalchemy.org · psycopg: psycopg.org · pgx: github.com/jackc/pgx · Prisma: prisma.io/docs · Drizzle: orm.drizzle.team · Alembic: alembic.sqlalchemy.org · golang-migrate: github.com/golang-migrate/migrate
