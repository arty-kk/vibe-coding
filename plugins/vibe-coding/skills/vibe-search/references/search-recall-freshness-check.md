# Search Recall & Freshness Check

## Goal

Verify one search/index invariant through bounded indexing, freshness, deletion, permission, and query scenarios.

## Context

Identify selected index/query/resource, expected result behavior, implementation summary or patch boundary, safe environment, fixtures, and repository-native commands.

## Scenarios

- Index/create a resource and verify it is searchable through the expected query path.
- Update/delete the resource and verify freshness or documented delay semantics.
- Verify tenant/role/privacy filters prevent unauthorized results.
- Exercise filters/facets/sorting/pagination and empty/error states relevant to the selected boundary.
- Run reindex/backfill or provider-mock checks when the patch changes document schema.

## Execute and decide

Fix a source/index snapshot, representative documents/principals and relevance judgments before replay. Include exact identifiers, natural task descriptions, domain/operation filters, supported language/aliases and nearest misleading results. State the top-rank/recall or result-set property the selected task requires; do not invent a universal score threshold.

Establish allowed normal queries, then replay the selected miss/ranking/filter case and source update/delete or permission change. Inspect returned IDs/order, snippets/facets/counts, hydration and the promised freshness window. For pagination, compare successive pages under the stated snapshot/ordering contract and check identity overlap/omissions.

Return passed, failed or blocked with corpus/query identity, expected/observed results and index/environment limits. Feed failures to the authorized owner repair, repeat their corpus/control after correction and finish Patch Checking. A non-empty list or one successful exact-ID lookup does not establish natural-language search quality.
