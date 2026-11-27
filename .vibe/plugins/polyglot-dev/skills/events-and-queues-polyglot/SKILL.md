---
name: events-and-queues-polyglot
description: Load this skill when building event-driven or queue-based systems in JavaScript/TypeScript, Python, or Go — Kafka/SQS/RabbitMQ, producer/consumer contracts, idempotency, retries with backoff, dead-letter queues, and testing async flows.
---

# Events & Queues (Polyglot)

## Broker choice

- **Kafka**: high-throughput event streaming, replay, partitions for ordering per key.
- **RabbitMQ**: flexible routing, good for task queues with priorities and TTLs.
- **SQS/SNS (AWS)**: managed, simple, at-least-once delivery — design for duplicates.
- Rule: at-least-once delivery is the norm — **every consumer must be idempotent**.

## Message contract

- Schema-registered payloads (Avro/Protobuf/JSON Schema in a registry) so producers and consumers can't drift silently.
- Include: message ID, timestamp, type/version, correlation ID. Consumers must ignore unknown fields (forward compatibility).
- Ordering only per partition key — don't assume global order.

## Consumers

- Idempotency: store processed message IDs (dedup table with unique constraint) or make handlers naturally idempotent (upsert by business key).
- Retry with exponential backoff + jitter; cap attempts, then **dead-letter queue (DLQ)** with alerting — a message in DLQ is an incident.
- Poison messages: after N failures, DLQ immediately rather than blocking the partition/queue.
- Graceful shutdown: stop polling, finish in-flight message (within visibility timeout), then exit.

## Per-language notes

- **JS/TS**: `kafkajs` or `@aws-sdk/client-sqs`; process with bounded concurrency (p-limit); `sqs-consumer` for SQS.
- **Python**: `aiokafka`/`confluent-kafka`, `pika` (RabbitMQ), `boto3` SQS; Celery/RQ/Dramatiq for task queues with retries/DLQ built in.
- **Go**: `sarama`/`franz-go` (Kafka), `amqp091-go` (RabbitMQ), `aws-sdk-go-v2` SQS; `errgroup` with context for consumer groups.

## Testing async flows

- Unit: handler with a fabricated message; assert side effects + idempotent re-processing.
- Integration: real broker in containers (Testcontainers) or localstack for SQS — verify publish → consume → effect.
- Test the failure paths: duplicate delivery, malformed message → DLQ, broker down → backoff behavior.
- Flake-proof: poll with timeout for eventual state; never `sleep(5)` and hope.

## Related

- `observability-polyglot` — lag, DLQ depth, and redelivery rate are the signals to watch once events flow.
