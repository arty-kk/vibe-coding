# Compatibility Golden Master Check

## Goal

Verify that the candidate preserves the selected reference behavior across the supported input and version corpus.

## Context

Identify authorized reference and candidate versions/configurations, accepted input corpus, expected semantic behavior and fields whose nondeterminism is proven.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Replay a versioned corpus against reference and candidate; compare semantic output, state, errors, ordering, and side effects.
- Mutate boundaries and malformed/unknown fields safely; verify parser limits and reference-compatible rejection/recovery.
- Run duplicate, concurrent, timeout, and restart cases to expose hidden identity, retry, persistence, and ordering contracts.
- Test multiple reference versions/configurations and classify stable contract versus version-specific behavior.
- Review every normalized golden field and prove why it is nondeterministic rather than masking a regression.

## Verification

Record each reference/candidate mismatch with input identity, output/state/error difference and allowed normalization; do not count a masked semantic difference as compatible.

## Execute and decide

Freeze the corpus, reference/candidate versions and normalization rules before comparison. Establish a valid control against both sides, then replay the selected normal, edge and failure cases while observing outputs and state/effects independently. Where order or timing is part of the contract, preserve that observation instead of sorting or dropping it.

Classify each difference as a supported mismatch, proven nondeterminism, environment variance or unobserved behavior. Return passed, failed or blocked for the stated corpus/window. Feed a failing case and its raw/normalized difference back to the authorized repair, repeat the comparison after correction and require Patch Checking for changed code. Regenerating goldens requires reference evidence or an explicit approved contract change.
