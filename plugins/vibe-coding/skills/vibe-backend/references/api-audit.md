# API Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit the reachable API surface for behavior, contract, validation, security-adjacent, and integration defects. Keep only issues supported by current repository evidence.

## Inspect

- Route definitions, controllers/handlers/resolvers, middleware, auth guards, policies, schemas/DTOs, serializers, validators, generated clients, OpenAPI/GraphQL/RPC docs, tests, migrations/models, and consumers.
- Public, internal, webhook, admin, background-triggered, generated, and third-party-facing endpoints.
- `docs/api_map.md` when present as a discovery aid, then verify against current source.

## Issue classes

- Method semantics, status codes, redirects, cache headers, CORS/CSRF assumptions, and content negotiation.
- Authn/authz behavior, tenant scoping, role/action checks, and status-code information leaks.
- Request validation, coercion, unknown fields, file/upload boundaries, body/query/path param consistency, and schema enforcement.
- Error envelope consistency, operator/user-safe diagnostics, partial success, and retry semantics.
- Response shape stability: field names, nullability, enum values, timestamps, serialization, sorting, and localization-sensitive values.
- Pagination, filtering, sorting, cursor stability, idempotency, async operation status, rate limits, quota headers, and webhooks.
- Versioning, deprecation, generated schema/client drift, and docs that would mislead consumers.
- REST/GraphQL/RPC conventions where the repository already relies on them.

## Finding quality

- Include reachable surface, affected actors/consumers/states, expected behavior, acceptance criteria, and validation direction when discoverable.
- Do not report generic REST purity issues unless the inconsistency creates current consumer or system impact.

## Trace and hand off

Choose a representative endpoint, principal and input. Follow registration/middleware → validation → rule owner → stored effect → serialization → actual consumer interpretation. Pair a valid request with the selected invalid, denied, duplicate or conflicting case. Locate the first violated boundary and pass its minimal request, initial state, expected response/effect and consumer consequence to Improve API when repair is authorized.
