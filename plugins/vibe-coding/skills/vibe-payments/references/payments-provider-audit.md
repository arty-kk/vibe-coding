# Payments Provider Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit one payments provider boundary such as checkout, subscription lifecycle, invoice state, webhook ingestion, entitlement activation, refund, chargeback, reconciliation, or tax/payment status mapping.

## Domain invariants

- Provider state, local billing state, and local entitlements have one authoritative reconciliation path.
- Webhooks are authenticated, idempotent, order-tolerant, replay-safe, and mapped to legal local transitions.
- Test/live mode, currency, amount, tax, invoice, refund, chargeback, cancellation, grace period, and failed-payment semantics are explicit.
- User-visible billing UI, API behavior, audit logs, and notifications reflect the same local source of truth.
- Tests or sandbox checks cover duplicate, delayed, missing, failed, and out-of-order provider events where relevant.

## Audit method

Trace the selected payment flow from user/API action through provider request, local persistence, webhook/reconciliation, entitlement changes, notifications, audit logs, UI state, and tests. Separate provider assumptions from repository evidence.
