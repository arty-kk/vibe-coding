# Improve Payments Provider

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected provider-event or billing transition while preserving authenticated ingestion, idempotency and local entitlements.

## Scope selection

Use the selected checkout/subscription/invoice/webhook/refund/chargeback/reconciliation bug, audit finding, failing test, provider event sample, or explicit billing task. Do not migrate payment providers or redesign pricing unless required by the selected fix.

## Change targets

- Provider SDK/client wrapper, request construction, idempotency keys, timeouts/retries, and test/live configuration.
- Local billing state machine, invoice/payment records, entitlement activation/deactivation, grace periods, and audit logs.
- Webhook verification, event deduplication, ordering tolerance, replay safety, and reconciliation jobs.
- Billing UI/API states, user notifications, tests/fixtures, generated types, and maps/docs directly affected.

## Implementation principles

- Make local state transitions explicit and monotonic where provider events can arrive late or duplicated.
- Never trust unauthenticated webhooks or client-only payment success.
- Preserve existing customer/subscription data compatibility and define forward-fix for unsafe rollback.
- Avoid touching unrelated pricing, plans, coupons, or tax behavior.

## Validation

Run repository-native tests and safe sandbox/provider-mock scenarios for the selected path: success, failure, duplicate event, delayed event, out-of-order event, refund/chargeback/cancellation when relevant. Report live-provider, tax, or managed-service gates honestly.
