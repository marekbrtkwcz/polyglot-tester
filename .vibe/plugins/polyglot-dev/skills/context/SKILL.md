---
name: context
description: Load this skill when working with request-scoped or ambient state in Go or Python — context cancellation, deadlines and values; contextvars in async code; context managers for resources; avoiding global state. Once the language is known, also read the matching references/ file (go.md, python.md) for language-specific rules.
---

# Context & Ambient State

- Request-scoped data travels explicitly (context / contextvars), never through globals.
- Every blocking operation gets a deadline or a cancellation path.
- Context values are for request-scoped data, not configuration — configuration belongs in env/config.

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | ctx as first param, cancellation, deadlines, values sparingly, request-scoped data rules |
| Python | `references/python.md` | contextvars in async code, context managers for resources, avoiding global state |
