# Design System Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit the implementation design system: tokens, components, variants, styles, layout primitives, interaction states, documentation, and test/story coverage. Keep only repo-visible issues that make UI work slower, inconsistent, inaccessible, fragile, or visibly divergent.

## Inspect

Theme config, tokens, CSS/Tailwind/styled-system files, shared components, page-level variants, icons/assets, Storybook or component docs, `DESIGN.md`, screenshots/previews, tests/snapshots, forms/tables/modals, layout primitives, i18n/copy patterns, and generated UI artifacts.

## Issue classes

- Token ownership: duplicated hardcoded values, mixed units, drift between theme/config/docs, missing semantic tokens for repeated UI decisions.
- Component variants: inconsistent sizes/states, forked implementations, duplicated patterns, missing disabled/loading/error/focus/destructive variants.
- Style architecture: ad-hoc CSS, one-off Tailwind/class soup where a component owner exists, conflicting responsive patterns, fragile specificity, and style leakage.
- Accessibility baked into system: shared components missing accessible names, focus handling, keyboard support, status announcements, contrast-friendly variants, or semantic defaults.
- Documentation and regression resistance: stale `DESIGN.md`, missing stories/examples for core variants, fragile snapshots, no visual/test coverage for shared components.
- Implementation drift: public surfaces bypass the system, docs promise unavailable variants, or owner components do not match actual route usage.

## Finding quality

- Include expected system behavior, affected surfaces, acceptance criteria, and validation direction including preview/story/screenshot when available.
- Do not report taste-only preferences without system consistency, accessibility, maintainability, or user-impact evidence.
