# Databases Diagnostics Reference

Companion to the databases knowledge: reading EXPLAIN, the psql health
queries, migration verification per tool, and catching ORM surprises.

## Reading EXPLAIN (ANALYZE, BUFFERS)

| Symptom in the plan | Usual cause | First move |
| --- | --- | --- |
| `Seq Scan` on a big table, filter discards most rows | missing index on the predicate | create the index, re-EXPLAIN |
| Row estimate wildly off the actual | stale statistics | `ANALYZE` the table |
| `Nested Loop` with many outer rows | no index on the inner join key | index the join column |
| Huge `Buffers: shared read=` | working set spills to disk | cut the rows or fix the query shape |
| Index present but never used | low selectivity or type mismatch | check `idx_scan` in `pg_stat_user_indexes` |

## Health queries

- Unused indexes (write overhead for nothing):
  `SELECT relname, indexrelname, idx_scan FROM pg_stat_user_indexes;`
- Top queries by time: `pg_stat_statements`
  `ORDER BY total_exec_time DESC LIMIT 10;`
- Who is blocking whom: `SELECT pid, pg_blocking_pids(pid), query FROM pg_stat_activity;`

## Migration verification per tool

- Alembic: `alembic upgrade head`, then `alembic downgrade -1`, then up
  again — the down path must work, not just the up path.
- Prisma: `prisma migrate dev` locally, `prisma migrate deploy` in CI/prod;
  never edit an already-applied migration.
- golang-migrate: `migrate -path migrations -database "$URL" up`, then
  `... down 1` to prove the rollback.
- After any migration, re-`EXPLAIN` the app's top queries — a new column
  can change a plan.

## Catching N+1 and ORM surprises

- Turn SQL echo on for one request: SQLAlchemy `create_engine(..., echo=True)`,
  Django `DEBUG=True` in a shell, Prisma log level `query`, GORM `db.Debug()`.
- Near-identical SELECTs repeated in one endpoint = N+1 → eager-load
  (`joinedload`, `select_related`/`prefetch_related`, `Preload`, `Include`)
  or batch with a loader.
- Review the generated SQL of hot ORM queries with `EXPLAIN ANALYZE` —
  never assume the ORM wrote the query you meant.
