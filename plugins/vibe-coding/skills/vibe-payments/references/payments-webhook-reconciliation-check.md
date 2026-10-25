# Payments Webhook & Reconciliation Check

## Goal

Verify one payment webhook, state transition, or reconciliation invariant through safe duplicate, delayed, failed, and out-of-order scenarios.

## Context

Identify provider, selected event/state transition, implementation summary or patch boundary, expected local state/entitlement result, safe sandbox/mock environment, fixture events, and repository-native commands.

## Scenarios

- Verify webhook signature/authentication and rejection of invalid events.
- Replay the same event and prove idempotent local state and side effects.
- Deliver delayed or out-of-order events and verify legal state transitions.
- Exercise provider failure, local transaction failure, retry/reconciliation, and entitlement consistency.
- Confirm user-visible billing/API state and audit/notification behavior when directly affected.

## Execute and decide

Use synthetic customers and signed provider-version fixtures or an authorized sandbox. Establish a permitted successful flow, then deliver the selected duplicate, delayed, invalid, ambiguous-response or partial-transaction sequence while preserving operation and event identities.

Inspect provider/sandbox receipts, local billing records, deduplication/reconciliation state, entitlements and directly affected notifications separately. Rejecting a response after an unwanted effect is a failure, as is a harness that rejects every event. Distinguish allowed business lifecycle changes from a stale event overwriting accepted state.

Return passed, failed or blocked with event order, expected/observed state/effects and exercised provider layers. Pass a failure into the authorized owner repair, replay its case/control after correction and finish Patch Checking on the change. Mocks cannot establish live tax/provider behavior.
