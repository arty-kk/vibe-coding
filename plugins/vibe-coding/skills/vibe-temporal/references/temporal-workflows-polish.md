# Improve Temporal Workflows

## Goal

Correct the selected Temporal workflow or Activity behavior while preserving replay and worker-version compatibility.

## Domain rules

- Keep Workflow code deterministic and move external I/O/side effects into Activities with stable idempotency keys.
- Use explicit timeout/retry/heartbeat/cancellation settings per Activity behavior; do not use retries for permanent business rejection.
- Introduce compatible workflow changes with the repository's supported patching or worker-versioning pattern and retain old branches until histories are safe.
- Bound history with Continue-As-New while transferring only durable workflow state and accounting for pending signals/updates.
- Deploy task-queue/build changes in a staged sequence with replay evidence and an explicit rollback/forward-fix policy.

## Repair sequence

1. Reproduce the failing history or Activity/message interleaving and record the expected durable state and external effect count.
2. Change the owner of the defect. Preserve old command behavior through the SDK's supported compatibility mechanism; keep network access outside Workflow execution. For ambiguous Activity success, reconcile or deduplicate the operation before retrying the effect.
3. For Continue-As-New, transfer the required state and pending intent and finish in-progress handlers at the SDK-supported boundary. Check whether message deduplication must span runs rather than assuming a new run inherits it.
4. Replay the affected history corpus and exercise the changed Activity or handler with an appropriate worker integration. A mock that always succeeds cannot verify a lost heartbeat, duplicate external effect or task-routing failure.

## Handoff

Give the check step the original failing case, old/new worker identities, changed compatibility branch, effect identity and observed results. Record deployment actions separately from the patch; perform them only within the authorized rollout scope. Pass the complete resulting patch and any unverified cases to Patch Checking.

## Validation

- Run workflow unit tests with deterministic time and Activity mocks only for logic, plus integration tests for worker/task-queue behavior.
- Replay representative captured histories, including old versions and edge cases, against candidate workflow code.
- Exercise Activity timeout/heartbeat/cancel/retry, worker loss, signal/update concurrency, Continue-As-New, and mixed-version deployment where feasible.
