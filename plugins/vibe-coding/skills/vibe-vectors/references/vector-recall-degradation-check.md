# Vector Recall & Degradation Check

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

Run baseline and candidate over the same corpus, embedding space and filter scope. Record expected/actual relevant IDs, ANN agreement, relevance judgments and latency with sample count and load conditions; aggregate scores must not hide a failing protected tenant, language or selective filter.

Check forbidden documents and their counts/snippets as well as a valid allowed control. During migration, distinguish missing chunks, stale source versions and approximate-neighbor loss. A failing segment returns its query/version and first divergent stage to the repair step. Missing judgments or a small local corpus cannot establish production recall or tail latency; report that limit and hand the verified patch to Patch Checking.
