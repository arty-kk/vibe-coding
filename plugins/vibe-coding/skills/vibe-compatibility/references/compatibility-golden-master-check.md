# Compatibility Golden Master Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

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
