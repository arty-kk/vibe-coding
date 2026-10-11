# API Navigation Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map the selected API endpoints, validation and authorization, data effects and direct consumers.

Suggested saved map: `docs/api_map.md`.

## Inspect

Routes, controllers/handlers/resolvers, schemas/DTOs, serializers, middleware, auth guards, rate limiters, webhooks, jobs that expose/consume API contracts, OpenAPI/GraphQL/RPC files, generated clients, tests, migrations/models, docs, and deployment/runtime config that affects public behavior.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: endpoint `A-*`, group `G-*`, schema `S-*`, middleware/policy `M-*`, webhook `W-*`.

### Coverage

Cover auth/authorization model, endpoint groups, schemas, middleware/policies, role/action matrix when discoverable, versioning/deprecation, webhooks, async status flows, generated artifacts, and consumer-facing tests.

### Entry details

For each endpoint, capture method/path, owner symbol, auth/roles/tenant scope, request/response schemas, status/error behavior, validation, side effects, pagination/filtering/sorting, idempotency/webhook behavior if relevant, tests, and notes/unknowns. For each schema or middleware/policy, capture owner symbol, consumers, invariants, tests, and known drift.
