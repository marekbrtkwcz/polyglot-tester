---
name: web-and-apis
description: Load this skill when building HTTP services, APIs, or browser-side apps in Go, Python, or JavaScript/TypeScript — framework/server choice, routing, middleware, request validation, graceful shutdown, and DOM/fetch patterns for the browser. Once the language is known, also read the matching references/ file (go.md, python.md, ts.md) for that stack's depth.
---

# Web & APIs

- Pick the framework the repo already has; consistency beats novelty.
- Middleware order matters: logging/correlation ID first, then auth, then validation, then the handler.
- Validate at the boundary, map domain errors to safe responses (see error-handling), shut down gracefully.
- Browser side (ts.md): DOM APIs, fetch with AbortController, storage, events, a11y basics.

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | net/http vs gin/echo/fiber, routing, middleware, request validation, graceful shutdown, JSON |
| Python | `references/python.md` | FastAPI/Django/Flask choice, async SQLAlchemy, Alembic, GraphQL with Strawberry, background tasks |
| JavaScript/TypeScript | `references/ts.md` | browser DOM APIs, fetch + AbortController, storage, events, framework-agnostic patterns, a11y basics |
