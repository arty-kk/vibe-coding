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
