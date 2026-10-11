# Product Capability Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map product capabilities to actors, entry points, accepted outcomes and implementation owners.

Suggested saved map: `docs/product_capability_map.md`.

## Inspect

Product routes, navigation, feature modules, copy, onboarding, settings, billing/plan gates, permissions, analytics events, experiments, docs/PRDs, tests, API contracts, workers, and existing product maps. Use repository behavior as the primary evidence source.

## Map rules

- Suggested IDs for new entries: capability `CAP-*`, actor `ACT-*`, journey `JNY-*`, requirement `REQ-*`, acceptance `ACC-*`, metric `MET-*`, risk `RISK-*`.
- Connect each capability to an authoritative owner, visible surfaces, backend/data contracts, roles/plans/tenant scopes, tests, metrics, and known gaps.
- Separate repository facts from inferred product intent. If product docs and implementation disagree, mark drift and cite both sources.
- Do not create implementation tasks; this map feeds product audits, workstream decomposition, traceability, and release readiness.

## Coverage

Map capabilities by user/business goal, not by folder alone. Include target actors, activation path, core and edge states, monetization or entitlement dependency, analytics/events, experiments, copy/legal claims, support/admin surfaces, acceptance evidence, and explicit non-goals if they are discoverable.
