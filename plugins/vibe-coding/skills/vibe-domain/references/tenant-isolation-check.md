# Tenant Isolation Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify one tenant/workspace/project isolation invariant through bounded cross-tenant scenarios. Prove the selected patch or behavior without broadening into unrelated auth or data audit work.

## Context

Identify the selected resource/action, tenant states, implementation summary or patch boundary, safe fixtures/accounts, and repository-native commands or manual scenarios.

## Scenarios

- Same-tenant access succeeds with correct data.
- Wrong-tenant read, list, search, write, export, job, or object access fails safely.
- Missing/stale tenant context fails safely.
- Admin/staff/impersonation access follows explicit policy and produces audit evidence when required.
- Cache/search/analytics/logging surfaces do not expose another tenant’s data for the selected boundary.
