# ClickHouse Ingestion & Query Load Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected ingestion identity, visible query result or resource budget using the actual table and topology.

## Context

Identify ClickHouse version/topology, table engine and keys, insert route, source checkpoint, representative data distribution and the selected duplicate, freshness or query-load promise.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Ingest duplicate/retried/partially failed batches around source checkpoint and dedup windows; verify exact observed duplicate/loss semantics.
- Run representative skewed queries and compare pruning, rows/bytes, memory/spill, p95/p99 latency, and concurrent workload limits.
- Interrupt a replica or Distributed destination in a disposable cluster; verify queueing, lag, recovery, and read consistency.
- Apply staged schema/materialized-view/mutation/backfill on representative parts; verify old/new writers/readers and rollback/forward fix.
- Drive merge/part pressure and verify insertion throttling, disk capacity, alerts, and recovery without unbounded mutations.

## Verification

Compare source/checkpoint identity, visible rows and duplicates, query results, scanned rows/bytes, parts, memory and recovery for the selected cases.

## Execute and decide

Use an isolated table/cluster or an authorized workload. Record engine/DDL/settings and create a deterministic dataset whose logical keys, versions and expected aggregates are known. Establish a normal insert/query control.

For ingestion, place the selected retry/failure at the acknowledgement or source-checkpoint boundary and compare physical rows with the expected consumer result. For merge-sensitive engines, observe the supported query semantics before and after merge rather than assuming immediate uniqueness. For load, preserve filter/time range, cardinality, skew, concurrency and measurement window; report sample limits with latency/resource results.

Return passed, failed or blocked against the selected guarantee. Pass a failure with batch/query identity and observed result to the owning repair, rerun affected cases after correction and review a changed patch through Patch Checking. Faults, mutations and backfills require a suitable authorized environment.
