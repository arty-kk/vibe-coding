# RBAC ABAC Matrix Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify one RBAC/ABAC policy matrix or patch through bounded allow/deny scenarios. Prove the selected actor/resource/action/scope contract without reopening unrelated auth audit work.

## Context

Identify the selected role/attribute matrix, resource/action, expected allow/deny states, implementation summary or patch boundary, safe environment, fixtures/accounts, and repository-native commands.

## Scenarios

- Exercise allowed and denied actors across relevant tenant/resource scopes.
- Verify ABAC attributes at their source: ownership, membership, region, status, relationship, plan, quota, or feature flag.
- Check unauthenticated, wrong-tenant, missing attribute, stale attribute, no-plan, over-quota, and admin/impersonation cases when relevant.
- Confirm UI affordance and backend enforcement agree, with safe error/no-access behavior.
