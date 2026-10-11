# Feature Flag Exposure & Rollback Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify one feature flag or rollout invariant through bounded on/off, targeted, rollback, missing-provider, and exposure-measurement scenarios.

## Context

Identify flag name, expected targeting/default/rollback behavior, implementation summary or patch boundary, safe environment, fixtures/accounts, and repository-native commands.

## Scenarios

- Verify default/off state and targeted/on state.
- Verify backend enforcement and UI visibility agree.
- Exercise rollback/kill switch and missing flag-provider/config behavior.
- Verify plan/role/tenant restrictions and analytics exposure/enrollment events where relevant.
- Check stale flag cleanup only if the selected task includes removal.
