# Improve Documentation Sync

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Synchronize the selected documentation or generator with current code, configuration and runnable commands.

## Domain rules

- Update the nearest maintained document or generator source, not downstream generated output alone.
- Keep examples executable/minimal and align them with the accepted contract. If implementation contradicts a requirement, identify the discrepancy rather than changing the requirement to match it.
- Record version/environment assumptions and distinguish repository-proven behavior from external requirements.
- Remove stale duplicate guidance when one canonical document now owns it.

## Validation

- Run doc generators, link/lint/example/command checks available in the repository.
- Compare generated diff and verify referenced paths/symbols/configs exist.
- List external service or deployment behavior not executable from the worktree.

## Repair cycle

Trace each selected drift finding to the maintained source, update the statement/example there and regenerate its direct outputs. Verify a safe command/example against the defining script or a controlled execution; documenting a production/deployment command does not authorize running it.

Recheck the corrected claims against code/configuration and inspect the generated diff. A failed example returns to its owner; a conflict with a product requirement remains a decision or product defect, not a prose rewrite. Once the selected drift is resolved, run Patch Checking on the documentation/generator patch. Report external prerequisites that still prevent a required example from being verified.
