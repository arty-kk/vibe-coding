---
name: vibe-security
description: "Audit, repair or verify a requested application-security, abuse, privacy or audit-log boundary; do not broaden ordinary edits into hardening."
---

# Security & privacy

Apply [the working contract](../../references/workflow.md) once. Select the requested trust, privacy or evidence boundary; ordinary implementation does not trigger a broad security/hardening review.

## Workflows

- **Application vulnerability:** Security Audit → Improve Security → Security Abuse Defense Check for the demonstrated control → [Patch Checking](../vibe-review/references/patch-checking.md).
- **A selected systemic abuse path:** System Security Hardening Audit → Improve System Security Hardening → Security Abuse Defense Check → Patch Checking.
- **Dependency/CI/build trust:** Build Supply Chain Audit → Improve Build Supply Chain → the synthetic attacker-input and valid-build controls, with Release Artifact Trust Check when final bytes/identity need verification → Patch Checking.
- **Privacy/data rights:** Privacy Data Rights Audit → Improve Privacy Data Rights → Privacy Data Rights Check → Patch Checking.
- **Durable action evidence:** Audit Logging Compliance Audit → Improve Audit Logging Compliance → Audit Trail Integrity Check → Patch Checking.

Start at correction for an established defect or at a named check for verification-only work. Carry actor/controlled input, asset or data identity, authoritative policy, reachable effect and a safe distinguishing case. Keep legal/product policy decisions separate from technical enforcement.

After correction, prove permitted use still succeeds and the selected denial/control happens before the protected effect. Inspect durable state, derived/provider data or audit sink when that is the guarantee. Return failed evidence to the same owner, replay its control/case and finish patch review. No recipe authorizes broad live scanning, credential attacks, destructive data cleanup or real key changes by itself; retain required external authority/evidence as a gate.

## Recipes

| Recipe | Operation |
|---|---|
| [Build Supply Chain Audit](references/build-supply-chain-audit.md) | audit |
| [Improve Build Supply Chain](references/build-supply-chain-polish.md) | implement |
| [Audit Logging Compliance Audit](references/audit-logging-compliance-audit.md) | audit |
| [Improve Audit Logging Compliance](references/audit-logging-compliance-polish.md) | implement |
| [Audit Trail Integrity Check](references/audit-trail-integrity-check.md) | check |
| [Privacy Data Rights Audit](references/privacy-data-rights-audit.md) | audit |
| [Privacy Data Rights Check](references/privacy-data-rights-check.md) | check |
| [Improve Privacy Data Rights](references/privacy-data-rights-polish.md) | implement |
| [Security Abuse Defense Check](references/security-abuse-defense-check.md) | check |
| [Security Audit](references/security-audit.md) | audit |
| [Improve Security](references/security-polish.md) | implement |
| [System Security Hardening Audit](references/system-security-hardening-audit.md) | audit |
| [Improve System Security Hardening](references/system-security-hardening-polish.md) | implement |


Build Supply Chain owns untrusted inputs, dependency execution and CI privileges. Verification of an already built artifact belongs to [Recovery](../vibe-recovery/SKILL.md).
