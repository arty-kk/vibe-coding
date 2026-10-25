# Desktop App Audit

## Goal and scope

Audit one desktop app boundary such as local storage, auto-update, IPC, native shell access, offline sync, file system permissions, notifications, packaging, or backend integration.

## Domain invariants

- Renderer/UI, main process/native layer, local storage, backend API, and OS permissions have explicit trust boundaries.
- Local secrets, tokens, files, logs, caches, and crash reports are protected.
- Auto-update, migrations, offline/sync, file access, notifications, and background tasks have defined failure/recovery behavior.
- Packaging/signing/notarization/release config matches the affected platform.
- Tests/manual checks cover the selected desktop behavior and supported platforms where relevant.

## Audit method

Trace the selected desktop flow through UI/renderer, main/native process, IPC/message validation, local storage/files, OS integrations, backend calls, update/packaging config, logs, tests, and release scripts.

Follow an operation from its caller identity through IPC/OS permission checks into the actual file, secret, process or sync effect. Compare allowed and denied inputs and inspect persisted state across the selected restart/update boundary. Pass the failing boundary, build/platform identity, initial local state and expected effect to Improve Desktop App; a successful renderer response is not proof of a completed durable operation.
