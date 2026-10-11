# SQL Load Lock & Failover Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

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
