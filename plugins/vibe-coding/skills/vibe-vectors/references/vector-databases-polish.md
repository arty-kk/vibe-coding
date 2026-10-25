# Improve Vector Databases

## Goal

Correct the selected embedding, indexing or retrieval behavior while preserving filter isolation, quality and freshness.

## Domain rules

- Centralize embedding/collection compatibility metadata and reject mismatched dimensions/model versions before write/query.
- Enforce tenant filters server-side in the repository's retrieval boundary and cover every query variant with isolation tests.
- Use stable source/chunk IDs and versioned idempotent upserts; reconcile deletes and failed partial batches.
- Tune ANN only against an evaluation dataset and explicit latency/resource budget; preserve a measurable quality floor.
- Perform reindex/migration through staged collection/alias cutover with completeness and quality comparison plus rollback.

## Validation

- Run integration tests against the supported vector engine/version, including payload filters, aliases, snapshots, and consistency settings used in production.
- Evaluate retrieval quality and latency under representative filters, concurrency, write load, partial failure, and degraded index state.
- Verify tenant isolation, stale/delete convergence, migration completeness, snapshot restore, and fallback behavior.

## Repair and handoff

Reproduce the failing query or ingestion event before changing the owner identified by the audit. Preserve an unchanged query/filter as a control. If embedding preprocessing or model changes, ensure both writers and queries move to the compatible space; matching dimensions alone do not establish compatible embeddings.

For stale data, repair version ordering, partial-batch reconciliation or tombstone handling before tuning ANN. For recall loss, compare equivalent filtered exact/ANN results before changing candidate counts, index parameters or reranking. Retain the declared latency/resource budget and authorization scope throughout.

Give the check step the baseline/candidate configurations, fixed corpus and queries, expected IDs, changed stage and migration/deletion evidence. For a cutover, report completeness and a usable recovery path rather than treating an alias switch as proof of a successful rebuild. Pass the complete patch and verification limits to Patch Checking.
