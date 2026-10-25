# Improve OCR Document AI

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected document-processing contract across intake, extraction, confidence, correction or export and its directly affected states. The required behavior determines the size of the correction; a single parser or label fix is valid when it resolves the observed defect.

## Scope selection

- If the user named a document type, field, table, upload flow, correction UI, export, or extraction bug, improve that surface and directly affected states.
- If the request is broad, inspect current document-AI surfaces and choose the highest-confidence improvement with meaningful user/operator impact.
- Include related fixtures, evals, copy, telemetry, and downstream contract fixes when they belong to the same document workflow.
- Avoid provider/model swaps, large data migrations, and unrelated ingestion redesign unless required by the task or repo evidence.

## Change targets

- File validation, upload constraints, preprocessing, page ordering, extraction schema, locale parsing, confidence thresholds, and typed field states.
- Low-confidence, unsupported-format, partial-extraction, retry, duplicate-job, correction, export, deletion, and permission states.
- Human review UX: clear labels, editable vs generated fields, validation messages, audit trail, and safe diagnostics.
- Downstream API/DB/export alignment and directly affected tests/evals/fixtures.
- Privacy boundaries: no unnecessary document/PII logging, no public internal error details.

## Implementation principles

- Apply changes at the owning pipeline or schema boundary rather than duplicating parser fixes downstream.
- Preserve existing storage, queue, OCR provider, and export architecture unless the task explicitly requires changing it.
- Keep extracted-data claims honest: distinguish missing, unknown, low-confidence, corrected, and verified values when the product model supports it.

## Validation

Run relevant repository-native checks and any document/OCR eval or fixture test that protects the changed path. If real document fixtures, provider keys, or queues are unavailable, run deterministic tests and state the exact gap.

Replay the same page/region and expected field state after correction, including persistence/export when a human correction was involved. Distinguish a correct extracted value from a value that only looks correct in the review UI. Return failures to the owning pipeline/schema, then review the accepted patch through Patch Checking.
