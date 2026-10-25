# Mobile App Audit

## Goal and scope

Audit one mobile app feature, navigation flow, offline/sync path, permission boundary, deep link, push notification, release config, or platform-specific behavior for iOS/Android or cross-platform mobile apps.

## Domain invariants

- Mobile UI states, navigation, deep links, offline/cache behavior, and backend contracts agree.
- Platform permissions, secure storage, push tokens, biometrics, app links, background tasks, and privacy prompts are correctly owned.
- Sync, retry, conflict resolution, and stale local state are explicit for the selected feature.
- Accessibility, responsive device states, error recovery, crash reporting, analytics, and release channels are covered where relevant.
- Tests or manual device/simulator gates prove the selected mobile behavior.

## Audit method

Trace the selected mobile flow from entry/deep link through navigation, local storage/cache, API calls, permissions, background tasks, push/deeplink handling, analytics/crash logs, tests, and store/release config.

Choose a concrete platform, initial account/local state and entry event. Follow navigation and operation identity through interruption/offline/restart to the server and resumed screen. Distinguish a local UI success from acknowledged durable state. Pass the failing state sequence, platform/build and expected consumer outcome into Improve Mobile App; a broad platform rewrite is not a substitute for locating that owner.
