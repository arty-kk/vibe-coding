# Improve Idempotency & Concurrency

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected duplicate or concurrent operation so final state and effects satisfy the intended contract.

## Domain rules

- Enforce uniqueness/versioning at the authoritative boundary and return the prior result or stable terminal status for duplicates.
- Use fencing/version checks for leased work and reject stale completion.
- Keep critical sections small and avoid lock-based coordination when a store-level atomic operation fits existing architecture.
- Synchronize retries, acknowledgements, status, cleanup, metrics, and tests with the concurrency contract.

## Validation

- Run deterministic concurrent/duplicate/crash/timeout/stale-worker tests and repository race detectors where available.
- Verify side-effect count, final state/version, lock/lease cleanup, and duplicate response.
- List distributed timing or multi-node gates not exercised.
