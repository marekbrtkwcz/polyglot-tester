---
name: api-design-polyglot
description: Load this skill when designing, versioning, or hardening HTTP/GraphQL/gRPC APIs in any language — resource modeling, status codes, pagination, error envelopes, and breaking-change policy.
---

# API Design (Polyglot)

## Resource modeling (REST)

- Model nouns (resources), not actions: `POST /orders` not `POST /createOrder`.
- Use HTTP methods with their semantics: GET safe/idempotent, PUT idempotent full replace, PATCH partial, DELETE idempotent.
- Nest one level deep max (`/orders/{id}/items`); use query params for filter/sort/page, not paths.

## Status codes & errors

- 2xx for success (201 + `Location` on create), 4xx for client errors, 5xx for server faults.
- Consistent error envelope: `{ "error": { "code": "VALIDATION_FAILED", "message": "...", "details": [...] } }` — machine-readable `code`, human `message`, never stack traces to clients.
- 400 validation, 401 unauthenticated, 403 unauthorized, 404 (not 403) for hidden resources, 409 conflict, 422 semantic validation, 429 rate limited with `Retry-After`.

## Pagination & filtering

- Cursor-based for large/ordered datasets; offset-based only for small ones. Always cap page size, default it too.
- Sort/filter via query params with an allowlist of sortable/filterable fields.

## Versioning & breaking changes

- Prefer additive changes (new optional fields, new endpoints) — they are non-breaking.
- Version via URL (`/v1/`) or header; deprecate with `Deprecation` + `Sunset` headers and a changelog entry; track client usage before removal.

## GraphQL / gRPC

- GraphQL: schema-first, depth/complexity limits, dataloaders for N+1, typed errors with `extensions.code`.
- gRPC: proto contracts as source of truth, deadline on every call, status codes mapped to equivalents.

## Cross-cutting

- Auth on every endpoint; rate limiting; request/response logging with correlation IDs (see `observability-polyglot`).
- Contract tests against the OpenAPI/proto spec so clients and server can't drift.
