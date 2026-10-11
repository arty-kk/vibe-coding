# Kubernetes Rollout & Failure Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected workload’s rendered contract, availability or state recovery during its required lifecycle transitions.

## Context

Identify target overlay/chart and cluster version, workload identity, probe/termination settings, availability budget, stateful dependencies and authorized test environment.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Render and validate the exact overlay; reject selector, port, reference, schema, or policy mismatches.
- Hold a dependency unavailable during startup and verify startup/readiness behavior without liveness restart amplification.
- Send traffic during rollout and SIGTERM; verify drain, availability budget, progress deadline, and rollback signal.
- Simulate pod/node loss within a safe test cluster and verify PDB, rescheduling, volume attach, and state recovery.
- Drive representative saturation and verify requests, limits, HPA signal, stabilization, backlog, and overload response.

## Verification

Compare the rendered resources, readiness/endpoints, accepted traffic, rollout progress, drained work and state recovery against the selected workload promise.
