# Improve ClickHouse

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected ClickHouse ingestion, table or query behavior using its actual engine, keys and merge semantics.

## Domain rules

- Choose engine/partition/ORDER BY from concrete access and lifecycle patterns; avoid high-cardinality partitions and broad `FINAL` as a routine correctness fix.
- Make ingestion idempotency explicit with stable source identity and supported dedup semantics; do not rely on a short dedup window for indefinite retries.
- Rewrite queries to prune early, bound joins/aggregations/results, and use projections/dictionaries/materialized views only with owned refresh/consistency semantics.
- Stage schema/view/backfill changes and throttle mutations or rebuilds; preserve compatibility for existing parts and distributed replicas.
- Set users, quotas, profiles, pools, and workload limits from aggregate deployment capacity and expose system-table signals.

## Validation

- Run DDL/query/ingestion integration tests against the supported ClickHouse version/topology and inspect system tables/query logs.
- Exercise duplicate/retried batches, partial failure, late data, replica/distributed-queue disruption, merge pressure, mutation/backfill, and query concurrency.
- Measure scanned rows/bytes, memory/spill, parts, merge backlog, insert/query latency, and result correctness with representative data shape.
