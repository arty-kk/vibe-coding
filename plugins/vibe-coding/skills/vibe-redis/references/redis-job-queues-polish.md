# Improve Redis Job Queues

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected Redis-backed queue or stream behavior using its actual framework delivery and recovery semantics.

## Domain rules

- Keep cache and queue durability assumptions separate; do not fix queue loss by globally disabling eviction without capacity ownership.
- Use stable job/operation IDs and idempotent side effects; align lock/heartbeat/visibility duration with real task execution and cancellation.
- Bound worker concurrency, retries, delayed work, payload size, results, completed/failed retention, and connection growth.
- Use framework-native recovery semantics for BullMQ, ARQ, or Streams instead of mixing acknowledgement models.
- Make key schema or serialization changes dual-readable/migratable when live jobs/cache entries can outlive deployment.

## Validation

- Run framework-native integration tests against the supported Redis topology/version and repository race/fake-clock tests where available.
- Exercise duplicate enqueue, crash before/after side effect and completion, lock expiry/stall, reconnect/failover, poison retry, delayed/cron timing, and cleanup.
- Measure connection count, queue age, pending/stalled work, memory, command latency, retry rate, and recovery; state topology gates not reproduced.
