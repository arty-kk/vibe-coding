# Improve Agent Harness

## Goal

Correct the selected agent-run transition, checkpoint or recovery path without repeating committed effects.

## Domain rules

- Make the state machine and commit points explicit before changing retry or parallelism behavior.
- Use stable operation/run/step IDs plus conditional version/fencing checks at every retryable commit boundary.
- Bound fan-out, queues, retries, memory, and context; propagate cancellation and deadlines to children and tools.
- Persist only resume-relevant state and event provenance; redact secrets and treat external observations as data, not instructions.
- Keep approval records and side-effect receipts durable enough to prevent silent re-execution after resume.

## Validation

- Run deterministic state-transition tests with injected crash points before/after side effects and checkpoints.
- Exercise duplicate delivery, stale worker, partial fan-out, child failure, timeout, cancellation, and resume from each durable boundary.
- Verify one terminal result, bounded live work, no orphan tasks, no duplicate protected effect, and replay/trace correlation.

Repair the conditional transition, effect owner or receipt/checkpoint boundary before adjusting retries. Where an external effect cannot enforce a fence, preserve its operation identity and supported deduplication/compensation contract instead of claiming a local lease check prevents all remote work. Replay the same history and feed durable records/effects to the failure check. A remaining mismatch returns to that owner; accepted recovery proceeds to Patch Checking.
