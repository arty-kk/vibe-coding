# Tenant Isolation Check

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

## Execute and decide

Create distinguishable synthetic tenants/resources and a verified principal for each. Establish same-tenant success, then reuse another tenant's resource identity and vary missing/stale context at the selected API, job, cache/search or object boundary.

Inspect response contents, persisted effects and affected asynchronous output. A denied response after a cross-tenant write still fails. Verify elevated/global access against its explicit policy rather than classifying every cross-tenant administrator operation as a leak.

Return passed, failed or blocked with the principal/resource/context and observed data/effects. Pass the leaking or wrongly denied edge into the authorized isolation repair, rerun it with its permitted control and finish Patch Checking on the resulting change.
