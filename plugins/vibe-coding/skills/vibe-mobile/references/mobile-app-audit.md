# Mobile App Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

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
