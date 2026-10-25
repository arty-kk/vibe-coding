# Temporal Replay & Versioning Check

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

Build a case matrix with history/worker version, injected interruption or message order, expected commands/state/effect count and actual result. Include a compatible old history and the history that exposed the defect. For an incompatible change, verify that routing or patching keeps that history on a compatible path; merely observing a new worker process a newly created workflow is insufficient.

After a repair, carry this evidence to Patch Checking. A replay error, lost in-progress handler or repeated business effect returns a concrete finding to the repair step. Unavailable histories, external-effect observation or mixed-version workers leave the corresponding guarantee unverified; they do not become a clean result through repeated retries.

For handler completion at Continue-As-New, consult the selected SDK's [message-handling guidance](https://docs.temporal.io/handling-messages) and use its supported wait condition.
