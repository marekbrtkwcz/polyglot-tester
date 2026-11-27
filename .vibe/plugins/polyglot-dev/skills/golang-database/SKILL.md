---
name: golang-database
description: Load this skill when working with databases in Go: choosing between database/sql, sqlx, sqlc, and ORMs, plus connection pooling, migrations, and query safety. If the language is not Go, prefer python-database or typescript-database.
---

# Go Database Access

## Choose the layer

| Layer | When |
| --- | --- |
| `database/sql` + driver | Simple queries, full control, zero magic |
| **sqlc** | Complex SQL — write SQL, get type-safe generated Go. Best default for serious apps |
| sqlx | `database/sql` with struct scanning (`StructScan`) convenience |
| GORM / ent | Rapid prototyping, heavy model layer — accept the abstraction cost |

Rule: SQL lives in `.sql` files (sqlc) or constants — never string-built from input.

## Connection pooling (database/sql)

```go
db.SetMaxOpenConns(25)        // match DB capacity, not "unlimited"
db.SetMaxIdleConns(5)
db.SetConnMaxLifetime(5 * time.Minute) // recycle; avoids stale conns behind LB
db.SetConnMaxIdleTime(time.Minute)
```

- One `*sql.DB` per database for the process lifetime — it IS the pool.
- Always `defer rows.Close()`; check `rows.Err()` after iteration.
- Use `db.QueryRowContext(ctx, ...)` — context-aware everywhere.

## Transactions

```go
tx, err := db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelReadCommitted})
if err != nil { return err }
defer tx.Rollback() // no-op after Commit
// ... tx.QueryContext ...
if err := tx.Commit(); err != nil { return err }
```

- Keep transactions short; don't do HTTP calls or sleeps inside one.
- `defer tx.Rollback()` is the safety net — Commit makes it a no-op.

## Migrations

- **golang-migrate** or **Atlas** — versioned migration files, applied in CI or at startup, never hand-run in prod.
- Expand/contract: add nullable column first, deploy code, backfill, then add constraints — never destructive migration with the code that needs the new schema.

## Safety checklist

- [ ] Parameterized queries only (`$1`/`?` placeholders), never Sprintf.
- [ ] Indexes on queried columns — verify with `EXPLAIN ANALYZE`.
- [ ] Credentials from env/secret manager, never in code; TLS to the DB.
- [ ] Connection limits set; slow query log enabled.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
