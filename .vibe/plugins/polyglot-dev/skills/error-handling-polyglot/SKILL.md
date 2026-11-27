---
name: error-handling-polyglot
description: Load this skill when designing error handling in JavaScript/TypeScript, Python, or Go — error chaining, domain error types, expected vs unexpected failures, and logging discipline across languages.
---

# Error Handling (Polyglot)

## The core rules — same in every language

- Handle or propagate every error; ignoring one is a bug, not a style choice.
- **Chain, don't replace**: preserve the original cause so the trace stays inspectable.
- Add context at the layer that knows *what it was doing* ("reading config", "saving user 42"), not just *where*.
- Expected, programmatic failures (not found, validation, conflict) get a **typed domain error** the caller can branch on; unexpected failures (bugs, broken invariants) propagate/throw.
- **Log once, at the boundary** that handles the error — never log and re-raise (double logs). Never log secrets/PII.
- Never use errors for ordinary control flow in hot loops — raise/catch/throw is not free.

## Chaining per language

- **Go**: `fmt.Errorf("looking up user %s: %w", id, err)` — `%w` keeps the chain. Match with `errors.Is(err, ErrNotFound)` / `errors.As`, never `==` after wrapping, never string matching. Sentinels (`var ErrNotFound = errors.New(...)`) for expected cases; `panic` only for unrecoverable programmer errors.
- **Python**: `raise ValidationError("...") from e` preserves `__cause__`; `from None` only when the original is pure noise. Catch the narrowest exception — never bare `except:` (it catches `KeyboardInterrupt`/`SystemExit`). Custom exceptions inherit from a domain base (`AppError` → `NotFoundError`, `ValidationError`).
- **JS/TS**: `throw new Error('save failed', { cause: err })` (ES2022). Subclass `Error`, set `this.name`, discriminate with `instanceof` or a `code` property. Every detached promise needs `.catch()`; last-resort handlers: `process.on('unhandledRejection')` (Node), `unhandledrejection` event (browser) — log, then exit.

## API error design

- Return a stable public contract: typed/sentinel errors internally, a generic safe message + correlation ID to the client. Never leak internals (stack traces, SQL, file paths) in production responses.
- HTTP mapping: validation → 400, auth → 401/403, not found → 404, conflict → 409, rate limit → 429, else → 500 with the correlation ID.

## Result type for expected failures (optional)

When callers must handle failure as a value (TS/Go style), use a Result: `{ ok: true; value } | { ok: false; error }` (TS), or Go's `(T, error)` — but pick one style per codebase and don't mix.

## Anti-patterns (all languages)

- `except: pass` / `catch {}` swallowing silently.
- Catching, logging, and returning a generic error that hides the cause (no chaining).
- `if err != nil { return err }` everywhere with zero added context — the trace becomes useless.
- Throwing non-Error values (strings, numbers).

## Per-language depth

`golang-error-handling`, `python-error-handling`, `typescript-error-handling`.
