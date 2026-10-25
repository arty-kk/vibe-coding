# Evidence Normalization

## Operation

Normalize the supplied evidence without changing the product or selecting an implementation.

## Goal

Convert heterogeneous repository findings, logs, traces, tickets, and audit outputs into a deduplicated evidence set suitable for synthesis without changing priority or inventing missing facts.

## Normalize

Accept logs, audit prose, tickets, traces, plans, or model outputs. Preserve provenance and exact uncertainty. Extract only evidence-backed owner, invariant, impact, acceptance, validation, scope, and rollout data. Do not upgrade hypotheses to facts, merge independent owners, or choose downstream implementation work.

Return the narrowest applicable artifact: intake summary, audit result, task definition, implementation summary, or check evidence. When source material conflicts, keep both claims and mark the missing discriminator.

- Preserve exact `path:line[-line]`, symbol, command, trace, timestamp, environment, and source references when available.
- Mark each statement as direct evidence, inference, assumption, or unavailable fact.
- Merge only identical observations; keep contradictory evidence side by side for [Synthesis](../../vibe-task/references/synthesis.md).
- Remove prose that does not change owner, invariant, impact, acceptance, validation, dependency, or exclusion.

Keep each observation attached to its source revision/environment and the claim it actually supports. A successful local fixture does not cancel a production failure from another environment. The handoff to Synthesis contains deduplicated observations, unresolved contradictions and missing discriminators; it does not label hypotheses as implementation-ready findings.
