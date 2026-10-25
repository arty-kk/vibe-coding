# Improve Design System

## Goal

Improve the selected design-system owner: a token family, component family, layout primitive, interaction-state pattern, or documented variant set. The diff should reduce drift across consuming surfaces rather than locally polishing one page.

## Scope selection

- If the user named a component, token, style pattern, Storybook story, or drift issue, improve that owner and directly affected usages.
- If the request is broad, inspect repeated UI patterns and choose the highest-confidence system fix with multiple consuming surfaces or high-risk state coverage.
- Include directly affected usage updates, tests, stories, docs, snapshots, and i18n/copy where the repo expects them.
- Avoid new design languages, broad theming rewrites, dependency changes, and visual redesigns not required by the selected system issue.

## Change targets

- Tokens: semantic names, theme config alignment, repeated values, dark/light/high-contrast variants where existing architecture supports them.
- Components: variant API, state coverage, accessible defaults, responsive behavior, composition boundaries, owner exports, and dead local forks.
- Layout primitives: spacing/density, containers, grids, stacks, headers, sidebars, modals/drawers, and breakpoint behavior.
- Documentation/regression: `DESIGN.md`, component docs, stories, snapshots, visual checks, and examples for important states.
- Migration: update directly affected call sites and remove obsolete local styles only when safe.

## Implementation principles

- Preserve current visual intent while consolidating source of truth.
- Prefer small owner-layer improvements over scattered route-level overrides.
- Keep public component APIs stable unless changing them is necessary and all affected usages are updated.
- Do not hide breaking UI changes behind permissive optional props or silent fallbacks.

## Validation

Run relevant repository-native checks. Use Storybook/preview/screenshot tooling when available; otherwise state the limitation. Verify at least one owner component and one consuming surface when possible.

Fix the selected token, primitive or variant at its maintained owner, update direct consumers and remove superseded overrides only after checking their intended states. Render the owner and a representative consumer with the same data/state/viewport as the failure, then check affected narrow/wide and focus/disabled states. A remaining consumer divergence returns to its owner; accepted rendering/interaction evidence proceeds to Patch Checking. A changed token value alone is not proof that the product now uses it correctly.
