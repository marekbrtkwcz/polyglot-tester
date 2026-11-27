---
name: typescript-logging
description: Load this skill when choosing or standardizing logging in JavaScript/TypeScript: pino vs winston, structured fields, levels, correlation IDs via AsyncLocalStorage, redaction, and testing logs.
---

# TypeScript Logging

## Default: pino

```ts
import pino from "pino";

const logger = pino({ level: process.env.LOG_LEVEL ?? "info" });
logger.info({ userId: u.id, ip: req.ip }, "user logged in");
```

- Fastest mainstream logger, JSON by default — the right production choice.
- Child loggers carry context: `const log = logger.child({ requestId })`.
- `pino-pretty` for local development (as a transport); never in production.

## Alternative: winston

- Richer transport/plugin ecosystem (files, syslog, cloud sinks) — pick it when you need a specific sink. Slower than pino, fine outside hot paths.

## Levels

- trace/debug: local development detail. info: audit trail. warn: recoverable oddity. error: needs attention — pass the error object (`logger.error({ err }, "request failed")`), pino serializes the stack.
- Read the level from env at startup and fail fast on an invalid value.

## Correlation IDs

```ts
import { AsyncLocalStorage } from "node:async_hooks";

const als = new AsyncLocalStorage<{ requestId: string }>();
// middleware: als.run({ requestId: crypto.randomUUID() }, () => next());
const requestId = als.getStore()?.requestId;
const log = logger.child({ requestId });
```

- Or let `pino-http` / `express-pino-logger` do this wiring.
- With OpenTelemetry, the pino + otel bridge propagates `trace_id`/`span_id` into every log line.

## What NOT to log

- Secrets, tokens, passwords, full request bodies with credentials — use pino's `redact` option: `redact: ["req.headers.authorization", "password", "*.token"]`.
- Personal data beyond what is needed (GDPR): log IDs, not emails.
- One line per loop iteration in a hot loop — sample or aggregate.

## Errors + logging

- Log an error once, at the layer that decides the response; pass `err` objects, not `err.message` strings, so the stack survives.
- `process.on("unhandledRejection")` → log, then exit non-zero.

## Testing

- Inject the logger (constructor parameter or a settable module export). In tests, point pino at a destination stream you control and assert on the captured JSON lines, or silence with `pino({ enabled: false })`.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
- `observability-polyglot` — metrics, tracing and alerting beyond logs.
- `typescript-node-runtime` — process lifecycle, signals, env validation.
