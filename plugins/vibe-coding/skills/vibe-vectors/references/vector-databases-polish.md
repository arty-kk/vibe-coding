# Improve Vector Databases

## Operation

Implement the requested change and verify its directly affected behavior.

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
