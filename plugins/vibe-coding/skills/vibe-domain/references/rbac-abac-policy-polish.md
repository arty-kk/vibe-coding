# Improve RBAC ABAC Policy

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Fix the selected RBAC/ABAC policy boundary end to end across the authoritative policy owner, enforcement points, UI affordances, tests, docs, and maps when used.

## Scope selection

Use the selected role/resource/action, ABAC rule, auth map row, audit finding, failing test, or explicit access bug. Do not redesign the entire permission model unless the selected fix cannot be made safely without a migration plan.

## Change targets

- Policy owner/helper/schema for actor, resource, action, scope, attributes, plan/quota, and deny reason.
- API/server action/worker enforcement and safe forbidden/not-found/no-access behavior.
- UI visibility/disabled states, upgrade or request-access copy, and route navigation.
- Audit logging and analytics where the repository already records access decisions.
- Role matrix docs, generated clients/types, fixtures, and tests for allow/deny cases.

## Implementation principles

- Preserve least privilege and make backend enforcement authoritative.
- Normalize duplicated policy checks only inside the selected boundary.
- Avoid leaking protected resource existence unless the product contract explicitly allows it.
- Keep ABAC attributes server-derived or otherwise validated at the owner layer.

## Validation

Run repository-native checks for allowed, forbidden, unauthenticated, wrong-tenant, wrong-attribute, no-plan/over-quota, and admin/impersonation states relevant to the selected boundary. Report unavailable fixtures or credentials as gates.
