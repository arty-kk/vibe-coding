# Project Atlas Map

## Operation

Map the requested area using current repository evidence.

## Goal

Explain the product, major modules, runtime entry points, data owners and useful detailed references for repository orientation.

Suggested saved map: `docs/project_atlas_map.md`.

## Build the view

Identify executable/deployed entry points from manifests and runtime configuration, then follow representative product requests and jobs into their owning modules and data stores. Use those traces to explain boundaries and dependencies. Link to a detailed map only when it exists or the user requests it. Finish with a small set of source-backed starting points and unresolved boundaries; folder names alone are not an architecture model.

## Inspect

Read entry docs, package/workspace manifests, application roots, routing, API handlers, workers/jobs, storage schemas, infrastructure/config, integration clients, auth and billing seams, test entry points, generated artifacts, and existing maps. Prefer current repository files over stale prose.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: capability `CAP-*`, bounded context `CTX-*`, surface `SURF-*`, runtime flow `FLOW-*`, integration `INT-*`, risk or unknown `RISK-*`.
- Treat generated maps as discovery aids, not authority. Verify risky or stale claims against code, schemas, config, tests, canonical specs, or runtime evidence.

### Coverage

Cover product type and users, core capabilities, bounded contexts, UI/API/bot/AI/mobile surfaces, storage and state owners, jobs/workflows, external integrations, auth/entitlements, observability/ops surfaces, test strategy, release gates, and links to detailed maps.

### Entry details

For each capability or context, capture owner files/symbols, primary actors, input/output contracts, main data entities, direct producers/consumers, related tests/docs, and the next best skills for deeper audit or polish. Avoid speculative architecture narratives.
