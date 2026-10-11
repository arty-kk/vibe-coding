# UI/UX Bug Probe

## Scope

Inspect one reachable presentation or accessible-interaction failure at a supported state/viewport. Use the project’s tokens, components and design references. Wrong data or state must be corrected at its behavioral owner, not hidden with CSS.

## Procedure

1. Capture the affected rendered state where tools permit. Check clipping/overflow, overlapping controls, readable content, keyboard/focus and accessible names or error relationships.
2. Trace the failure to its component, shared primitive, theme/token or stylesheet. Establish the expected behavior; aesthetic preference alone is not a defect.
3. If authorized, correct the defining rule and affected usages. Use existing tokens and breakpoints where they fit; add a value at the appropriate local or shared owner only when the required behavior needs it.
4. Preserve product behavior and unrelated visual intent. A markup, composition or copy correction is allowed when it is necessary for the demonstrated accessible interaction.

## Verification

Replay the failing viewport/state and a nearby normal state; exercise keyboard behavior when affected. Check generated styles and component/visual tests where available. Computed contrast or layout arithmetic is source evidence; report missing renderer/baseline rather than claiming visual equivalence. Apply the selection/history and result rules in the parent skill.
