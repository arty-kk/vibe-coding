# Improve Form & Data UI

## Goal

Correct the selected field or data operation from user input through validation, serialization and stored result.

## Domain rules

- Keep one validation source where architecture permits and map server errors to stable field/form states.
- Use stable record identity and explicit query/mutation ownership; do not infer saved state from optimistic UI alone.
- Preserve user input across recoverable failure and prevent stale responses from overwriting newer edits.
- Update affected schemas, generated types, fixtures, analytics, and copy with the field contract.

## Validation

- Run form/table/component/type/e2e checks for changed contracts.
- Exercise invalid input, server rejection, duplicate submit, slow/stale response, conflict, pagination/filter, and keyboard paths.
- Verify serialized payload and stored result, not only rendered success state.

Correct the field/schema, draft/mutation or query/selection owner, preserving recoverable user input and stable record identity. Replay the same input and slow/rejected/conflicting sequence, then inspect request, stored data and rendered feedback. Feed acceptance into Product Acceptance Check where needed; return failures to the same boundary and finish Patch Checking rather than masking data errors with copy.
