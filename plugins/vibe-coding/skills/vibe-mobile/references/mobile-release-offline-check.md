# Mobile Release & Offline Check

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

## Execute and decide

Record the actual platform/build mode, synthetic account/data, permission state and expected route/back stack or local/server result. Establish normal online behavior, then introduce the selected offline, interruption, permission denial, background or cold-start/deep-link event.

Observe queued operation identities, local persistence, server effects and the resumed screen after recovery. Test a duplicate/retry or conflict only when it is part of the selected sync guarantee, using the product's stated resolution policy. A visually successful screen cannot conceal a lost or repeated operation.

Return passed, failed or blocked with the state/event sequence and environment actually exercised. Pass failures to the authorized owner repair, repeat their control/transition after correction and finish Patch Checking for changed files. Use synthetic notifications/test devices; code verification does not authorize contacting real recipients or publishing to a store.
