# Improve Object Storage

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected object operation while preserving authorization, identity, integrity and recovery.

## Domain rules

- Allocate stable object/version identity before retryable upload and use conditional operations or database version checks for concurrent writers.
- Keep multipart state resumable, verify checksums using provider-supported algorithms, and ensure abort/lifecycle cleanup for abandoned uploads.
- Issue short-lived least-scope presigned operations only after application authorization and validate metadata/content again at completion.
- Treat events as hints and make consumers idempotent/reconciling; preserve the selected immutable key, version/generation or conditional validator in dependent references.
- Stage lifecycle/versioning/retention changes with inventory and restore evidence; do not equate replication with backup.

## Validation

- Run provider-compatible integration tests or an explicitly qualified emulator for request shape; do not infer managed-service behavior from an emulator alone.
- Exercise interrupted/resumed multipart, duplicate complete, checksum mismatch, concurrent overwrite/delete, expired presign, duplicate/out-of-order event, lifecycle, and restore.
- Measure memory/connections/throughput for representative object sizes and record provider-side gates not exercised.
