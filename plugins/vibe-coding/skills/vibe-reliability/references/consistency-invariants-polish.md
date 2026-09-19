# Consistency Invariants Polish

## Operation

Implement the requested coherent change at the owning source and update directly affected consumers. An earlier audit is optional when the user and repository already establish the target. Validate the changed behavior, then stop when the requested scope is complete.

## Goal

Implement one selected, evidence-backed Consistency Invariants improvement at the authoritative owner. Complete the directly affected contract without broad cleanup or redesign.

## Domain rules

- Choose an explicit consistency pattern fitting current architecture: atomic transaction, outbox/inbox, idempotent projection, version check, or reconciliation.
- Keep one source of truth and make derived-state freshness/version visible where decisions depend on it.
- Handle duplicate, reorder, and replay with stable identities and monotonic/versioned transitions.
- Update repair jobs, metrics/alerts, status surfaces, migration, and tests with the invariant.

## Validation

- Run failure-window tests around commit/publish/cache/status ordering.
- Exercise duplicate, reorder, stale read, retry, restart, and reconciliation to prove convergence.
- Record distributed/environment gates not reproducible locally.
