# Improve Accessibility

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Improve the selected accessible path or shared accessible component behavior. The diff should make the selected interaction perceivable, operable, understandable, and regression-resistant without introducing speculative abstractions.

## Scope selection

- If the user named a route, component, form, modal, table, keyboard issue, screen-reader issue, or accessibility audit task brief, improve that owner and directly affected states.
- If the request is broad, inspect primary flows and select the highest-confidence accessibility fix with meaningful task-completion or safety impact.
- Include related labels, validation, focus management, state announcements, tests, docs, and stories when they belong to the same accessibility defect.
- Avoid visual redesigns, unrelated copy rewrites, dependency changes, and broad framework changes unless the accessibility fix requires them.

## Change targets

- Semantic HTML first; ARIA only when semantics do not express the interaction.
- Accessible names/descriptions for controls, links, fields, icons, dialogs, tables, filters, and destructive actions.
- Keyboard reachability, tab order, focus visible state, focus return, escape/close behavior, and modal/popover traps.
- Form validation associations, inline errors, summary errors, helper text, required/optional clarity, and server error recovery.
- Live/status announcements for async updates, toasts, progress, loading, partial success, and error states.
- Directly affected tests, accessibility checks, stories, snapshots, and docs when the repo uses them.

## Implementation principles

- Reuse existing accessible components, hooks, helpers, tokens, and test patterns.
- Fix the shared owner when the same accessibility defect appears across surfaces.
- Preserve visible behavior unless a visible change is needed for accessibility.
- Do not suppress lint/a11y warnings without a specific repo-compatible rationale.

## Validation

Run relevant repository-native checks. When possible, perform a keyboard trace for the changed path and use preview/accessibility tooling. State any screen-reader or browser limitations plainly.
