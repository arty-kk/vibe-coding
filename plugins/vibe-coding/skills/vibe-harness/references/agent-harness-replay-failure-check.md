# Agent Harness Replay & Failure Check

## Goal

Verify that the selected run can resume or replay without losing required state or repeating protected effects.

## Context

Identify selected run/step transition, stable operation identity, durable checkpoint/effect stores, lease/version rules and expected terminal result.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Crash immediately before and after tool side effects, checkpoint commits, child joins, and terminal publication; resume each history.
- Duplicate the same run/step/tool request and prove stable deduplication or safe repeatability.
- Lose a worker lease during a long tool call and verify fencing blocks stale completion.
- Saturate fan-out/downstream capacity and verify bounded admission, fair progress, cancellation, and recovery.
- Replay a stored run and compare decisions, events, state versions, and externally committed effects.

## Verification

Compare durable state and versions, protected effect count, child cleanup and terminal outcomes after the selected crash/replay windows.

## Execute and decide

Use controlled stores/tools and a fixed run/input history. Establish normal completion, then hold one selected boundary before or after effect commit, receipt/checkpoint persistence, join or terminal publication. Interrupt/resume or lose the lease there and retain the same operation identity.

Inspect the authoritative effect store alongside run versions, receipts, child lifetimes and emitted outcomes. A single local terminal record cannot conceal duplicate remote effects, and a replay that skips required work is not success. Select only the histories necessary for the stated guarantee.

Return passed, failed or blocked with the interleaving, expected/observed effects and durable state. Feed a failure into the authorized owner repair, repeat the history/control after correction and finish Patch Checking for changed code. Synthetic tool receipts do not prove an untested provider's replay behavior.
