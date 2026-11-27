---
name: observability-polyglot
description: Load this skill when adding or fixing logging, metrics, and tracing in JavaScript/TypeScript, Python, or Go — structured logs, RED/USE metrics, correlation IDs, and alerting on symptoms. For logging alone in one language prefer golang-logging, python-logging, or typescript-logging.
---

# Observability (Polyglot)

## The three signals

- **Logs**: discrete events, structured (JSON in production), with level, timestamp, message, and context.
- **Metrics**: aggregated numbers over time — RED (rate, errors, duration) for services, USE (utilization, saturation, errors) for resources.
- **Traces**: request path across services with span IDs and a shared trace ID.

## Structured logging rules

- One log line = one JSON object in prod: `level`, `ts`, `msg`, plus context fields (`trace_id`, `user_id`, `route`).
- Levels: `debug` (dev only), `info` (business events), `warn` (recoverable anomalies), `error` (action needed, with stack).
- Never log secrets/PII; scrub or hash identifiers at the logging boundary.
- Log at the decision points: request received, external call made (with latency), error caught at top level.

## Correlation

- Propagate `traceparent`/`trace-id` header end to end; generate at the edge if missing.
- Include the correlation ID in error responses so users can report it.

## Metrics discipline

- Counters for events, gauges for current state, histograms for latency/size — pick per use, don't default to everything.
- Bound cardinality: never put user IDs, emails, or raw URLs in label/tag values.
- Alert on symptoms (error rate, p99 latency, queue depth), not on causes you can't measure; every alert must be actionable.

## Per-language quick reference

- **JS/TS**: `pino` (fast, JSON) in Node; `console` methods map to levels in dev; OpenTelemetry SDK (`@opentelemetry/sdk-node`) for metrics+traces; browser: `navigator.sendBeacon`, Web Vitals.
- **Python**: stdlib `logging` with `dictConfig`/JSON formatter, or `structlog`; OpenTelemetry SDK (`opentelemetry-sdk`) for traces/metrics; Prometheus client for /metrics.
- **Go**: `log/slog` (structured by default), zap/zerolog for hot paths; OpenTelemetry Go SDK; Prometheus client_golang.

## Health checks

- `/health` (liveness: process up) vs `/ready` (readiness: dependencies reachable) — wire both into orchestrators.

## Related

- Per-language logging depth: `python-logging`, `golang-logging`, `typescript-logging`.
- `events-and-queues-polyglot` — broker lag and DLQ metrics for queue-backed systems.
