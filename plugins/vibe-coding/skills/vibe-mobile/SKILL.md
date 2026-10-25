---
name: vibe-mobile
description: "Audit, repair or verify mobile navigation, offline/sync, permissions, local data, deep links and release configuration."
---

# Mobile apps

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Mobile App Audit → Improve Mobile App → Mobile Release & Offline Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry the platform/build mode, entry/deep link, account/permission state, local data version and expected navigation/sync outcome into correction. A known mobile defect starts at implementation; a verification-only request does not change product code or store settings.

Trace the first mismatch between navigation, local queue/cache, server state and OS lifecycle. Correct that owner, then replay the same cold/warm, online/offline or permission transition with a normal control. Preserve the accepted conflict policy; reconnect is not proof that queued work or duplicate effects converged.

A failed device state returns to its owner, followed by the relevant simulator/device check and final patch review. Keep unavailable physical-device, push, signing and store evidence distinct from a successful development build. Offline support is tested where the feature promises it, not invented as an unrelated requirement.

## Recipes

| Recipe | Operation |
|---|---|
| [Mobile App Audit](references/mobile-app-audit.md) | audit |
| [Improve Mobile App](references/mobile-app-polish.md) | implement |
| [Mobile Release & Offline Check](references/mobile-release-offline-check.md) | check |
