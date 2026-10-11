# Improve Temporal Workflows

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected Temporal workflow or Activity behavior while preserving replay and worker-version compatibility.

## Domain rules

- Keep Workflow code deterministic and move external I/O/side effects into Activities with stable idempotency keys.
- Use explicit timeout/retry/heartbeat/cancellation settings per Activity behavior; do not use retries for permanent business rejection.
- Introduce compatible workflow changes with the repository's supported patching or worker-versioning pattern and retain old branches until histories are safe.
- Bound history with Continue-As-New while transferring only durable workflow state and accounting for pending signals/updates.
- Deploy task-queue/build changes in a staged sequence with replay evidence and an explicit rollback/forward-fix policy.

## Validation

- Run workflow unit tests with deterministic time and Activity mocks only for logic, plus integration tests for worker/task-queue behavior.
- Replay representative captured histories, including old versions and edge cases, against candidate workflow code.
- Exercise Activity timeout/heartbeat/cancel/retry, worker loss, signal/update concurrency, Continue-As-New, and mixed-version deployment where feasible.
