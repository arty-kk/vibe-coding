# Improve Product UI

## Goal

Correct the selected user interaction across state, data, permissions and directly affected rendered states.

## Domain rules

- Fix the owning data/action contract before adding component-local conditionals.
- Keep async state explicit; cancel or ignore stale work and prevent duplicate destructive effects.
- Reuse the existing design system, accessibility patterns, copy, localization, and analytics conventions.
- Update only directly affected states and consumers; avoid route-wide redesign without evidence.

## Validation

- Run affected type/build/component/e2e/accessibility checks.
- Inspect representative desktop/mobile states, keyboard/focus flow, slow/error/retry, and auth/plan boundaries.
- Capture preview/screenshot evidence when tooling exists and list browsers/devices not exercised.

Correct the owning action/data/state rule and update its direct rendering/accessibility consumers. Replay the original event order with a normal interaction, inspect durable effects and verify the failed visible/keyboard state. Pass selected acceptance into its check, return remaining failures to the same owner and finish Patch Checking. An optimistic success state alone cannot close the workflow.
