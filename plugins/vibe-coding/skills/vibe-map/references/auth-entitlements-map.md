# Auth Entitlements Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map identity, roles, attributes and entitlements to the backend decisions and UI/API/job enforcement that use them.

Suggested saved map: `docs/auth_entitlements_map.md`.

## Inspect

Auth providers, session/membership models, role definitions, policy helpers, ABAC attribute sources, tenant/workspace/project scopes, entitlement/plan/quota code, route guards, API handlers, UI conditionals, feature flags, background jobs, generated clients, tests, audit logs, and docs.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: role `ROLE-*`, permission/action `PERM-*`, ABAC rule `ABAC-*`, entitlement `ENTL-*`, gate `GATE-*`, scope `SCOPE-*`, quota `QUOTA-*`.
- Anchor every rule to owner evidence. Distinguish UI visibility from backend enforcement and policy source from duplicated consumer checks.

### Coverage

Cover identities, roles, attributes, tenant scopes, policy decision points, policy enforcement points, plan/feature gates, quota limits, admin/staff/impersonation, invitations, unauthenticated/forbidden/not-found semantics, no-access/upgrade states, background/job contexts, audit logs, and tests.

### Entry details

For each permission or entitlement, capture actor, resource, action, scope, attributes, plan/quota dependency, backend owner, UI consumers, API/jobs, error/no-access behavior, tests, audit log expectations, and known drift.
