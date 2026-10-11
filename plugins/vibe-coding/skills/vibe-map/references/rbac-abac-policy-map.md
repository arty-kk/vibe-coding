# RBAC ABAC Policy Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map selected access decisions across subject, action, resource, attributes, scope and backend enforcement.

Suggested saved map: `docs/rbac_abac_policy_map.md`.

## Inspect

Policy helpers/engines, role enums, permission tables, membership/resource ownership models, attribute sources, feature/plan gates, admin/staff/impersonation, API handlers, server actions, frontend guards, workers, migrations, tests, seeds, docs, audit logs, and existing auth maps.

## Map rules

- Suggested IDs for new entries: policy `POL-*`, decision `DEC-*`, role `ROLE-*`, attribute `ATTR-*`, relationship `REL-*`, enforcement point `EFP-*`, test `TEST-*`.
- Separate RBAC roles, ABAC attributes, relationship/ownership checks, and entitlement gates even when they are implemented in the same helper.
- For each decision, capture subject, action, resource, scope, attributes, allow/deny semantics, owner source, UI/API/job enforcement points, denial behavior, and tests.
- Do not invent policy semantics from names alone; mark missing deny/default behavior explicitly.

## Coverage

Cover permission matrix, policy composition, deny-by-default behavior, attribute freshness, tenant isolation, delegated access, service/admin contexts, impersonation, public links/sharing, UI affordance consistency, cache/search/index leakage, audit logging, tests, and known drift.
