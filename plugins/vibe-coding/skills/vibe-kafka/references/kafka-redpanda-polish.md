# Improve Kafka Redpanda

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

Fix the producer, consumer commit, state/effect identity or assignment lifecycle owner using the original record/sequence. Preserve supported partition ordering and reader/schema combinations through the transition. Feed candidate settings, record corpus and observed offsets/effects to the failure check. A mismatch returns to that owner; supported evidence proceeds to Patch Checking without silently moving the completion boundary to hide lost work.
