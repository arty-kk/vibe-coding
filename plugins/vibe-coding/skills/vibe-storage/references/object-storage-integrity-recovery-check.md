# Object Storage Integrity & Recovery Check

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

## Execute and decide

Use a dedicated authorized bucket/prefix and distinguishable synthetic bytes with a known checksum. Establish a normal authorized upload/download and reference control, then interrupt or race the selected initiate/part/complete/reference/event boundary while preserving operation identity.

Inspect provider upload/object versions, actual assembled/downloaded bytes, database references and orphan state independently. Verify the selected expired/denied operation cannot access or alter the protected object. For lifecycle/restore, retain the exact source version and compare recovered bytes/application references under the stated policy.

Return passed, failed or blocked with identities, event order, byte/reference observations and missing provider layers. Feed failures into the authorized owner repair, repeat its case/control and finish Patch Checking. Retention/delete/restore tests must not mutate unapproved production data.
