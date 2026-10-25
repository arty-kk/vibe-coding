# Improve Feature Flags Rollout

## Goal

Correct the selected flag or rollout behavior across targeting, enforcement, fallback and directly affected consumers.

## Scope selection

Use the selected flag, rollout bug, stale flag, audit finding, failing test, experiment issue, or explicit release task. Do not migrate flag providers or redesign experimentation globally unless required by the selected fix.

## Change targets

- Flag definition/defaults, environment config, targeting, dependencies, and kill-switch behavior.
- Backend gates, UI visibility, API/jobs, paid/security boundaries, and no-access states.
- Analytics exposure/enrollment events and experiment consistency when relevant.
- Tests/fixtures for on/off, targeted/untargeted, rollback, missing-provider, and stale-flag states.
- Docs/maps and removal cleanup for the selected flag.

## Implementation principles

- Make off state safe and preserve existing behavior for untargeted users.
- Keep sensitive entitlement decisions server-side.
- Avoid leaving permanent flag complexity unless the product/repo requires it.
- Keep rollout/rollback and observability explicit.

## Validation

Run repository-native tests and targeted scenarios for flag on/off, missing config/provider, targeted user, wrong plan/role, rollback/kill switch, and analytics exposure where relevant.

Correct the definition, context construction, enforcement, exposure or cleanup owner that violates the selected policy. Preserve the intended fallback instead of choosing fail-open/fail-closed from convention alone. Feed the candidate, targeting fixtures and on→off state into the exposure/rollback check. Recheck failures at that boundary, then run Patch Checking; changing a live rollout or deleting a shared flag still requires the corresponding authorized environment/action.
