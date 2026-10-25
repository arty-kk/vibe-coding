---
name: vibe-vectors
description: "Audit, repair or verify embedding/index compatibility, tenant filters, retrieval quality, freshness and reindex recovery."
---

# Vector databases

Apply [the working contract](../../references/workflow.md). Select one source-to-result path and establish its embedding/collection version, authorization scope and quality budget.

## Workflow

For missing, stale, irrelevant or forbidden results, start with **Vector Databases Audit**. Its handoff identifies the failing layer: source/chunk coverage, embedding compatibility, filter semantics, ANN candidate recall or ranking. Pass that evidence to **Improve Vector Databases**; for an already isolated defect, start with the repair recipe.

Run **Vector Recall & Degradation Check** on the affected queries, source versions and failure cases, then [Patch Checking](../vibe-review/references/patch-checking.md). Repeat review after corrections under [the cycle contract](../../references/cycles.md). A retrieval audit or benchmark request stops with its evidence.

Carry a fixed corpus/query set, judged relevant IDs, embedding and index versions, authorization filters, freshness expectations and measured resource budget. Exact nearest-neighbor agreement measures ANN approximation; judged relevance measures usefulness. A faster result that loses the required documents or exposes forbidden metadata is not an improvement.

## Recipes

| Recipe | Operation |
|---|---|
| [Vector Databases Audit](references/vector-databases-audit.md) | audit |
| [Improve Vector Databases](references/vector-databases-polish.md) | implement |
| [Vector Recall & Degradation Check](references/vector-recall-degradation-check.md) | check |
