# Agent Harness Replay & Failure Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

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
