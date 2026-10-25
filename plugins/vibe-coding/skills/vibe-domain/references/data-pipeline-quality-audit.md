# Data Pipeline & Quality Audit

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

## Handoff

Retain a representative source batch/event, logical key, window/watermark, checkpoint and expected sink result. Locate the first extraction, transform, commit or quality gate that loses or reinterprets that identity. Pass the failing partition/sequence and reconciliation criterion to Improve Data Pipeline & Quality; job success and equal total row counts alone cannot establish correct records or values.
