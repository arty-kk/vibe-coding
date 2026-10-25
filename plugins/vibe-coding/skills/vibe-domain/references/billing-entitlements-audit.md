# Billing Entitlements Audit

## Goal

Audit billing, plan, quota, entitlement, tenant, and permission behavior for correctness and user-visible consistency. Keep only issues with repository evidence; do not invent pricing rules, plan names, provider behavior, or business policy.

## Inspect

Plan definitions, auth entitlement maps when present, billing provider integration, webhook handlers, subscription state, entitlement/feature-flag helpers, quota counters, RBAC/ABAC/tenant/workspace ownership, route/API guards, UI gates, upgrade/downgrade/trial/cancel flows, invoices/payment states, jobs/reconciliation, tests, docs, and env/config. Use [Payments Provider Audit](../../vibe-payments/references/payments-provider-audit.md) when the provider runtime/webhook contract itself is the primary risk.

## Issue classes

- Source-of-truth drift: different plan/quota/feature rules across UI, API, workers, docs, tests, and provider mapping.
- Enforcement gaps: visible actions not server-enforced, disabled UI hiding allowed operations, missing tenant/role checks, stale subscription state, or quota race conditions.
- Lifecycle bugs: trial start/end, upgrade/downgrade, cancel/reactivate, payment failure, grace period, webhook retry/order/idempotency, and reconciliation gaps.
- User-facing clarity: no-access/no-plan/over-quota/upgrade copy contradicts actual entitlements or provides unsafe diagnostics.
- Data safety: cross-tenant billing exposure, wrong invoice/account owner, destructive plan action without confirmation/audit trail.
- Regression resistance: missing tests for plan matrix, webhook idempotency, quota boundaries, or UI/API gate alignment.

## Finding quality

- Include affected plan/role/tenant state, expected behavior, acceptance criteria, and validation direction.

## Trace and hand off

Trace the selected subscription/plan state into the local entitlement decision, quota update, backend action and displayed state. Separate provider event truth from the application's local policy. Preserve the actor/tenant, lifecycle sequence and expected allowed/denied or quota outcome for Improve Billing Entitlements. Route a signed-event or provider reconciliation defect to Payments rather than inventing local plan rules to conceal it.
