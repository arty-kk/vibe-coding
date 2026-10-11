# Object Storage Integrity & Recovery Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected object operation preserves authorized identity, bytes and recoverability under its supported retry or lifecycle behavior.

## Context

Identify provider/API version, selected bucket/key and versioning/conditional-write model, upload identity, integrity algorithm, authorization and promised recovery behavior.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Interrupt multipart upload at each boundary, resume it, submit wrong/duplicate parts, and verify checksum, exact completion, and orphan cleanup.
- Race two writers and delete/overwrite operations using conditional/versioned requests; verify database/object identity and recoverability.
- Replay duplicate/out-of-order/missing notifications and prove idempotent reconciliation against current object version.
- Expire/revoke presigned access and test wrong key/method/content constraints without unsafe broad credentials.
- Exercise version recovery/lifecycle/replication failure in a safe bucket and verify restore procedure, retention, encryption permissions, and observability.

## Verification

Compare object bytes/checksums, database references, identity/version, allowed access and orphan/recovery state; do not use ETag as a universal content checksum.
