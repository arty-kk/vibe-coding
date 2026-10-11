# Data Pipeline & Quality Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit a batch/stream/ELT/notebook pipeline across lineage, contracts, quality, retries, late data, reproducibility, and operational ownership.

## Domain invariants

- Source-to-sink lineage, schema, identity, partition/window, watermark, units, nullability, and ownership are explicit.
- Retries, partial batches, late/out-of-order data, duplicates, schema evolution, and backfills converge deterministically.
- Quality checks detect completeness, validity, uniqueness, referential, distribution, and freshness failures at useful boundaries.
- Production transformations, including scheduled notebooks, have versioned inputs/code, reproducible execution, meaningful validation and explicit failure ownership.

## Audit method

1. Trace one dataset from source extraction through transforms, storage, quality gates, consumers, and backfill path.
2. Check checkpoint/offset ownership, partition overwrite/append semantics, duplicate/late data, partial commit, and retry/resume.
3. Inspect schema contracts, lineage metadata, data tests, alerts, quarantine, reconciliation, and privacy/retention.
4. Identify hidden notebook/manual steps and environment/dependency drift.
