# Synthesize Findings

## Scope

Reconcile the supplied audit reports into a prioritized set of actionable tasks. Use their source references and inspect current code only to resolve stale, conflicting or unsupported claims.

## Procedure

1. Retain each candidate’s problem, defining owner, trigger, impact and evidence. Separate observed behavior from assumptions.
2. Merge candidates only when the same correction and validation resolve them. Keep different contracts, rollout boundaries or independent acceptance criteria separate.
3. Drop solved, duplicate or unsupported defect claims. A requested new capability can be planned from the user’s requirement; it does not need a pre-existing bug.
4. Resolve contradictory facts against current sources. Identify the specific missing decision when the repository cannot resolve a requirement or repair choice.
5. Rank by demonstrated impact and dependencies, using the repository’s severity conventions.

## Result

For each retained task give the expected behavior, defining owner and evidence, one recommended correction, acceptance and verification. Preserve dependencies and every requested outcome. Follow the user’s requested number of priorities or output format; do not create new conversations or background work.

Retain enough input references to trace each task back to its findings. If two reports propose incompatible fixes for the same invariant, resolve the owning contract before choosing a correction; do not output both as independently executable tasks. Pass an incomplete retained task to Task Shaping, then Validation & Clarification. A brief that already meets that contract can go directly to validation.
