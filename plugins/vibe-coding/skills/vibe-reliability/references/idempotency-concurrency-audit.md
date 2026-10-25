# Idempotency & Concurrency Audit

## Goal and scope

Audit one operation for duplicate execution, races, lost updates, lock/lease ownership, ordering, and stale completion.

## Domain invariants

- The logical operation has a stable identity and a defined duplicate result across retries/processes.
- Read-check-write transitions are atomic, versioned, serialized, or otherwise protected at the authoritative store.
- Locks/leases have bounded lifetime, fencing or stale-owner rejection, and do not span slow external work without design evidence.
- Parallelism preserves required ordering and cannot apply stale completion over newer state.

## Audit method

1. Map operation identity, mutable state, critical sections, side effects, acknowledgement, and retry sources.
2. Construct simultaneous, duplicate, delayed, timeout-after-success, crash, lease-expiry, and stale-worker interleavings.
3. Inspect database constraints/transactions, compare-and-set/version fields, distributed lock semantics, and consumer ordering.
4. Distinguish idempotent effect from deduplicated request and document retention window.

## Handoff

Retain the logical operation key, initial state/version, exact concurrent or timeout-after-success sequence and expected effect/duplicate response. Identify which authoritative write or external effect can escape deduplication, lease or version ownership. Feed that smallest violating interleaving into Improve Idempotency & Concurrency; one local request record does not prove an external effect was protected.
