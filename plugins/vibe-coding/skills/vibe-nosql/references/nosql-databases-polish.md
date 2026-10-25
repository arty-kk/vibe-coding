# Improve NoSQL Databases

## Goal

Correct the selected NoSQL data path using the engine’s actual key, atomicity, consistency and indexing guarantees.

## Domain rules

- Use engine-native conditional/atomic operations at the smallest authoritative document/item boundary.
- Redesign keys/indexes only with a live-data migration, dual-read/write, backfill, and rollback/forward-fix plan when compatibility requires it.
- Make consistency and retry choices per operation; do not raise global consistency or retry counts without latency/capacity analysis.
- Distinguish logical expiry, physical cleanup and CDC/projection visibility according to the engine. Add explicit expiry enforcement or resync when the required timing/completeness is not provided by that mechanism.
- Bound pagination, fan-out, pools, retries, and change-stream consumers; expose throttling, hot partitions, lag, and conflicts.

## Validation

- Run integration tests against the supported engine/version/topology and repository migration/index tooling.
- Exercise conditional conflicts, duplicate/retry, hot partitions, node/failover behavior, stale/read-after-write semantics, TTL lag, CDC resume/resync, and pool saturation.
- Report engine-specific guarantees and untested managed-service gates separately from local observations.

Correct the key, conditional update, consistency choice, index or lifecycle owner using fixed representative records and the original failing sequence. Preserve operation identity through ambiguous retry and stage live key/index changes with their supported reader/writer window. Feed candidate settings and final-state expectations into the domain check; repair remaining violations before Patch Checking rather than raising global retries or consistency indiscriminately.
