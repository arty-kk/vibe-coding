---
name: vibe-recovery
description: "Audit, repair or verify exact release artifacts, rollout/rollback compatibility and backup restoration."
---

# Delivery & recovery

Apply [the working contract](../../references/workflow.md) once; read only the recipe for the requested result.

## Recipes

| Recipe | Operation |
|---|---|
| [Release Artifact Trust Check](references/release-artifact-trust-check.md) | check |
| [Delivery Recovery Audit](references/delivery-recovery-audit.md) | audit |
| [Improve Delivery Recovery](references/delivery-recovery-polish.md) | implement |
| [Delivery Restore & Rollback Check](references/delivery-restore-rollback-check.md) | check |


Use Release Artifact Trust Check for source/build/published-byte identity. Repair of CI trust or dependency execution belongs to [Security](../vibe-security/SKILL.md).
