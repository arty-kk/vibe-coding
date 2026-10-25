# Vector Databases Audit

## Goal and scope

Audit vector retrieval from embedding/version and collection schema through tenant filtering, ingestion, ANN recall/latency, reindex, snapshot, and fallback.

## Domain invariants

- Embedding model/version, preprocessing, dimension, datatype, normalization, distance metric, collection/namespace, and payload schema are versioned as one compatibility contract.
- For protected data, tenant/authorization scope is enforced at the authoritative query boundary and cannot be omitted by a caller or applied only after forbidden candidates or metadata are exposed. Public collections and authorized global queries use their declared scope.
- Source document/chunk IDs, content/version hash, embedding version, upsert idempotency, tombstone/delete, and reconciliation prevent stale or duplicate vectors.
- Payload/filter indexes support actual filter combinations; filter semantics under ANN are understood and tested for both isolation and recall.
- ANN parameters and index build state are evaluated against a representative labelled set using recall/precision/ranking and latency distributions, not anecdotal queries.
- Capacity includes vector count/dimension, replicas/shards, index build memory/disk, compaction, write rate, query concurrency, and hot tenants.
- Model/schema/index migration uses new collection or compatible staged rebuild, backfill/checkpoint, dual-read/write/shadow evaluation, cutover, and rollback.
- Snapshots/backups and restore include collection config, payload/schema, aliases, and embedding compatibility; degradation has an explicit exact/fallback/no-result policy.

## Audit method

1. Map source/version → chunk/preprocess → embedding model → collection/payload/index → filtered query/rerank → result citation/authorization → delete/reindex.
2. Inspect every writer and query path for shared embedding/schema/tenant contracts and locate stale-data reconciliation.
3. Build or use a representative evaluation set segmented by tenant, filter selectivity, language/domain, rare terms, and hard negatives.
4. Measure recall/ranking and p50/p95/p99 latency across ANN parameters, dataset size, concurrent query/write load, and filtered cases.
5. Trace partial ingestion, duplicate retry, deletion, index-build failure, snapshot/restore, cutover, and fallback behavior.

## Diagnosis and handoff

Choose a failing query and a relevant allowed source document. Check whether the current chunk/version exists, its vector belongs to the declared embedding space, filters retain it, candidate generation retrieves it and ranking retains it. Record the first stage that loses or exposes the wrong identity; changing every retrieval parameter obscures that owner.

Compare candidate recall against an exact baseline using the same embedding metric and authorization scope. Compare relevance against human/domain judgments separately. Hand the repair step the query/filter, expected IDs, source/index versions, first divergent stage and the smallest regression that exposes it. If no judged corpus or production-scale load is available, bound the quality or latency claim to the evidence obtained.
