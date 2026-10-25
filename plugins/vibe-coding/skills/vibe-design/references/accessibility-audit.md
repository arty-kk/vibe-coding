# Accessibility Audit

## Goal

Audit reachable accessibility defects in critical user/admin/public paths. Keep only issues supported by repository evidence and observable behavior; do not produce generic WCAG checklists without an owner and affected surface.

## Inspect

Routes/pages, layouts, shared components, forms, modals/drawers/popovers, tables/lists, navigation, toasts/alerts/status regions, media/assets, CSS/theme/tokens, keyboard/focus helpers, i18n/copy, tests, Storybook/previews, accessibility tooling, and generated design docs.

## Issue classes

- Semantics and structure: invalid heading order that hurts comprehension, clickable non-controls, landmark gaps, incorrect list/table/form semantics, and hidden content exposed incorrectly.
- Names and descriptions: missing/incorrect accessible names, vague links/buttons, icon-only controls, unlabeled fields, broken error associations, missing alt/fallback text where needed.
- Keyboard and focus: unreachable controls, focus traps, lost focus after async updates, bad tab order, missing escape/close behavior, disabled action ambiguity, and destructive confirmation traps.
- Status and state announcements: loading/success/error/progress/toast/validation changes that are not perceivable or are announced unsafely.
- Visual accessibility: contrast/token risks, focus indicators, reduced-motion support where existing tokens/patterns support fixes, zoom/overflow issues, and touch target failures.
- Regression resistance: no tests/stories/previews for a critical accessible interaction, stale docs, or shared components that make repeated a11y regressions likely.

## Finding quality

- Include affected user path, expected accessible behavior, acceptance criteria, and validation direction such as keyboard trace, accessibility test, preview, or screenshot.
- Do not report purely theoretical standard violations without reachable product impact.

## Trace and hand off

Reproduce the selected task with its actual entry, state and input method. Follow semantic control/name relationships, focus movement and state announcements alongside rendered presentation. Identify where an actual user cannot perceive, operate or recover the interaction. Pass that state, expected behavior, DOM/component owner and keyboard/semantic/rendered evidence to Improve Accessibility; do not turn every tool warning into an unrelated rewrite.
