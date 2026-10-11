# Improve Consistency Invariants

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Restore the selected business invariant across its authoritative state and directly affected projections or consumers.

## Domain rules

- Choose an explicit consistency pattern fitting current architecture: atomic transaction, outbox/inbox, idempotent projection, version check, or reconciliation.
- Keep one source of truth and make derived-state freshness/version visible where decisions depend on it.
- Handle duplicate, reorder, and replay with stable identities and monotonic/versioned transitions.
- Update repair jobs, metrics/alerts, status surfaces, migration, and tests with the invariant.

## Validation

- When the selected design uses outbox/inbox delivery, verify atomic domain/write intent and consumer identity/effect commits, or identify the external idempotency/reconciliation owner.
- Run failure-window tests around commit/publish/cache/status ordering.
- Exercise duplicate, reorder, stale read, retry, restart, and reconciliation to prove convergence.
- Record distributed/environment gates not reproducible locally.

For database-to-event delivery, select relevant cases from [Transactional Delivery Check](transactional-delivery-check.md).
