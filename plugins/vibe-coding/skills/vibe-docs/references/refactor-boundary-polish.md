# Improve Refactor Boundary

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Move the selected behavior to its intended owner and update direct dependents without changing unrelated contracts.

## Domain rules

- Move behavior to one owner and update all directly affected consumers as part of the same accepted change.
- Preserve contracts by default; when changing them, provide explicit migration and remove obsolete paths when safe.
- Add an adapter, temporary flag or compatibility shim only for a named transition, with its consumers and removal condition explicit. Avoid unrelated abstraction layers and mass formatting/renames.
- Synchronize tests, docs, generated outputs, config, registration, and build/deploy references.

## Validation

- Run affected unit/integration/type/build/import/dependency checks.
- Verify old/new compatibility or migration, dead-path removal, generated artifacts, and one representative runtime trace.
- Report untested plugin/reflection/deployment consumers explicitly.

## Execute the transition

Establish the current observable behavior and dependency/registration paths before moving it. Move the invariant to the selected owner, update its direct callers and regenerate dependent artifacts. Keep a deliberate compatibility path until its removal criteria are satisfied; remove an obsolete duplicate only after proving it has no required readers.

Run the checks that can distinguish a mechanical move from a behavior change, including dynamic registration/loading when relevant. A failure returns to the owning transition; a newly invalid migration assumption returns to the plan. After those checks pass, repeat Patch Checking on the full resulting change until clean or blocked. Report the accepted boundary and retained compatibility paths, not merely the list of moved files.
