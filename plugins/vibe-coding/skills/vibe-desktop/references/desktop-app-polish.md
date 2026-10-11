# Improve Desktop App

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Fix the selected desktop app boundary across UI/native layers, IPC, local storage/files, backend integration, tests, and packaging/release config when directly affected.

## Scope selection

Use the selected desktop feature, OS integration, local data issue, auto-update problem, audit finding, failing test, or packaging failure. Do not rewrite the app shell or update system unless required by the selected fix.

## Change targets

- Renderer/main/native process boundaries, IPC payload validation, OS permission requests, notifications, tray/menu/deep-link behavior.
- Local storage, secrets, file access, cache, logs, crash reports, offline/sync, migrations, and cleanup.
- Backend API integration, auth/session refresh, tests/manual scripts, packaging/signing/notarization config, docs/maps directly affected.

## Implementation principles

- Validate all cross-process and external inputs.
- Protect tokens/secrets and avoid logging sensitive local data.
- Preserve platform compatibility and existing update/migration paths.
- Keep release and rollback gates explicit.

## Validation

Run repository-native tests/builds and bounded manual/platform scenarios for the selected behavior, including offline/restart/update/permission states when relevant. Report unavailable signing/store/platform gates honestly.
