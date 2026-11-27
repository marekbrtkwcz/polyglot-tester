---
name: python-context
description: Load this skill when managing request-scoped or ambient state in Python: contextvars in async code, context managers for resources, and avoiding global state.
---

# Python Context & Ambient State

## contextvars — the async-safe "global"

- `contextvars.ContextVar` holds per-task/per-request values that propagate through `await` automatically — the Python equivalent of Go's context / request ID threading.

```python
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar("request_id")

# middleware sets it once per request:
token = request_id.set(new_id)
try:
    await handle(request)
finally:
    request_id.reset(token)

# anywhere deeper:
logger.info("processing", extra={"request_id": request_id.get()})
```

- Each `asyncio.Task` gets a **copy** of the context — setting a var in one task doesn't leak into siblings.
- Works in threads too (each thread has its own context), but the killer feature is async propagation.
- Always `reset(token)` in `finally` — otherwise the value leaks to the next user of the context.

## Context managers for resources

- `with` for files, locks, DB connections/sessions, `tempfile.TemporaryDirectory()`.
- `@contextlib.contextmanager` for custom setup/teardown (yield = the `as` value):

```python
@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

- `contextlib.suppress(SpecificError)` when "ignore this one error" is the intent — explicit beats bare except.

## Avoiding global state

- Module-level mutable globals are a testing and concurrency hazard — pass dependencies explicitly (constructor injection).
- If you need app-wide singletons (config, logger), initialize once in one place and pass references; tests can then swap them.
- Logging: `logging.getLogger(__name__)` per module is the idiom — never `print` in library code.
