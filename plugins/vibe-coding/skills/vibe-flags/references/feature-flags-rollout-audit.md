# Feature Flags Rollout Audit

## Goal and scope

Audit one feature flag, rollout control, experiment gate, kill switch, environment flag, or gradual-release boundary for consistency, safety, ownership, and cleanup.

## Domain invariants

- Flag owner, default, environment behavior, target audience, dependencies, and removal plan are explicit.
- Backend enforcement, UI visibility, analytics, docs, tests, and rollout gates agree.
- Off state and rollback/kill-switch behavior are safe and tested for the selected feature.
- Stale flags, conflicting experiments, and environment drift do not create unreachable or unsafe behavior.
- Sensitive or paid features are not unlocked by client-only flags.

## Audit method

Trace the selected flag from definition/config/provider through server checks, client checks, API behavior, jobs, analytics, tests, deployment, docs, and cleanup references.

Select a targeted and untargeted principal plus the actual default/degraded-provider policy. Follow evaluation identity into feature effects and the point where exposure is emitted. Inspect state created while enabled and what old/off consumers do with it. Pass the failed context/evaluation/transition and expected behavior to Improve Feature Flags Rollout rather than assuming that flipping the boolean alone restores safety.
