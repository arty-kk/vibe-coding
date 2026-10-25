# Redis Job Queues Audit

## Goal and scope

Audit the selected Redis-backed queue, stream or worker-lease behavior. Inspect shared cache/Redis configuration only where it affects delivery; application cache freshness belongs to the cache skill.

## Domain invariants

- Key names encode environment/tenant/entity/version intentionally, have an ownership and TTL policy, and use compatible hash-tagging when cluster multi-key atomicity is required.
- Connection pools, command/socket/connect timeouts, retry/backoff, health checks, and blocking commands are bounded per process and deployment replica.
- Atomic state transitions use one Redis command, transaction, or reviewed script; partial multi-key updates cannot silently corrupt queue/cache state.
- maxmemory/eviction and persistence/replication settings match whether data is reconstructible cache, queue state with a stated persistence guarantee, or coordination state.
- Redis Streams consumers acknowledge after processing, inspect pending entries, reclaim only stale ownership, and retain/trim data without losing required replay.
- BullMQ job IDs, lock duration/renewal, stalled handling, attempts/backoff, flows, rate limits, delayed jobs, and cleanup preserve idempotency and parent/child completion semantics.
- ARQ job uniqueness, retry/defer/cron, timeout, health, result retention, and worker shutdown match its delivery semantics rather than assuming Celery/BullMQ behavior.
- Queue retention removes completed/failed payloads only after audit/retry needs; sensitive job data is minimized and not embedded indefinitely.

## Audit method

1. Classify each Redis keyspace as cache, queue, stream, lock/lease, rate limit, dedup record, or durable state and map its TTL/eviction/persistence owner.
2. Trace enqueue → schedule/delay → reserve/claim → heartbeat/lock → side effect → ack/complete/fail → retry/DLQ/cleanup for the actual framework.
3. Inspect crash windows, duplicate job IDs, stale lock/consumer, retry storms, cron overlap, flow dependency failure, and Redis failover/reconnect.
4. Compute connection and in-flight budgets across processes/replicas and compare queue concurrency with downstream capacity and Redis memory/CPU.
5. Check scripts/transactions and cluster key-slot compatibility for every multi-key invariant.

## Handoff

Retain framework-native job/entry and business operation identity, key/slot layout, effective lease/retention settings and the failing effect/completion order. Distinguish duplicate attempts from duplicate business effects, and retained-job uniqueness from long-lived operation deduplication. Pass the first violated guarantee to Improve Redis Job Queues rather than mixing another framework's acknowledgement model.
