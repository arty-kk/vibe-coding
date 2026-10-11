# Payments Webhook & Reconciliation Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

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
