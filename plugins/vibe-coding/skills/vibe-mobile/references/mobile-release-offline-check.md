# Mobile Release & Offline Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify one mobile release, navigation, offline/sync, permission, push, or deep-link invariant through bounded simulator/device or repository-native scenarios.

## Context

Identify selected mobile behavior, platform(s), expected state transitions, implementation summary or patch boundary, safe simulator/device environment, fixtures/accounts, and commands.

## Scenarios

- Exercise online happy path and relevant offline/stale/retry/reconnect state.
- Verify navigation/deep link/app link and back-stack behavior where relevant.
- Verify platform permission prompts, secure storage, push/background behavior, or biometrics only when in scope.
- Run build/test/release config checks for the affected platform.
- Confirm analytics/crash/logging behavior if directly affected.
