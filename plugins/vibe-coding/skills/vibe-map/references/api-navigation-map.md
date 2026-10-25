# API Navigation Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map the selected API endpoints, validation and authorization, data effects and direct consumers.

Suggested saved map: `docs/api_map.md`.

## Build the view

Enumerate the selected endpoints from actual router/schema registration. Trace each registration into middleware, handler, validation, state effects and the response consumed by a client. Compare generated contracts with their source schemas and direct callers; distinguish a declared endpoint from a reachable route. Use method/path and schema identity to join entries, then verify errors, permission scope and compatibility at their defining owners.

## Inspect

Routes, controllers/handlers/resolvers, schemas/DTOs, serializers, middleware, auth guards, rate limiters, webhooks, jobs that expose/consume API contracts, OpenAPI/GraphQL/RPC files, generated clients, tests, migrations/models, docs, and deployment/runtime config that affects public behavior.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: endpoint `A-*`, group `G-*`, schema `S-*`, middleware/policy `M-*`, webhook `W-*`.

### Coverage

Cover auth/authorization model, endpoint groups, schemas, middleware/policies, role/action matrix when discoverable, versioning/deprecation, webhooks, async status flows, generated artifacts, and consumer-facing tests.

### Entry details

For each endpoint, capture method/path, owner symbol, auth/roles/tenant scope, request/response schemas, status/error behavior, validation, side effects, pagination/filtering/sorting, idempotency/webhook behavior if relevant, tests, and notes/unknowns. For each schema or middleware/policy, capture owner symbol, consumers, invariants, tests, and known drift.
