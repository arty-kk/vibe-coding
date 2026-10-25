# Refactor Boundary Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit a proposed or partial refactor for ownership, contract preservation, migration completeness, and removal of duplicate paths.

## Domain invariants

- The target boundary has a clear owner and satisfies the requested reason for the refactor without losing required behavior; an architectural preference alone is not a defect.
- Public/internal contracts, imports, serialization, state, errors, config, and performance remain compatible or deliberately migrated.
- All direct callers, tests, docs, generated artifacts, deployment/runtime references, and dead paths are accounted for.
- Compatibility shims have explicit users and removal criteria; no parallel source of truth remains.

## Audit method

1. Map the current owner, dependency graph, call sites, data/control flow, tests, config, and runtime loading.
2. Define the proposed boundary and identify contract, rollout, migration, and validation deltas.
3. Check cyclic dependencies, hidden initialization, generated code, reflection/registration, serialization, and performance-sensitive paths.
4. Split independent refactors and reject broad cleanup without task value.

## Handoff

Provide the owning invariant, current/proposed boundary, concrete consumer break or duplicate truth, and an acceptance check. For a transition requiring mixed versions or data movement, pass those constraints into Migration & Refactor Plan. For an already bounded compatible move, feed Improve Refactor Boundary directly when changes are authorized.
