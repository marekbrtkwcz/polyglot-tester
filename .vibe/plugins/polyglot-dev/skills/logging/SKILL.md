---
name: logging
description: Load this skill when choosing or standardizing logging in JavaScript/TypeScript, Python, or Go — structured fields, levels, correlation IDs, redaction, and testing logs. Once the language is known, also read the matching references/ file (go.md, python.md, ts.md) for that stack's logging depth.
---

# Logging

- Structured logs (fields, not interpolated strings) so queries and alerts actually work.
- One correlation/request ID per request, propagated across async boundaries.
- Never log secrets or PII — redact at the logger and test the redaction.

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | log/slog in depth, structured attributes, levels, context propagation, when zap/zerolog beat stdlib |
| Python | `references/python.md` | logging module, structlog, levels, formatters/filters, correlation IDs |
| JavaScript/TypeScript | `references/ts.md` | pino vs winston, structured fields, AsyncLocalStorage correlation IDs, redaction, testing logs |
