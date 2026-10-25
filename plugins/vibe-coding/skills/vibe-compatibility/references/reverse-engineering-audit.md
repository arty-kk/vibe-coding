# Reverse Engineering Audit

## Goal and scope

Reconstruct an existing system's observable contract from authorized evidence and preserve compatibility through differential and golden-master validation.

## Domain invariants

- Scope and authorization are explicit; evidence acquisition does not bypass access controls, licensing restrictions, or safety boundaries.
- Observed facts, inferred hypotheses, and unknowns are labelled separately with provenance, version, environment, and reproducible capture steps.
- The contract includes accepted inputs, normalization, state, outputs, errors, timing/order, retries, side effects, persistence, and compatibility quirks—not only the happy-path schema.
- Data model reconstruction distinguishes logical identity, storage representation, indexes/constraints, lifecycle, and derived/cached fields.
- Protocol/file-format analysis preserves framing, encoding, endianness, lengths, checksums, optional/unknown fields, version negotiation, and malformed-input behavior.
- Golden masters normalize only proven nondeterminism; semantic fields remain asserted, sensitive captures are redacted, and fixtures are versioned and reviewable.
- A replacement or adapter is compared differentially against the reference over representative, edge, malformed, retry, restart, and concurrency cases.
- Intentional deviations are explicit product decisions with migration/consumer evidence rather than accidental incompatibility.

## Audit method

1. Define the exact reference version/environment and capture authorized inputs/outputs/state/transcripts with timestamps and provenance.
2. Build a behavior matrix across normal, boundary, invalid, duplicate, concurrent, timeout, restart, and partial-failure cases.
3. Infer the smallest model explaining observations and design discriminating experiments for competing hypotheses.
4. Map every observed field/message/table/file element to producer, consumer, lifecycle, optionality, and compatibility behavior.
5. Compare current implementation/reference fixtures and classify deterministic mismatch, nondeterminism, environment variance, and unsupported unknown.

## Handoff

For each selected behavior, supply the authorized capture, reference version/config, input identity, observed output/state/effect and the narrowest supported interpretation. Preserve competing hypotheses with the experiment that would distinguish them. Feed supported behavior and unresolved branches to Improve Reverse Engineering; a plausible inferred schema is not evidence that unobserved branches are compatible.
