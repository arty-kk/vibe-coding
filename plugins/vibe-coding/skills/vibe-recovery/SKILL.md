---
name: vibe-recovery
description: "Audit, repair or verify exact release artifacts, rollout/rollback compatibility and backup restoration."
---

# Delivery & recovery

Apply [the working contract](../../references/workflow.md) once.

## Workflows

- **Inspect or repair delivery/recovery:** Delivery Recovery Audit → Improve Delivery Recovery → Delivery Restore & Rollback Check → [Patch Checking](../vibe-review/references/patch-checking.md) for changed source/configuration.
- **Verify release bytes/identity:** Release Artifact Trust Check directly on the exact candidate and authorized publication/promotion evidence. Route a broken build trust boundary to Security or the owning delivery repair; do not mutate release state during inspection.

Carry source/build/artifact/configuration identities, current data/schema compatibility, backup/restore point and agreed recovery criteria between prompts. A known failing procedure can start at correction; a check-only request performs only the authorized rehearsal/inspection.

Compare actual published/promoted bytes and application state rather than substituting one green build or backup job for the whole chain. Failed identity, compatibility or restore behavior returns to its owning procedure/source, followed by the same check and patch re-review.

Finish at the requested, evidenced delivery/recovery stage. A checksum is not builder authorization, binary rollback is not data rollback, and an unexercised RPO/RTO remains a gate. Restores, failover and production promotion require their own suitable authorized environment.

## Recipes

| Recipe | Operation |
|---|---|
| [Release Artifact Trust Check](references/release-artifact-trust-check.md) | check |
| [Delivery Recovery Audit](references/delivery-recovery-audit.md) | audit |
| [Improve Delivery Recovery](references/delivery-recovery-polish.md) | implement |
| [Delivery Restore & Rollback Check](references/delivery-restore-rollback-check.md) | check |


Use Release Artifact Trust Check for source/build/published-byte identity. Repair of CI trust or dependency execution belongs to [Security](../vibe-security/SKILL.md).
