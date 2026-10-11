# Improve Product UI

## Operation

Implement the requested change and verify its directly affected behavior.

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
