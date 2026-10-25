# Improve Reverse Engineering

## Goal

Implement the selected compatibility behavior against an authorized reference and a reproducible comparison corpus.

## Domain rules

- Implement the smallest compatibility layer at the actual boundary and preserve raw evidence/fixtures separately from inferred domain models.
- Parse defensively with explicit bounds and unknown-field/version policy; never execute captured untrusted content.
- Use semantic normalization only for documented nondeterminism and keep stable order/timing/error quirks when consumers depend on them.
- Add differential/golden tests before refactoring internals; isolate intentional deviations behind versioning or migration.
- Document confidence and unresolved branches so future evidence can update the model without rewriting the entire adapter.

## Validation

- Run deterministic fixture/golden tests and differential tests against an authorized reference where available.
- Exercise version skew, malformed/truncated/unknown fields, duplicate/retry, concurrent operations, restart, and representative data scale.
- Verify fixture redaction, provenance, deterministic normalization, and absence of unsupported claims.

First preserve the reference capture and a failing differential case. Correct the parser, adapter or state owner at the observed boundary, then replay the same corpus without changing expectations to fit the candidate. Pass candidate/reference identities and allowed normalization to the golden-master check. A semantic mismatch returns to that owner; an unsupported reference branch remains unknown. After accepted comparison, finish Patch Checking on the resulting change.
