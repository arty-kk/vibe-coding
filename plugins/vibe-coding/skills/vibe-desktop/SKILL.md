---
name: vibe-desktop
description: "Audit, repair or verify browser-extension or desktop-app permissions, IPC, local data, update and packaging behavior."
---

# Desktop & extensions

Apply [the working contract](../../references/workflow.md) once. Identify the real process/origin and permission boundary before changing a UI symptom.

## Workflows

- **Extension:** Browser Extension Audit → Improve Browser Extension → Local Client Runtime Security Check for affected permission/message/storage/lifecycle guarantees → [Patch Checking](../vibe-review/references/patch-checking.md).
- **Desktop app:** Desktop App Audit → Improve Desktop App → the local-runtime check for affected IPC/OS/file/update guarantees → Patch Checking.

A known bug starts at its repair prompt; verification-only work starts at the check. Pass the actual browser/platform/build mode, sender/origin, requested operation, permission state and local data/effect into correction.

Replay a permitted control and a denied/malformed request at the real content/background/native or renderer/main boundary. Observe the file/data/OS effect separately from the returned message, then exercise the selected reload/restart/update state. A failed boundary returns to its owning validation or lifecycle code, not a permissive UI workaround.

Finish with supported runtime behavior and a clean patch review. Missing signing/store/platform evidence remains a distribution-specific gate. Use synthetic local data and an appropriate test profile/environment; code changes alone do not authorize broader host/OS access or destructive changes to a personal profile.

## Recipes

| Recipe | Operation |
|---|---|
| [Browser Extension Audit](references/browser-extension-audit.md) | audit |
| [Improve Browser Extension](references/browser-extension-polish.md) | implement |
| [Desktop App Audit](references/desktop-app-audit.md) | audit |
| [Improve Desktop App](references/desktop-app-polish.md) | implement |
| [Local Client Runtime Security Check](references/local-client-runtime-security-check.md) | check |
