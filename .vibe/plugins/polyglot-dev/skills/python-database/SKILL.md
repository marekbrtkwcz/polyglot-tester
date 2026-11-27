---
name: python-database
description: Load this skill when working with databases from Python: SQLAlchemy 2.x (sync and async), psycopg3/asyncpg, Alembic migrations, pooling, transactions, and query safety. If the language is not Python, prefer golang-database or typescript-database.
---

# Databases in Python

## Driver & stack choice

- **psycopg3** (sync) / **asyncpg** via SQLAlchemy async, or asyncpg directly for raw async SQL. Avoid psycopg2 for new projects.
- **SQLAlchemy 2.x**: Core (`text()` with bound params) for SQL-heavy code, ORM for domain-heavy code. One style per project.
- Lightweight: `databases`/`aiosql` if you want minimal abstraction without an ORM.

## Async discipline (the classic trap)

- Never mix sync engine in async code — it blocks the event loop. Use `create_async_engine` + `async_sessionmaker`.
- Lazy loading in async ORM raises `MissingGreenlet` — always `selectinload`/`joinedload` relations you will access (the async N+1 guard).

## Pooling

- `pool_size` + `max_overflow` on the engine; keep app total below DB `max_connections`.
- `pool_pre_ping=True` to drop dead connections; `pool_recycle` below the DB idle timeout.

## Transactions & sessions

- One session per request/unit of work: `async with Session() as s, s.begin(): ...` — commit on success, rollback on exception.
- `sessionmaker(expire_on_commit=False)` to avoid lazy re-loads after commit.

## Migrations (Alembic)

- `alembic revision --autogenerate -m ...` then **read the diff** — autogenerate misses renames and some constraints.
- Test `upgrade()` and `downgrade()` in CI against a scratch database.
- Expand/contract: additive migrations ship with the code that needs them; destructive ones only after old code is gone.

## Query safety

- Bound parameters everywhere (`text("... :param")` with dict, or driver placeholders `%s`); never f-strings into SQL.
- Set `statement_timeout` for user-facing queries; cap result sizes (`LIMIT`).
- Verify index usage with `EXPLAIN (ANALYZE, BUFFERS)` on slow queries.

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
