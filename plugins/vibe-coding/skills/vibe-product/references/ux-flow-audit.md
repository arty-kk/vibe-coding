# UX Flow Audit

## Goal

Audit an end-to-end user/admin/system flow from entry point to completion, including permissions, state transitions, copy, recovery, and post-action feedback. Keep only issues that affect task completion, safety, clarity, conversion, or regression resistance.

## Inspect

Routes, navigation, guards, onboarding, forms, tables, dialogs, loaders/actions, API hooks, state stores, RBAC/plan/tenant rules, redirects, async jobs, notifications/toasts/emails, empty/loading/error/disabled/no-access states, analytics, i18n/copy, tests, docs, and generated navigation maps.

## Issue classes

- Flow continuity: broken entry/exit paths, lost state, wrong redirects, dead ends, missing next step, and unclear success/after-action behavior.
- Decision clarity: CTAs, labels, helper text, progress, destructive confirmations, plan/permission explanations, and recovery options that mislead users.
- State transitions: loading/pending/optimistic/partial-success/retry/error states that contradict backend or leave the user unsure.
- Permissions and context: visible actions not matching allowed actions, tenant/workspace/project context confusion, stale selected entity, and no-access/no-plan/over-quota states.
- Forms and validation: field order, required/optional ambiguity, validation timing, inline vs summary errors, disabled submit rules, and persisted draft behavior when present.
- Measurement and regression: missing tests/analytics hooks for critical funnel steps where repo patterns require them, stale nav maps, or shallow smoke coverage.

## Finding quality

- Include actor, starting context, completion goal, expected result, acceptance criteria, and validation path.
- Do not report cosmetic preferences unless they affect comprehension, safety, conversion, accessibility, permissions, or task completion.

## Handoff

Choose the actor's start context and accepted completion/recovery state, then trace actual navigation, action commits and feedback. Record the first dead end, lost state, contradictory decision or missing recovery path, with the governing source. Feed that bounded journey and failing transition into Improve UX Flow; do not infer a measured conversion effect from a usability observation alone.
