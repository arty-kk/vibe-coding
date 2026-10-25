---
name: vibe-map
description: "Explain a repository or create/update a requested map of capabilities, owners, data, runtime or verification."
---

# Project mapping

Apply [the working contract](../../references/workflow.md) once. Load the map recipe that answers the user's question; the list below is a choice of views, not an instruction to generate all of them.

## Workflow

1. Define the question and output: repository orientation, one surface/flow, a rule's owner, or a maintained map update. Reuse the supplied scope and existing artifact before choosing a new map.
2. Start from an authoritative entry: registration, schema, policy, accepted requirement or test assertion. Trace the recipe's concrete relationships outward to their direct owners and consumers. Separate reachable behavior from declarations that are not wired into runtime.
3. Build the requested view with source anchors and only the fields needed to navigate or decide. Mark an unresolved relationship at the missing edge; do not fill it with an architectural guess.
4. Reopen representative source links, verify renamed/deleted symbols and check the relationships against the same source state. Repair stale entries and repeat this reference check before handing the map off.
5. For several maps, use [Map Synthesis](../vibe-task/references/map-synthesis.md) to reconcile shared entities and contradictory owners. For subsequent work, carry source anchors and open questions into the chosen audit/task workflow. A map alone does not authorize implementation or prove correctness.

An explanation can end in chat. A maintained-file update ends with the requested map complete and its documentation patch reviewed through [Patch Checking](../vibe-review/references/patch-checking.md). Do not start a product audit merely because the map exposes an unverified edge.

## Map contract

Choose the map that answers the requested question. Project Atlas provides broad orientation; it does not require generating every detailed map.

Use the requested output format. For a saved map, reuse the existing document/location and stable IDs; recipe paths and new-ID prefixes are defaults, not mandatory additions. An explanation can remain in chat.

Trace the relevant entities and relationships to current code, schema, configuration or supplied product decisions. Each useful entry identifies its defining source and the edge or rule the reader needs next. Include optional fields only when they help navigation or the requested decision; omit inapplicable rows and placeholder unknowns. Distinguish stated requirements from observed implementation.

Use a short overview and appropriate entity/relationship tables or lists. Verify references before finishing. A map indexes evidence; it does not establish runtime correctness.

## Recipes

| Recipe | Operation |
|---|---|
| [AI Navigation Map](references/ai-navigation-map.md) | map |
| [API Navigation Map](references/api-navigation-map.md) | map |
| [Auth Entitlements Map](references/auth-entitlements-map.md) | map |
| [Bot Navigation Map](references/bot-navigation-map.md) | map |
| [Domain Data Map](references/domain-data-map.md) | map |
| [Integration Map](references/integration-map.md) | map |
| [Ownership & Invariant Map](references/ownership-invariant-map.md) | map |
| [Product Capability Map](references/product-capability-map.md) | map |
| [Product Journey Map](references/product-journey-map.md) | map |
| [Product Metrics Events Map](references/product-metrics-events-map.md) | map |
| [Product Requirements Map](references/product-requirements-map.md) | map |
| [Project Atlas Map](references/project-atlas-map.md) | map |
| [RBAC ABAC Policy Map](references/rbac-abac-policy-map.md) | map |
| [Risk & Release Map](references/risk-release-map.md) | map |
| [Runtime Flow Map](references/runtime-flow-map.md) | map |
| [SaaS Navigation Map](references/saas-navigation-map.md) | map |
| [Test Coverage Map](references/test-coverage-map.md) | map |
| [Traceability Map](references/traceability-map.md) | map |
