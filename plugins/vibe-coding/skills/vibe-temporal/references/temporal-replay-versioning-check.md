# Temporal Replay & Versioning Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected workflow’s replay, Activity effects and state transitions across supported histories and worker versions.

## Context

Identify Temporal server/SDK and worker versions, selected workflow/Activity, histories, task routing, stable effect identity and replay/rollout acceptance criteria.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Replay a curated corpus of old and edge-case histories against the patched worker and fail on nondeterminism or decode incompatibility.
- Interrupt long Activities before/after heartbeat and external side effects; verify retry, cancellation, idempotency, and progress resume.
- Send duplicate/concurrent signals or Updates around initialization and Continue-As-New; verify one legal state transition and response semantics.
- Run old and new worker versions against staged task routing; verify compatibility, poll capacity, rollback, and histories created by each version.
- Grow a representative long-lived history and verify Continue-As-New threshold, state transfer, pending intent, and observability.

## Verification

Compare replay commands, durable workflow state, Activity effects, message handling and history compatibility; qualify mocked Activities separately from worker integration.
