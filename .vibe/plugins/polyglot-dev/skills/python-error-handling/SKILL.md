---
name: python-error-handling
description: Load this skill when designing error handling in Python: custom exceptions, exception chaining with raise-from, traceback reading, and logging errors correctly.
---

# Python Error Handling

## The hierarchy

- Catch the **narrowest** exception: `except ValueError`, never bare `except:` (it catches `KeyboardInterrupt`/`SystemExit` too — use `except Exception:` if you must).
- Custom exceptions inherit from a domain base:

```python
class AppError(Exception): ...

class NotFoundError(AppError): ...

class ValidationError(AppError): ...
```

Callers can then catch `AppError` broadly or `NotFoundError` specifically.

## Chaining: raise ... from

```python
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    raise ValidationError(f"invalid JSON at line {e.lineno}") from e
```

`from e` preserves the original traceback (`__cause__`); `from None` suppresses it when the original is noise. Never swallow silently.

## Raising

- `raise ValidationError("id must be positive")` — message for humans, args for programmatic access.
- Include context in the message: what failed, with which value.
- Don't raise for expected control flow — return `None`/sentinel or use `Optional`; exceptions are for exceptional cases (and in Python, also for some control flow like `StopIteration`).

## Reading tracebacks

- Read **bottom-up**: the last frame is where it exploded, the frames above show the call chain.
- `Traceback (most recent call last)` — the *most recent* is at the bottom.
- `e.__cause__` / `e.__context__` hold the chain — print with `traceback.format_exception`.

## Logging errors

- `logger.exception("...")` inside `except` — includes the traceback automatically (equivalent to `error(..., exc_info=True)`).
- Log once, at the boundary that handles it; don't log and re-raise (double logs).
- Never log sensitive data in error messages (tokens, passwords).

## Anti-patterns

- `except: pass` — the silent killer.
- Catching, logging, and returning a generic error that hides the cause (no `from`).
- Using exceptions for flow control in hot loops — raise/catch is not free.

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
