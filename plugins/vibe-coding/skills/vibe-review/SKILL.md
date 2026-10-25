---
name: vibe-review
description: "Review a patch, PR or branch against its intended behavior; repair in-scope defects when authorized and repeat Patch Checking until clean or blocked. Use for changed code and its direct contracts."
---

# Change review

Use [Patch Checking](references/patch-checking.md) as the review step of an implementation workflow or as a standalone review. Apply [the working contract](../../references/workflow.md) once.

## Workflow

1. Fix the review boundary: the explicit patch/PR/range, or the current branch against its evidenced integration target. Keep that same boundary through every correction; a new fix commit does not replace the original review target.
2. Recover the intended behavior and inspect the complete resulting change, including the unchanged owners and direct consumers needed to judge it. A test passing is evidence for that test, not a substitute for reviewing the changed contract.
3. For a review-only request, return supported findings without editing. For an authorized implementation or repair, correct those findings, run the relevant validation and start another review pass on the resulting patch.
4. Continue until a full pass makes no product changes, finds no qualifying defects and has evidence for every required check. Only then return the clean marker. A missing environment, unresolved finding or repeated failure with no new evidence ends the loop with its actual limitation.

Pass the reviewed base, resulting patch identity, findings and validation results between passes in the current task. Do not open a new task, merge the PR or expand into an unrelated audit.

## Completion

The clean result starts exactly with `✅ Everything is fine. No changes required 👌`. If this pass applied a correction, it cannot issue that marker: repeat the review first. Findings, blocked validation and an absent patch have distinct outcomes in the recipe.

## Recipes

| Recipe | Operation |
|---|---|
| [Patch Checking](references/patch-checking.md) | review |
