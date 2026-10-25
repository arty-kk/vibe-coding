# Go Rust Concurrency & Shutdown Check

## Goal

Verify the selected service’s cancellation, task ownership, resource bound or shutdown guarantee.

## Context

Identify language/toolchain, selected service/task, spawn and cancellation owner, resource/deadline limits, expected effect and configured shutdown behavior.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Cancel callers at relevant wait, I/O and commit boundaries and verify child work, locks, connections, and side effects terminate consistently.
- Saturate admission and downstream pools; verify bounded queue/task growth, fairness, timeout budget, and recovery.
- Inject connection resets and slow responses; verify pool reuse, retry eligibility, deadline propagation, and no retry storm.
- Send SIGTERM during idle, active request, streaming, and background work; verify readiness, drain/cancel, telemetry, and forced-deadline behavior.
- Run race/leak/deadlock instrumentation supported by the repository and inspect before/after task/goroutine counts.

## Verification

Compare final effect/state, live tasks or goroutines, held resources, admission/recovery and shutdown deadline for the exercised path.

## Execute and decide

Establish a normal request and steady resource baseline with the actual runtime. Use controlled barriers or an existing failure harness to hold the selected child/I/O/commit boundary, then trigger caller cancellation, saturation or the supported shutdown signal.

Observe response/ack, child completion, committed effects, queued work, held locks/connections and readiness until the stated deadline. Compare retained resources with the intended pool/lifecycle policy rather than demanding every count become zero. Use race/leak instrumentation only where supported, alongside the actual interleaving.

Return passed, failed or blocked for the selected guarantee with event order and observed effects/resources. Pass a failure to the authorized lifecycle repair, rerun its sequence/control after correction and finish Patch Checking for changed code. Process termination and load tests need a suitable isolated environment.
