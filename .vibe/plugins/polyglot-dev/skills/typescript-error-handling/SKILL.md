---
name: typescript-error-handling
description: Load this skill for error handling in JS/TS: Error subclasses, cause chaining, sync vs async errors, unhandled rejection handling, and a Result type for expected failures. If the language is not JavaScript/TypeScript, prefer golang-error-handling or python-error-handling.
---

# Error Handling in JS/TS

## Error basics

- Always `throw new Error(...)` (or a subclass) — never throw strings/numbers.
- Use `error.cause` (ES2022) to chain: `throw new Error('save failed', { cause: err })`.
- Custom errors for expected, handleable failures:

```ts
class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

- In TS, set `this.name` and use `instanceof` for discrimination (or a `code` property for cross-realm safety).

## Sync vs async

- `try/catch` catches sync throws and awaited rejections — but NOT fire-and-forget promises. Every detached promise needs `.catch()`.
- Node: `process.on('unhandledRejection')` and `uncaughtException` as a last-resort logger (then exit — state may be corrupt).
- Browser: `window.addEventListener('unhandledrejection', ...)`.

## Expected vs unexpected errors

- Expected failures (validation, not found, conflict) → return a Result or throw a typed domain error the caller handles.
- Unexpected failures (bugs, broken invariants) → let them throw; log with stack and context.

```ts
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };
```

## Logging discipline

- Log once, at the boundary: catch at the top level, log with context (request id, user id), return a generic message to the client.
- Never log secrets (tokens, passwords, PII) — scrub before logging.
- Include `error.stack` in logs; in production responses send only a safe message + correlation id.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
