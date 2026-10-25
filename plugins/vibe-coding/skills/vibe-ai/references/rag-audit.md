# RAG Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit retrieval-augmented generation behavior from ingestion to answer rendering. Keep only reachable issues that affect answer correctness, source grounding, access control, freshness, latency/cost, or regression resistance.

## Inspect

Document loaders, parsers, chunkers, metadata extraction, embeddings, vector/search indexes, hybrid search, rerankers, query rewriting, filters/ACL checks, tenant scoping, deletion/reindex flows, answer prompts, citation/source rendering, cache/freshness logic, admin ingestion UI, queues/jobs, tests/evals, telemetry, docs, and `docs/ai_map.md` when present.

## Issue classes

- Ingestion and indexing: stale or missing reindex paths, duplicate chunks, unstable IDs, broken deletion, bad file-type handling, lost metadata, and unbounded document size.
- Chunking and retrieval quality: chunk boundaries that drop critical context, missing title/section metadata, no multilingual handling where repo serves multiple locales, weak top-k/rerank defaults with current impact, and query rewrite drift.
- Access control: tenant/user/project ACL not applied consistently at ingestion, search, rerank, cache, or answer rendering.
- Grounding and citations: generated answers cite missing/wrong sources, source snippets cannot support claims, UI hides uncertainty, or answer prompt allows unsupported claims.
- Freshness and consistency: source docs change without invalidating index/cache, background jobs silently fail, partial ingestion is presented as complete, or embeddings/index schema drift from retrieval code.
- Operational behavior: high-cost retrieval loops, rate-limit gaps, slow hot paths, missing telemetry for empty/low-confidence retrieval, and absent operator recovery paths.
- Evaluation: missing eval fixtures for representative queries, ACL filtering, citation correctness, stale-index behavior, or known answer regressions.

## Finding quality

- Include data source, index/retriever owner, ACL/freshness boundary, expected behavior, acceptance criteria, and validation/eval direction when discoverable.
- Do not recommend provider/model/vector database swaps unless current repo evidence proves the existing owner cannot satisfy the behavior.

## Trace and hand off

Choose a query with an expected authorized source, plus a source that must not be used. Trace ingestion/version → indexed identity → filters/candidates → ranking → assembled context → answer/citations. Determine whether failure begins at coverage, access filtering, freshness, ranking, context construction or unsupported generation. Pass the query class, source/version anchors, failing boundary and expected observation to Improve RAG; do not treat a fluent answer as evidence of successful retrieval.
