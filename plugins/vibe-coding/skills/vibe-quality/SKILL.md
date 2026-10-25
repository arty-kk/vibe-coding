---
name: vibe-quality
description: "Audit test coverage or release readiness, repair a test harness, or verify rendered visual changes."
---

# Quality & readiness

Apply [the working contract](../../references/workflow.md) once. Choose the lane by the evidence the user needs.

## Workflows

- **Find meaningful test gaps:** Test Coverage Audit → Improve Test Harness for an authorized, selected gap → exercise the original behavior/counterexample and a valid control → [Patch Checking](../vibe-review/references/patch-checking.md). Carry the behavior owner and observable assertion, not a target test count.
- **Repair a known harness failure:** Improve Test Harness directly. Reproduce why the assertion, fixture, clock or environment is wrong before changing it. A passing test is useful only when it still distinguishes the required behavior from the failure.
- **Verify rendered changes:** Visual Regression Check → the relevant design/product/state repair when authorized → rerender the failed state and a normal control → Patch Checking if files changed. A check-only request reports the result without editing product code.
- **Assess a release:** use Release Readiness Audit on the actual candidate and target environment after its relevant patch checks. Route each material blocker to its owner, repeat affected validation and Patch Checking, then reassess the same release gates. Do not replace this with a whole-repository checklist.

## Completion

Report what the evidence establishes at the selected stage: a specific test gap, an effective regression test, rendered behavior or a release-gate verdict. Preserve candidate revision, environment and unverified external layers in handoffs. If the candidate changes, invalidate the affected earlier evidence. Required missing evidence stays a gate; optional checks do not become universal release requirements.

This covers verification quality and release assessment. It does not grant release/deployment permission. A visual result needs rendered evidence; code inspection alone is not visual verification.

## Recipes

| Recipe | Operation |
|---|---|
| [Release Readiness Audit](references/release-readiness-audit.md) | audit |
| [Test Coverage Audit](references/test-coverage-audit.md) | audit |
| [Improve Test Harness](references/test-harness-polish.md) | implement |
| [Visual Regression Check](references/visual-regression-check.md) | check |
