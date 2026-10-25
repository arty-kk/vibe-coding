# Improve Auth Permissions

## Goal

Fix the selected authentication, authorization, tenancy, or permission-gated experience end to end. The patch should align owner-layer checks, API behavior, UI affordances, copy, and tests.

## Scope selection

- If the user named a role, route, endpoint, workspace, plan state, invitation flow, or access bug, improve that boundary and directly affected surfaces.
- If the request is broad, inspect permission seams and apply the highest-confidence improvement with security, correctness, or user-impact value.
- Include related no-access UI, error/copy, redirects, audit logging, and tests when they belong to the same access contract.
- Avoid broad auth rewrites, provider migrations, role-model redesigns, or entitlement changes unless required by the selected fix.

## Change targets

- Server-side owner checks for role, tenant/workspace/project ownership, membership, plan/entitlement, invitation token, and admin/impersonation context.
- API/server action behavior: safe status codes, machine-readable errors, no data leakage in forbidden/not-found paths, and stable redirect/recovery behavior.
- UI behavior: hidden vs disabled actions, explanatory no-access/upgrade states, safe destructive states, and consistency between visible affordances and allowed operations.
- Shared permission helpers/types/tests to reduce drift across routes, handlers, components, workers, and generated clients.
- Session lifecycle, cache keys, query filters, and background/job/webhook contexts where they touch the same access boundary.

## Implementation principles

- Enforce permissions in the backend/owner layer, not only in UI.
- Preserve least privilege and existing public contracts unless the task authorizes a contract change.
- Avoid leaking whether protected resources exist unless the repo already defines that behavior safely.

## Validation

Run repository-native checks for allowed, forbidden, unauthenticated, wrong-tenant/wrong-owner, and relevant plan/role states. If a state cannot be exercised because fixtures/credentials are unavailable, state the limitation and the exact manual verification path.

Repair trusted identity/scope construction or the authoritative access decision before adjusting its UI consumer. Replay the same allowed and denied cases and inspect protected state/effects, session transitions and recovery. Use the OAuth/OIDC session check only for the implemented protocol boundary. A remaining violation returns to that owner; supported acceptance proceeds to Patch Checking.
