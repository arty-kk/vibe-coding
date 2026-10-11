# NoSQL Consistency & Hot Partition Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

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
