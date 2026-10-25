---
name: vibe-product
description: "Audit, implement or verify a selected requirement, user journey, onboarding, form or data interface."
---

# Product & UX

Apply [the working contract](../../references/workflow.md) once. Choose the user outcome and owning state/decision before treating the problem as visual polish.

## Workflows

| Outcome | Prompt chain |
|---|---|
| Align an accepted requirement | Product Requirements Audit → Improve Product Requirements → Product Acceptance Check |
| Verify a product decision/event/metric | requirements or analytics evidence → Product Decision & Metrics Check; return failures to their decision/implementation owner |
| Correct a route/component interaction | Product UI Audit → Improve Product UI → Product Acceptance Check for the selected state/actor |
| Correct a form/table operation | Form & Data UI Audit → Improve Form & Data UI → input/request/persisted-result acceptance |
| Complete a multi-step journey | UX Flow Audit → Improve UX Flow → entry → completion/recovery acceptance |
| Reach first meaningful value | Onboarding Activation Audit → Improve Onboarding Activation → first-run/returning-user and partial-setup acceptance |

Start at implementation when the requirement/defect and owner are known. Verification-only work starts at the appropriate check; an audit-only request ends with findings. Carry actor, initial role/plan/tenant/state, trigger, accepted outcome and a distinguishing failure case between prompts.

After repair, replay the same path and its relevant denial/recovery control. Inspect server/persisted effects independently of optimistic UI and inspect rendered/keyboard behavior where affected. Failed acceptance returns to that state or contract owner; then repeat the affected check and [Patch Checking](../vibe-review/references/patch-checking.md) on the resulting patch until clean or blocked.

Do not change an accepted product decision to fit implementation or invent conversion/activation success from code alone. Missing product, measurement or device evidence stays explicit.

## Recipes

| Recipe | Operation |
|---|---|
| [Form & Data UI Audit](references/form-data-ui-audit.md) | audit |
| [Improve Form & Data UI](references/form-data-ui-polish.md) | implement |
| [Onboarding Activation Audit](references/onboarding-activation-audit.md) | audit |
| [Improve Onboarding Activation](references/onboarding-activation-polish.md) | implement |
| [Product Acceptance Check](references/product-acceptance-check.md) | check |
| [Product Decision & Metrics Check](references/product-decision-metrics-check.md) | check |
| [Product Requirements Audit](references/product-requirements-audit.md) | audit |
| [Improve Product Requirements](references/product-requirements-polish.md) | implement |
| [Product UI Audit](references/product-ui-audit.md) | audit |
| [Improve Product UI](references/product-ui-polish.md) | implement |
| [UX Flow Audit](references/ux-flow-audit.md) | audit |
| [Improve UX Flow](references/ux-flow-polish.md) | implement |
