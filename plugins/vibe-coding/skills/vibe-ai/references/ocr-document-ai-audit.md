# OCR Document AI Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit OCR and document-AI behavior from upload/intake to extracted data, correction, export, storage, and downstream use. Keep only reachable issues that affect extraction correctness, safety, privacy, workflow completion, or regression resistance.

## Inspect

Upload/intake routes, file validators, storage, preprocessing, OCR engines, document classifiers, page/region/table extraction, field schemas, confidence handling, human correction UI, export serializers, downstream consumers, async jobs, retries/idempotency, audit logs, PII handling, tests/evals/fixtures, telemetry, docs, and `docs/ai_map.md` when present.

## Issue classes

- Intake and preprocessing: unsupported formats accepted as valid, unsafe file handling, page order drift, rotation/skew not handled where current docs imply it, image/PDF conversion failures, and unbounded file/page size.
- Extraction contracts: field/table/checkbox/signature schema drift, missing required fields, weak confidence thresholds, locale/date/number parsing bugs, and ambiguous null vs unknown behavior.
- Human review and correction: low-confidence data presented as final, correction UI not persisted/exported, no audit trail for edits, and inaccessible or unclear validation states.
- Async/idempotency: duplicate jobs, lost partial results, retries creating conflicting exports, stale status, and user-visible completion before extraction is durable.
- Privacy/security: PII or document contents logged unnecessarily, cross-tenant document exposure, unsafe temporary files, and public error leakage.
- Downstream sync: extracted data shape mismatches API/DB/export/contracts, stale docs/maps, and tests that assert fixtures but not observable behavior.
- Evaluation: missing fixtures for representative document types, low-confidence cases, table extraction, locale parsing, and known regressions.

## Finding quality

- Include document type, pipeline step, expected output/validation behavior, acceptance criteria, and eval/test direction when discoverable.
- Do not recommend changing OCR providers/models unless current repo evidence proves the existing owner cannot satisfy the behavior.

## Trace and hand off

Use a permitted representative document and expected field/table output. Follow page/region identity through preprocessing, extraction, typed confidence/missing states, human correction, persistence and export. Compare the final consumer value with the source region and any accepted correction. Pass the document class, failing pipeline step, expected typed state and reproducing fixture to Improve OCR Document AI; retain privacy-safe references instead of raw sensitive documents in reports.
