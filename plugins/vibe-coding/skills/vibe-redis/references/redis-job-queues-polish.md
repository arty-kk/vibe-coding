# Improve Redis Job Queues

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

Repair the framework-native enqueue, ownership/renewal, effect idempotency, completion or retention owner using the original operation. Preserve supported live key/payload versions. Feed the candidate settings and controlled crash/expiry history into the load/recovery check. Recheck failures at their owner and finish Patch Checking; increasing a lock duration or keeping every job forever is not by itself a proof of correct recovery.
