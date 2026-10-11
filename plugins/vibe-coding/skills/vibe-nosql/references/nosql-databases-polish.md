# Improve NoSQL Databases

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected NoSQL data path using the engine’s actual key, atomicity, consistency and indexing guarantees.

## Domain rules

- Use engine-native conditional/atomic operations at the smallest authoritative document/item boundary.
- Redesign keys/indexes only with a live-data migration, dual-read/write, backfill, and rollback/forward-fix plan when compatibility requires it.
- Make consistency and retry choices per operation; do not raise global consistency or retry counts without latency/capacity analysis.
- Treat TTL and CDC as asynchronous operational mechanisms; add explicit logical expiry or resync where exact timing/completeness is required.
- Bound pagination, fan-out, pools, retries, and change-stream consumers; expose throttling, hot partitions, lag, and conflicts.

## Validation

- Run integration tests against the supported engine/version/topology and repository migration/index tooling.
- Exercise conditional conflicts, duplicate/retry, hot partitions, node/failover behavior, stale/read-after-write semantics, TTL lag, CDC resume/resync, and pool saturation.
- Report engine-specific guarantees and untested managed-service gates separately from local observations.
