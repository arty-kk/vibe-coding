---
name: vibe-backend
description: "Audit, implement or verify API contracts and bot flows: schemas, validation, state, permissions and direct consumers."
---

# APIs & bots

Apply [the working contract](../../references/workflow.md) once. Choose the owning contract rather than treating every backend request as an API redesign.

## Workflows

- **Endpoint behavior:** API Audit when the defect is unproven → Improve API → request/state/consumer verification → [Patch Checking](../vibe-review/references/patch-checking.md).
- **Schema/client evolution:** API Contract Evolution Audit → Improve API Contract Evolution → API Contract Compatibility Check → Patch Checking. Carry the supported version/encoding pairs and rollout window, not just the new schema.
- **Bot journey:** Bot Audit → Improve Bot → replay entry, transition and recovery/denial states → Patch Checking. Carry actor/chat type, persisted state, callback identity and the expected next state.

Start at the correction prompt for a known defect or explicit new requirement. A compatibility-check-only request uses the check directly and makes no product changes. An audit-only request returns findings.

## Repair and handoff

The implementation step consumes the failing request/transition, authoritative owner, expected response/effect and direct consumers. Verification inspects returned values and persisted/external effects where they differ. A failed version pair or bot transition returns to that same owner; repair, rerun the affected cases, then review the complete resulting patch until the clean marker or a concrete gate.

Do not reduce a supported compatibility window to make a check pass, or send real bot messages merely to validate code. Preserve the selected service/schema/platform and user authorization through the whole chain.

## Recipes

| Recipe | Operation |
|---|---|
| [API Contract Evolution Audit](references/api-contract-evolution-audit.md) | audit |
| [Improve API Contract Evolution](references/api-contract-evolution-polish.md) | implement |
| [API Contract Compatibility Check](references/api-contract-compatibility-check.md) | check |
| [API Audit](references/api-audit.md) | audit |
| [Improve API](references/api-polish.md) | implement |
| [Bot Audit](references/bot-audit.md) | audit |
| [Improve Bot](references/bot-polish.md) | implement |


For an old/new schema or generated-client compatibility boundary, select the API Contract Evolution recipes. A general endpoint behavior audit still uses API Audit.
