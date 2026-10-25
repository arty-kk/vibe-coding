# Improve RAG

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected retrieval/answer contract across the directly affected ingestion, access, ranking, context, citation or failure states. A small prompt or filter correction is sufficient when it resolves the demonstrated failure and its acceptance is verified.

## Scope selection

- If the user named a feature, route, command, retriever, document type, answer bug, or query class, improve that surface and directly affected ingestion/retrieval/answer states.
- If the request is broad, inspect current RAG surfaces and choose the highest-confidence improvement with visible user or operator impact.
- Include related eval, fixture, telemetry, copy, source-rendering, and cache/freshness fixes when they belong to the same RAG behavior.
- Avoid provider swaps, vector DB migrations, broad reindexing, and model changes unless the repo/user evidence requires them.

## Change targets

- Query preparation, filters, metadata, top-k/rerank parameters, chunk display, answer prompt boundaries, and source/citation rendering.
- Empty, low-confidence, partial-ingestion, stale-index, deleted-source, permission-denied, loading, error, retry, and timeout states.
- Source attribution, user-safe uncertainty, generated-content labels, and claims that must be backed by retrieved context.
- Ingestion status, reindex triggers, cache invalidation, idempotency, and operator recovery when directly tied to the selected surface.
- Tests/evals that protect the changed retrieval, citation, ACL, or answer behavior.

## Implementation principles

- Apply changes at the owner layer: loader/chunker/indexer/retriever/prompt/renderer/eval, not by duplicating local guards.
- Preserve existing model/provider/index architecture unless the task explicitly requires changing it.
- Keep answer claims truthful and traceable to current retrieved context.
- Do not log raw private documents, secrets, or unredacted user prompts.

## Validation

Run relevant repository-native checks and any RAG eval/test script that protects the changed path. If live indexes, provider keys, or fixtures are unavailable, run the deterministic parts and state the exact gap.

Keep the failing query and expected authorized/deleted/stale sources fixed during comparison. Change the first violating owner, then inspect both retrieved context and the claims/citations it supports. Recheck denied and empty-context cases when affected. Return failed observations to that same boundary; after acceptance, run Patch Checking. Do not repair missing or unauthorized retrieval by teaching the generator to sound more certain.
