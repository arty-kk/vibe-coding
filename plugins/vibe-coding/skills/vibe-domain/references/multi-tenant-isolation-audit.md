# Multi Tenant Isolation Audit

## Goal and scope

Audit one tenant, workspace, organization, project, or account isolation boundary across API, data, cache, search, jobs, analytics, storage, and UI behavior. Limit scope to the selected boundary and direct producers/consumers.

## Domain invariants

- Every read, write, list, search, export, import, job, webhook, and object key is scoped to the correct tenant/resource owner.
- Tenant-scoped data and execution retain the verified tenant boundary across caches, clients, events, logs and jobs; authorized global/admin aggregation has its own explicit policy.
- Admin/staff/impersonation paths are explicit, audited, and do not contaminate user context.
- Forbidden/not-found behavior avoids existence leaks where the product contract requires it.
- Tests cover same-tenant, wrong-tenant, missing-tenant, and elevated-context states.

## Audit method

Trace the selected resource from route/API entry through auth context, query filters, service owner, storage/index/cache keys, async jobs, exports, object storage, analytics/logging, and UI state. Mark every unscoped or ambiguously scoped edge.

Build two synthetic tenants with distinguishable resources and trace the same operation under their trusted principals. Change supplied resource/tenant IDs independently of authenticated context and inspect the resulting data/effects. Feed the first leaking or wrongly denied edge, principal/resource identities and expected outcome to Improve Multi Tenant Isolation.
