# AI Safety & Governance Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit an AI release for misuse, harmful output, privacy, accountability, evaluation evidence, human control, and rollback governance.

## Domain invariants

- Intended use, excluded use, affected users, risk owners, human control, and escalation paths are explicit.
- Safety and policy controls are enforced at input/tool/output/product boundaries and tested against reachable misuse.
- Data/model/prompt/tool provenance, evaluation results, approvals, release identity, monitoring, and incident evidence are retained appropriately.
- Disable, rollback, correction, user reporting, and remediation paths exist for harmful or materially wrong behavior.

## Audit method

1. Define the concrete harm/misuse scenarios and map them to feature capabilities, users, data, tools, and side effects.
2. Inspect policy implementation, refusal/guardrails, human review, overrides, logging, appeal/correction, and incident ownership.
3. Review evaluation coverage by risk slice, adversarial inputs, false-positive/negative tradeoffs, and model/provider change.
4. Check privacy, retention, consent, third-party terms, and cross-tenant exposure from repository evidence.

## Handoff

For each selected risk, identify the actor/input, reachable harmful effect, enforcing boundary and observable allowed/denied outcome. Distinguish technical controls from policy/legal decisions requiring an owner. Feed the technical correction and its safe misuse/control scenarios into Improve AI Safety & Governance; do not substitute an extra refusal sentence for absent runtime control.
