# Visual Regression Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected rendered change against accepted behavior and visual references for supported states and viewports.

## Context

Identify the selected change, affected routes/components/states, supported browsers/viewports and existing visual references. Use the project’s rendering and test tools.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Render loading, empty, error, success, validation, disabled, permission, long-content, localization, reduced-motion, and dark/high-contrast states when applicable.
- Compare responsive layout, overflow, focus order/visibility, keyboard interaction, semantic/accessibility tree, and pointer/touch targets.
- Use deterministic data, fonts/assets, animation disabling, stable viewport, and documented screenshot masks only for proven nondeterminism.
- Review baseline changes semantically; never bulk-accept screenshots to make the suite green.
- Correlate visual diffs with DOM/style/component changes and run interaction/a11y assertions for behavior that pixels cannot prove.

## Verification

Report actual rendered differences and interaction results; identify any missing renderer or baseline. A code-only inspection cannot establish visual equivalence.
