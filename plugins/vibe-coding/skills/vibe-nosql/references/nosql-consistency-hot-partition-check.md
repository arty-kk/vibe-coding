# NoSQL Consistency & Hot Partition Check

## Goal

Verify the selected data invariant and access/resource behavior using the engine’s actual atomicity and partition model.

## Context

Identify engine/version/topology, selected key/document and query, index, consistency/conditional-write policy, expected invariant and representative skew.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Generate representative skew/hot keys and verify throttling, latency, partition distribution, capacity response, and recovery.
- Run conflicting conditional/transactional updates and retries; verify final invariant and conflict/error mapping.
- Interrupt topology/connection paths and verify bounded selection/connect/socket timeouts, retries, pool recovery, and stale-read contract.
- Expire data and interrupt change-stream consumers; verify asynchronous TTL expectations, resume token, duplicates, retention gap, and full resync.
- Exercise each changed query/index with representative cardinality and pagination; reject unbounded scan/fan-out behavior.

## Verification

Compare final stored values, conflict handling, access path, read freshness, TTL/stream behavior and resource bounds using engine-specific evidence.

## Execute and decide

Use the selected engine/topology and deterministic records with known keys, versions and expected values. Establish a normal write/read/query control. Synchronize the chosen concurrent update, ambiguous retry, stale read or CDC interruption and observe the authoritative final records and relevant projection.

For access/resource checks, retain query predicates, index evidence, cardinality/skew, page/fan-out bounds and measurement window. For TTL/CDC, observe logical expiry separately from cleanup and stream/index lag; a resume token alone does not prove a retention gap was recovered.

Return passed, failed or blocked with engine, sequence, stored values/access evidence and missing managed-service layers. Pass a failure to the authorized owner repair, repeat its case/control and finish Patch Checking for changed code/configuration. Use a suitable test environment for topology faults, backfills and saturation.
