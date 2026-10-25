# Feature Flag Exposure & Rollback Check

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

## Execute and decide

Record the flag/environment, current values, trusted principal/tenant attributes and expected default/provider-failure behavior. Establish targeted and untargeted controls, then exercise the selected backend/UI path and inspect actual feature effects.

Enable the feature in the test environment, create representative state, disable/kill it and observe how current and required old/off consumers behave. Simulate the selected provider/config failure and inspect fallback/cache behavior. Verify exposure at actual treatment delivery and keep assignment/enrollment distinct.

Return passed, failed or blocked with context, transitions and observed effects/events. Feed failures into the owning repair, repeat the failed case/control and finish Patch Checking after code changes. Do not mark rollback passed from the flag value alone.
