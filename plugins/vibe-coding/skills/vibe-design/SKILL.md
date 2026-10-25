---
name: vibe-design
description: "Audit or repair repository design-system and accessibility behavior: tokens, components, responsive layout, semantics, keyboard and focus."
---

# Design & accessibility

Apply [the working contract](../../references/workflow.md) once.

## Workflows

- **Accessible task completion:** Accessibility Audit → Improve Accessibility → keyboard, semantic/name/state and rendered checks → [Patch Checking](../vibe-review/references/patch-checking.md).
- **Shared visual/interaction consistency:** Design System Audit → Improve Design System → verify the owner variant and actual consumers across affected states/viewports → Patch Checking.

Choose by the violated contract: an unusable keyboard/focus/name relationship belongs to the accessible interaction, while repeated token/variant/layout drift belongs to its shared owner. A known defect starts at correction; an audit-only request reports findings without editing.

Carry a reachable state, expected interaction/visual rule, source owner and rendered evidence into repair. Prefer a shared correction when the same rule governs several consumers; a genuinely local requirement does not need a new global token or component.

After correction, replay the failing interaction and a normal control. A screenshot cannot establish keyboard or screen-reader behavior, and an accessibility-tree check cannot establish visual equivalence. Return failed states to their owner, then finish the resulting patch through repeated Patch Checking; retain unavailable renderer/device evidence as a limitation.

## Recipes

| Recipe | Operation |
|---|---|
| [Accessibility Audit](references/accessibility-audit.md) | audit |
| [Improve Accessibility](references/accessibility-polish.md) | implement |
| [Design System Audit](references/design-system-audit.md) | audit |
| [Improve Design System](references/design-system-polish.md) | implement |
