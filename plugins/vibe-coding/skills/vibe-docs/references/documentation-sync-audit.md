# Documentation Sync Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit repository documentation against authoritative code, configuration, schemas, commands, runtime behavior, and generated references.

## Domain invariants

- Documentation identifies its governing source. Distinguish accepted requirements from observed implementation; a mismatch may be a code defect rather than stale prose.
- Commands, paths, config keys, API/schema examples, lifecycle, permissions, and failure behavior match the repository.
- Generated docs/maps are rebuilt by repository-native tooling and distinguish generated from hand-maintained content.
- Runbooks include observable trigger, safe action, rollback/recovery, ownership, and environment assumptions.

## Audit method

1. Trace each selected statement/example to code, tests, config, schema, script, or runtime evidence.
2. Check stale commands, dead paths, renamed symbols, incompatible examples, missing failure/rollback, and duplicated truth.
3. Inspect generation sources and whether manual edits would be overwritten.
4. Separate factual drift from broader editorial improvement.
