# SQL Load Lock & Failover Check

## Goal

Verify the selected query or transaction invariant and resource/recovery behavior under supported database conditions.

## Context

Identify database/proxy versions and topology, selected query/transaction, application roles, connection/deadline budgets, required invariant and representative data.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Drive pool saturation across representative application replicas and verify bounded acquire wait, timeout, admission, and reserved recovery capacity.
- Run the changed query with representative skew/cardinality and compare plan, rows, buffers/I/O, memory/temp spill, and latency distribution.
- Execute conflicting transactions to prove isolation/constraint behavior, lock order, deadlock/serialization retry, and final invariant.
- Interrupt and resume schema migration/backfill while old/new application versions run; verify compatibility, load control, and rollback/forward fix.
- Simulate connection reset/primary failover or use a test proxy; verify pool recovery, session reset, transaction outcome ambiguity, and replica consistency.

## Verification

Compare final committed state, transaction outcome, query plan/results, connection cleanup and permitted freshness; qualify mocks, in-memory engines and failover simulations.

## Execute and decide

Use the supported engine and application/migration roles with deterministic records and expected committed values. Establish a normal transaction/query control, then use coordinated sessions or a test proxy to hold the selected acquire, lock, statement, commit or replica-read boundary.

Observe actual committed rows, errors/retries, transaction/session cleanup and pool state independently of the caller response. For plan/load cases, preserve predicates, cardinality/skew, concurrency and measurement window. For migration or failover, inspect supported mixed-version data and ambiguous outcome recovery.

Return passed, failed or blocked with the exact role/sequence, values/plan/resource evidence and missing topology layers. Pass failures to the authorized owner repair, replay the affected control/interleaving after correction and finish Patch Checking. Faults, backfills and load need an appropriate test environment.
