# Improve Kubernetes Platform

## Operation

Implement the requested change and verify its directly affected behavior.

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
- Where a cluster is available, use dry-run/apply diff plus rollout, endpoint, event, and metrics evidence without destructive production experiments.
- Test startup delay, dependency unavailability, SIGTERM/drain, unavailable replica, node disruption, and rollback compatibility as applicable.
