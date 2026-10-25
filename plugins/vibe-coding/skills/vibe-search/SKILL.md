---
name: vibe-search
description: "Audit, repair or verify application search indexing, authorization, freshness, result ranking/filters and reindex recovery."
---

# Search indexes

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Search Index Audit → Improve Search Index → Search Recall & Freshness Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry authoritative document/version, query intent, relevance expectations, explicit filters/principal and freshness/deletion window between prompts. A known query/index defect starts at correction; a verification-only request uses the check without edits.

Trace write/delete → index/schema/version → query normalization/ranking/filters → hydrated results/facets → consumer. Correct the first violated projection, access or relevance boundary and replay fixed representative queries plus nearest misleading negatives.

Do not call any non-empty result a success or silently drop restrictive filters to manufacture matches. A failed ranking, stale/deleted document or access result returns to its owner, followed by the same replay and final patch review. Distinguish query language, result-display language and actually translated/indexed content; provider and reindex cutover evidence not exercised stays explicit.

## Recipes

| Recipe | Operation |
|---|---|
| [Search Index Audit](references/search-index-audit.md) | audit |
| [Improve Search Index](references/search-index-polish.md) | implement |
| [Search Recall & Freshness Check](references/search-recall-freshness-check.md) | check |
