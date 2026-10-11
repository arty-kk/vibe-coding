# Improve Mobile App

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected mobile flow across navigation, local state, backend behavior and relevant platform constraints.

## Scope selection

Use the selected mobile feature, platform bug, deep link, push notification, offline issue, release failure, audit finding, or failing test. Do not rewrite navigation or state management globally unless required by the selected fix.

## Change targets

- Screens/components, navigation params, deep links/app links, loading/empty/error/offline states, and accessibility.
- Local storage/cache, sync, conflict resolution, retry/backoff, and stale-state recovery.
- API/generated clients, auth/session refresh, secure storage, platform permissions, push tokens, background tasks.
- Tests, simulator/device scripts, crash/analytics instrumentation, release config, and docs/maps directly affected.

## Implementation principles

- Preserve platform conventions and existing app architecture.
- Keep sensitive data in secure storage when available and avoid leaking tokens/log payloads.
- Validate both online and offline paths when the selected feature supports offline behavior.
- Avoid broad dependency upgrades or app-store metadata rewrites outside scope.

## Validation

Run repository-native mobile tests, type checks, builds, simulator/device scenarios, deep-link checks, offline/sync scenarios, or release config checks relevant to the selected boundary. Report unavailable devices/accounts/store gates honestly.
