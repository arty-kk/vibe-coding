---
name: vibe-storage
description: "Audit, repair or verify object-storage authorization, identity, upload integrity, lifecycle and recovery."
---

# Object storage

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Object Storage Audit → Improve Object Storage → Object Storage Integrity & Recovery Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry provider/API, bucket/account/key, upload operation, actual version/generation or conditional validator, authorization and expected bytes/recovery into correction. A known upload/lifecycle defect starts at implementation; a verification-only request uses a safe bucket/fixture without product edits.

Trace authorization → key/upload allocation → provider completion → database reference → event/lifecycle/recovery. Correct the first identity, integrity, access or cleanup boundary and replay the same interruption/race with a valid control.

Inspect actual downloaded/assembled bytes, object version and database references independently. A completed response, ETag or replication status is not proof of content integrity or backup recovery by itself. Return failed evidence to its owner, recheck and finish patch review; provider retention, lifecycle and restore actions require the appropriate authorized environment.

## Recipes

| Recipe | Operation |
|---|---|
| [Object Storage Audit](references/object-storage-audit.md) | audit |
| [Object Storage Integrity & Recovery Check](references/object-storage-integrity-recovery-check.md) | check |
| [Improve Object Storage](references/object-storage-polish.md) | implement |
