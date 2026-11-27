# Architecture Diagnostics Reference

Companion to the architecture knowledge: the checks that tell you whether
the dependency rule actually holds in this repo today — not in the diagram.

## Detecting boundary violations

- Framework types in the domain:
  `rg "from '(express|@nestjs|fastapi|django|@prisma/client)'" src/domain/`
  (Python: `rg "import (django|fastapi|sqlalchemy)" src/domain/`).
- ORM models used as domain objects: search the domain for imports of
  `models`, `entities`, or ORM base classes — mapping belongs in the adapter.
- Circular feature imports (JS/TS): `madge --circular --extensions ts src/`.
- Layer direction rules (JS/TS): dependency-cruiser with a `forbidden` rule
  such as "domain must not import adapters" — wire it into CI.
- Layer contracts (Python): import-linter `layers` contract
  (`lint-imports`), e.g. `domain` above `adapters`, never the reverse.
- Go: import cycles are compile errors — the compiler enforces the rule for
  free. What to watch instead: interfaces defined where *implemented*
  instead of where *consumed*, and `internal/` code importing heavyweight
  outer packages (`go list -deps ./internal/...`).

## Quick verdict table

| Question | Healthy sign | Red flag |
| --- | --- | --- |
| Can I test the domain without infrastructure? | domain tests import no drivers, no docker | every test needs `docker compose up` |
| Where is config read? | once, at startup, injected inward as typed values | `process.env` / `os.environ` deep in services |
| Does one change touch one place? | a feature owns its whole slice | `utils`/`common` imported everywhere |
| Can I swap the DB in a week? | repository is an interface at the boundary | handlers query the ORM directly |

## When someone proposes a new shared package

- Which feature owns it? No owner → it belongs inside the consuming feature.
- Only two importers today? Inline it; extract on the third use.
- Named after a technical kind (`utils`, `common`, `helpers`)? It is the
  next god-object — name it after what it does, or reject it.
