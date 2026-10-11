# Vector Recall & Degradation Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected vector retrieval contract preserves authorization, source freshness and the agreed quality/resource floor.

## Context

Identify engine/version, embedding and collection configuration, selected query/filter, source identity, labelled corpus and expected quality/freshness/resource budget.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Compare exact/brute-force or trusted baseline results with ANN across representative labelled queries and filter selectivity; report recall and ranking distributions.
- Run concurrent ingestion/query with duplicate upserts, partial batch failure, deletes, and stale source versions; verify convergence.
- Attempt all query variants across tenants and filters; prove authorization cannot be omitted or bypassed.
- Build/rebuild a new index/collection, shadow or dual-read it, cut over by alias/config, and verify rollback plus completeness.
- Degrade replicas/index availability or capacity in a test environment and verify bounded latency, quality floor, backpressure, and fallback/no-result policy.

## Verification

Compare filtered result identities, recall/ranking, source/delete convergence, latency/resource measurements and migration completeness for the selected contract.
