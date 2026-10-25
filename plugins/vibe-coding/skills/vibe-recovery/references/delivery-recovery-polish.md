# Improve Delivery Recovery

## Goal

Correct the selected release, rollback or restore path and verify artifact identity and application-level recovery.

## Domain rules

- Preserve exact tested artifact identity through promotion and rollback. For required environment-specific builds, record the inputs and verify each resulting artifact.
- Keep release gates deterministic and least-privilege; invalidate or segregate caches/artifacts when trust or inputs change.
- Stage rollout with explicit health/abort criteria and compatibility order; use flags only as owned temporary controls.
- Coordinate schema/data changes with rollback reality and document forward-fix/restore when binary rollback cannot restore correctness.
- Repair the selected restore procedure and verify integrity/application behavior in an authorized isolated environment. Protect backups from production credential and failure-domain loss.

## Validation

- Run CI/build tests from clean inputs where supported and verify artifact digest/provenance/manifest linkage.
- Exercise staged rollout/abort/rollback or a faithful rehearsal, including config/flag and schema compatibility.
- Restore representative backups into an isolated environment and verify integrity, application behavior, observed RPO/RTO, and operator runbook.

Correct the owning build/promotion, compatibility transition or restore procedure while preserving the original candidate/state identities. Rehearse the selected failure and recovery in the authorized environment, then feed actual artifact, restored data and timing evidence into the restore/rollback check. Return failed links to their owner before Patch Checking. Preserve old recoverable artifacts and evidence; cleanup is not a substitute for reconciliation.
