# Kubernetes Rollout & Failure Check

## Goal

Verify the selected workload’s rendered contract, availability or state recovery during its required lifecycle transitions.

## Context

Identify target overlay/chart and cluster version, workload identity, probe/termination settings, availability budget, stateful dependencies and authorized test environment.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Render and validate the exact overlay; reject selector, port, reference, schema, or policy mismatches.
- Hold a dependency unavailable during startup and verify startup/readiness behavior without liveness restart amplification.
- Send traffic during rollout and SIGTERM; verify drain, availability budget, progress deadline, and rollback signal.
- Test voluntary eviction through its supported mechanism separately from involuntary pod/node loss; inspect the relevant budget, rescheduling, volume attach and state recovery.
- Drive representative saturation and verify requests, limits, HPA signal, stabilization, backlog, and overload response.

## Verification

Compare the rendered resources, readiness/endpoints, accepted traffic, rollout progress, drained work and state recovery against the selected workload promise.

## Execute and decide

Record the exact rendered artifact, target API version, namespace/workload identity and expected availability/drain/state criteria. Validate selectors, ports and references, then establish healthy endpoints and a normal request/state control in the authorized cluster when runtime evidence is required.

Introduce only the selected startup, dependency, termination, rollout or disruption condition. Observe actual accepted traffic, readiness/endpoints, progress/events, unfinished work and persisted state through recovery. PDB behavior applies to the relevant eviction path; it does not prevent involuntary loss or replace a workload controller's rollout policy.

Return passed, failed or blocked for the stated transition and environment. Feed a failure to the owning chart/operator/resource repair, repeat its transition/control after correction and finish Patch Checking for source changes. Without a suitable cluster, report the render/policy checks actually performed and the missing runtime gate.
