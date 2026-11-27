---
name: architecture
description: Architecture patterns across JavaScript/TypeScript, Python, and Go: layered vs hexagonal (ports/adapters) vs clean architecture, dependency direction, where code lives per language, and anti-patterns to avoid.

display_name: Architecture
icon: blueprint
---

# Architecture Reference (Polyglot)

## The one rule that matters

**Dependencies point inward.** The domain/core knows nothing about frameworks,
databases, or HTTP. Outer layers (adapters: DB, HTTP, CLI, queues) depend on
inner layers, never the reverse. In practice: define interfaces/ports at the
boundary where you mock or swap, and implement them in the adapter.

## Choosing a shape

- **Layered (3-tier)**: controllers/handlers → services → repositories. Simple,
  familiar, fine for most CRUD apps. Risk: services become god-objects.
- **Hexagonal / ports & adapters**: domain in the center, ports (interfaces)
  around it, adapters plugged in. Best when you swap implementations (DB,
  message bus, external API) or test the domain without infrastructure.
- **Clean architecture**: same idea, stricter use-case layer between
  entities and interfaces. Best for large, long-lived domains.
- **Vertical slices / feature modules**: code grouped by feature
  (`user/`, `order/`) instead of by technical layer. Often the pragmatic
  middle ground in all three languages.

Rule of thumb: start layered, extract ports when a second implementation
appears, split by feature when a layer gets crowded.

## Where code lives per language

- **Go**: flat-ish stdlib layout — `cmd/<app>/main.go` (wiring), `internal/<feature>/`
  (unexported by design), `pkg/` only for genuinely shared code. Interfaces
  defined where consumed, not where implemented.
- **Python**: `src/<package>/` layout; modules by feature (`app/users/`),
  `app/ports.py` (Protocols) + `app/adapters/` when hexagonal; avoid circular
  imports by keeping `__init__.py` re-exports minimal.
- **JS/TS**: `src/features/<feature>/` or `src/<feature>/` with colocated
  tests; barrel `index.ts` per feature, not one giant root barrel; dependency
  injection by constructor parameter (or a lightweight container like
  tsyringe only when wiring gets big).

## Cross-cutting concerns

- Config/env parsing at the edge (startup), injected inward as typed objects —
  never read `os.environ`/`process.env` deep in the domain.
- Logging/metrics via the port interface too, so tests stay silent.
- Errors: domain errors are typed (sentinel/exception subclass/Error subclass);
  adapters translate them to HTTP/gRPC codes at the boundary.

## Anti-patterns

- Anemic domain: entities with only getters/setters, all logic in services.
- Framework types leaking into the domain (ORM models, Express `Request`,
  Django models used as domain objects) — map at the adapter boundary.
- `utils`/`common` catch-all packages — they become the new god-object.
- Circular imports between features — a sign the boundary is in the wrong place.
- Big-ball-of-mud growth: no new module without asking "which feature owns this?"

## Related

Skills `typescript-project-structure`, `python-project-structure`,
`golang-project-structure` cover concrete layouts; `refactoring-polyglot`
for safe restructuring toward these shapes.
