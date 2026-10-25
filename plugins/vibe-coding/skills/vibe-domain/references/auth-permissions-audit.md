# Auth Permissions Audit

## Goal

Audit authentication, authorization, tenancy, roles, session boundaries, and permission-gated UI/API behavior. Keep only reachable issues that can cause unauthorized access, user confusion, broken legitimate access, or maintainability drift in permission logic.

## Inspect

Auth middleware/guards, session/JWT/cookie handling, route protection, server actions/API handlers, role/permission models, RBAC/ABAC policy helpers/maps, tenant/workspace/project scoping, plan/entitlement gates, admin impersonation, invitation/member flows, frontend route guards, disabled/hidden UI actions, cache/search/export filters, audit logs, tests, seed data, migrations, docs, and generated maps when present.

## Issue classes

- Boundary gaps: protected data or mutations reachable without the expected session, role, tenant, ownership, plan, or feature gate.
- Scope confusion: user/workspace/project/org IDs accepted from the client without owner-layer verification, inconsistent tenant filters, unsafe cache keys, or cross-tenant search/index leakage.
- Role drift: duplicated permission checks, UI-only enforcement, inconsistent admin/member semantics, stale enum values, or migrations that do not match application checks.
- Session lifecycle: weak logout/session invalidation, invitation/recovery token handling, refresh behavior, impersonation escape, missing CSRF protection where relevant, or unsafe redirect handling.
- UX/API mismatch: UI hides/shows actions incorrectly, backend rejects valid actions without recovery, forbidden states have misleading copy, or plan gates conflict with entitlements.
- Regression resistance: missing tests for role boundaries, tenant isolation, forbidden mutations, invitation flows, ownership transfer, and no-access UI states.

## Trace and hand off

Choose a legitimate principal/resource/action and a closely related denied case. Follow identity/session establishment, trusted scope construction, owner decision, enforcement and resulting data/effect. Record the first disagreement, including UI recovery only when directly affected. Pass the principal/state, violated rule and observable allowed/denied result into Improve Auth Permissions; a hidden action is not proof of backend denial.
