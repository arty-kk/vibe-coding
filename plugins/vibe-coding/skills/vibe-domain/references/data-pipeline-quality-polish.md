# Improve Data Pipeline & Quality

## Goal

Correct the selected source-to-sink data guarantee, preserving schema, identity, retries, quality checks and recovery.

## Domain rules

- Make stage outputs idempotent or atomically committed and use stable batch/event identities.
- Version schemas and transforms; preserve mixed-version compatibility or gate cutover explicitly.
- Fail or quarantine on material quality violations with operator-visible recovery; do not silently coerce bad data.
- Make selected notebook steps parameterized, versioned and reproducible; extract code only when the required behavior or existing execution model needs it.

## Validation

- Run pipeline/schema/data-quality tests plus partial batch, retry/resume, late/duplicate, schema-change, and backfill scenarios.
- Reconcile representative source and sink counts/aggregates and inspect lineage evidence.
- List production data volume, scheduler, warehouse, and external source gates separately.

Repair the source/transform/commit/checkpoint owner using a fixed representative batch/window and expected records/aggregates. Replay the original partial/retry/late-data case alongside a normal batch and reconcile key-level values at the sink. A failing quality or recovery criterion returns to its owner; after the selected guarantee is supported, finish Patch Checking without claiming unmeasured production volume.
