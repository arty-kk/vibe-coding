# Form & Data UI Audit

## Goal and scope

Audit a form, editor, table, search, filter, pagination, or data-entry surface against validation and persistence contracts.

## Domain invariants

- Field names, types, units, nullability, defaults, normalization, and validation agree with the authoritative API/schema.
- Dirty state, autosave, submit, duplicate submit, optimistic state, server errors, and conflict recovery are explicit.
- Sorting, filtering, pagination, selection, and bulk actions retain stable identity and tenant/permission scope.
- Labels, instructions, errors, focus, keyboard use, and screen-reader relationships remain accessible.

## Audit method

1. Trace each changed field or data operation from UI representation to serialized request and persisted result.
2. Check client/server validation drift, timezone/locale/unit conversion, partial edit, refresh, back navigation, and conflicts.
3. Inspect table identity, cursor/page semantics, selection across pages, and stale query behavior.
4. Identify data loss, duplicate submission, misleading success, and inaccessible error recovery.

## Handoff

Retain field/record/query identity, initial draft/page state, exact user input, serialized payload and expected stored value. Locate the first representation, validation, mutation or query-state mismatch and feed it to Improve Form & Data UI. A success toast is not evidence of the persisted contract or stable selection across pages.
