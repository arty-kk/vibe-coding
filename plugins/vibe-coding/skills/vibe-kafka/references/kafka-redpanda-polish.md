# Improve Kafka Redpanda

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected Kafka/Redpanda delivery contract across record identity, offsets, ordering and replay.

## Domain rules

- Keep topic/key/schema/consumer-state changes compatible through staged producers and consumers; use explicit versioning or dual-read/write when required.
- Place offset commits at the real completion boundary and make external side effects idempotent; do not call broker exactly-once a guarantee for arbitrary external systems.
- Bound retries and processing concurrency, pause/resume deliberately, and preserve partition ownership/order where required.
- Use producer transactions only with a complete transactional topology and reader isolation; otherwise state the duplicate/loss contract explicitly.
- Treat partition-count changes, compaction keys, retention, and migration feature differences as data-contract changes with replay implications.

## Validation

- Run serializer/schema compatibility and repository integration tests against the supported broker implementation(s).
- Exercise duplicate delivery, process crash at commit boundaries, consumer rebalance, poison record, partition unavailability, and graceful shutdown.
- Report observed loss/duplicate/order/lag/recovery behavior and any broker-level gates not reproduced locally.
