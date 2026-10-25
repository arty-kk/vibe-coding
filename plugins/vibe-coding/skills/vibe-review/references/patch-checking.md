# Patch Checking

## Target and operation

Honor the explicit diff, PR, snapshot, branch, range or commit supplied by the user. A single commit limits scope only when explicitly requested. Otherwise use the current branch and its evidenced integration target; use their merge base and include the full branch delta plus staged, unstaged and untracked changes. If no integration target can be established, inspect available working-tree changes and state that branch integration remains unverified. Do not invent a remote or compare an unrelated branch.

If no changes or target are visible, report `Patch not found: no changed files or review target visible.` and stop. Do not create a sample patch.

Review means inspect and report. Apply fixes only for a request to fix or an already-authorized implementation. Preparing or reviewing a PR does not authorize merging it.

## Establish a review pass

Keep the original comparison base and requested scope stable. Record the current revision and working-tree delta sufficiently to notice changes during the pass. Carry forward the requested behavior, findings already fixed, failed checks and external gates; recover this state from the visible task rather than assuming an unseen prior review.

A pass examines one resulting patch state. If a correction, generated output, migration update or concurrent edit changes that state, review the new state before declaring it clean. Inspect the full requested delta again, not only the last corrective commit.

## Review the resulting state

Recover intended behavior and acceptance criteria. Inventory additions, renames, deletions, code, schemas, migrations, manifests, lockfiles, generated files, config and deployment assets. For each changed contract identify its owner and inspect direct callers, consumers and operational paths. Check target-side changes after the merge base when available; use a non-destructive merge simulation if it adds relevant evidence.

Check ownership and architectural layer, producer/consumer compatibility, API/event/error semantics, permissions and tenancy, serialization, state transitions, concurrency, retries, cancellation, cleanup, migration and rollout/rollback only where the actual change makes them relevant. Check that verification exercises the real changed path rather than an unrelated or fully mocked path.

A defect must be introduced by the change, represent required behavior that is missing, or be a pre-existing condition that directly prevents the changed contract from working or integrating correctly. Exclude style preferences, speculative redesign and unrelated existing defects. Cite the governing expectation and a reachable violation with path, line, symbol and impact. Separate direct evidence from inference.

## Correction and validation

For each supported finding, retain its owner, violated expectation, reachable input/state, impact and a concrete acceptance check. This becomes the input to correction; a suggestion without a demonstrated violation is not a repair target.

When authorized, correct the in-scope defect at its authoritative owner and synchronize directly affected contracts. Preserve the required behavior and earlier fixes as constraints. Do not replace the implementation with another architecture merely to generate a new patch.

Discover relevant commands from the actual repository and run focused applicable checks. Record exact commands and outcomes. Required failed, missing or unavailable validation prevents a fully clean verdict; optional unrun checks are reported proportionally. Preserve unrelated work. Inspect final changes, including untracked and generated files, and use `git diff --check` when Git is available.

## Repeat until the resulting patch is clean

After a correction, run its validation and start another pass from the same review boundary. Check the corrected owner, consumers and failure paths in the complete resulting delta. Reconcile previous findings: fixed with evidence, still open, or withdrawn with a reason. Do not count a finding as resolved merely because the code was edited.

- **No findings, required checks passed, no correction in this pass:** finish clean.
- **Corrections applied:** carry the new patch state and validation forward, then repeat Patch Checking. A correction pass does not produce the clean marker.
- **Findings in review-only mode:** report them and stop; the request did not authorize a repair loop.
- **Required validation unavailable, a fix needs an unprovided decision, or a necessary external action lacks authorization:** report the gate and stop blocked. Completed checks remain recorded; unavailable checks remain unavailable.
- **The same unresolved finding or failed check returns without a changed patch, a new hypothesis or new evidence:** stop and describe what is needed to make progress. Do not repeat indefinitely or turn the lack of progress into a clean verdict.

The loop may complete within the current authorized task. It does not require a new user message, a new conversation or a second agent. If the user limits attempts or resources, stop at that boundary and retain the actual verdict.

## Result

For a clean pass, start exactly with:

`✅ Everything is fine. No changes required 👌`

Then identify the reviewed target and material validation evidence briefly. When earlier passes made fixes, summarize their effect after the marker; the marker describes the final pass, not the absence of changes during the whole task.

For other outcomes, start with `PATCH_CHECK: FINDINGS`, `PATCH_CHECK: BLOCKED`, or the exact no-patch message above. Give the remaining defect or gate, its evidence and the next necessary action. While a repair loop continues, carry `PATCH_CHECK: RECHECK` internally rather than presenting an intermediate fix as completion.

Write the explanation in the user's language. Do not emit the clean marker in examples, quoted findings or blocked results where a consumer could mistake it for the verdict.
