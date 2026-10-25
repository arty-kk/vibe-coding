# Payments Provider Audit

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

Use a synthetic operation/event sequence and expected local state. Compare provider acknowledgement, authenticated event, transaction commit and entitlement outcome, including the selected duplicate/out-of-order case. Pass the failing identity/transition, governing provider contract and expected durable effect to Improve Payments Provider; do not infer payment completion from a client redirect.
