---
name: python-logging
description: Load this skill when setting up or standardizing logging in Python: the logging module, structlog, levels, formatters/filters, and correlation IDs. If the language is not Python, prefer golang-logging or typescript-logging.
---

# Python Logging

## Setup once, use everywhere

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)  # per-module logger — the idiom
```

- Never `print` in library code; `logger.debug/info/warning/error/exception`.
- Configure in one place (app entrypoint / `dictConfig`), not per module.
- JSON in prod: `python-json-logger` formatter, or structlog (below).

## Levels

- DEBUG: local dev detail. INFO: audit trail (startup, key actions). WARNING: recoverable oddity. ERROR: failure needing attention. `logger.exception(...)` inside `except` adds the traceback.

## Structured logging: structlog

```python
import structlog

structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.get_logger()
log.info("user_login", user_id=u.id, ip=request.remote_addr)  # kwargs = fields
```

- Bind context once: `log = structlog.get_logger().bind(request_id=...)` — flows through the call chain.
- structlog can render through stdlib logging or standalone — pick one pipeline, don't mix.

## Correlation

- Request ID per request (middleware/ASGI): bind into logger context; include in every line.
- With OpenTelemetry: `structlog` + otel logging bridge propagates trace_id/span_id into logs.

## What NOT to log

- Secrets, tokens, passwords, full request bodies with credentials — use a `logging.Filter` to redact known field names.
- Personal data beyond what's needed (GDPR) — log IDs, not emails.
- Per-iteration debug in hot loops — sample or aggregate.

## Testing

- `caplog` fixture captures logs in tests; assert on `caplog.records` messages/levels.
- Or inject a logger (dependency) and assert on a mock — better for unit tests.

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
