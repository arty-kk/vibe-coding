# Privacy Data Rights Audit

## Goal and scope

Audit one privacy/data-rights boundary such as PII collection, consent, retention, deletion, export, account closure, data sharing, telemetry, or sensitive logging. Use the supplied product/privacy policy as expected behavior; do not infer jurisdictional requirements from code.

## Domain invariants

- PII/sensitive data has explicit collection, storage, access, retention, deletion/export, and logging behavior.
- Consent, opt-out, privacy settings, and communication preferences are enforced at owner layers.
- Deletion/export jobs cover primary stores and directly affected indexes, caches, object storage, analytics, and provider integrations.
- Logs, traces, analytics, and error reports avoid unnecessary sensitive payloads.
- Tests or operational gates verify the selected data-right behavior.

## Audit method

Trace selected data fields from collection through persistence, derived stores, external providers, logs, exports, deletion/retention jobs, backups/runbooks when visible, and user/admin UI. Separate repository facts from legal/business assumptions.

## Handoff

Retain the synthetic subject/data identity, accepted collection/retention/export/deletion rule and the first store/provider/log edge that violates it. Include relevant retry, derived-data and restoration behavior without inferring a jurisdictional rule. Feed that concrete data lifecycle and expected observation into Improve Privacy Data Rights.
