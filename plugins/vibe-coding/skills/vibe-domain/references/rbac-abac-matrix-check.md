# RBAC ABAC Matrix Check

## Goal

Verify one RBAC/ABAC policy matrix or patch through bounded allow/deny scenarios. Prove the selected actor/resource/action/scope contract without reopening unrelated auth audit work.

## Context

Identify the selected role/attribute matrix, resource/action, expected allow/deny states, implementation summary or patch boundary, safe environment, fixtures/accounts, and repository-native commands.

## Scenarios

- Exercise allowed and denied actors across relevant tenant/resource scopes.
- Verify ABAC attributes at their source: ownership, membership, region, status, relationship, plan, quota, or feature flag.
- Check unauthenticated, wrong-tenant, missing attribute, stale attribute, no-plan, over-quota, and admin/impersonation cases when relevant.
- Confirm UI affordance and backend enforcement agree, with safe error/no-access behavior.

## Execute and decide

Define representative matrix rows before execution: actor, action, resource, scope, trusted attributes and expected decision/effect. Establish one permitted control, then vary the denied role, tenant, missing/stale attribute or plan condition that tests the selected policy. Invoke the backend directly as well as affected UI paths so hidden controls cannot masquerade as enforcement.

Inspect returned decisions and protected reads/writes, then compare UI affordances with the same policy inputs. Return passed, failed or blocked for the selected rows with actual evidence. Feed a failed row and effect into the authorized policy repair, repeat that row/control after correction and finish Patch Checking for changed code.
