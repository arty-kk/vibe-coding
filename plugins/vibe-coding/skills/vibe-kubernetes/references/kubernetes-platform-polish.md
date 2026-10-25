# Improve Kubernetes Platform

## Goal

Correct the selected rendered workload or rollout behavior for its actual environment and dependent resources.

## Domain rules

- Modify the environment's actual source of truth—chart, kustomization, operator CR, or manifest—not a generated copy unless generation is authoritative.
- Separate startup, readiness, and liveness intent; preserve graceful drain and allow enough termination time for the measured shutdown path.
- Keep selectors immutable-compatible and coordinate service, policy, autoscaling, disruption, and workload changes as one rollout slice.
- Use least-privilege RBAC and pod security settings; do not solve connectivity by removing policies or granting cluster-wide permissions.
- For risky schema/state changes, use a staged rollout and explicit rollback/forward-fix condition rather than assuming Deployment rollback restores data compatibility.

## Validation

- Run repository-native render/schema/policy checks and inspect the complete rendered delta for the target environment.
- Where a cluster is available and access is authorized, use suitable dry-run/diff checks and observed rollout, endpoint, event and metric evidence. An actual apply is a separate authorized mutation.
- Test startup delay, dependency unavailability, SIGTERM/drain, unavailable replica, node disruption, and rollback compatibility as applicable.

Correct the maintained target source and render the complete affected resource set before runtime verification. Preserve selector/reference consistency and the actual rollout/data transition; Deployment rollback does not restore incompatible data by itself. Feed the rendered candidate and selected availability/recovery scenario to the rollout check, repair failures at their owner and finish Patch Checking once supported.
