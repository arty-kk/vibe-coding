# Reconcile Repository Maps

## Scope

Compare the supplied or explicitly selected maps. Use only related source code, schemas, configuration and decisions to resolve stale entries or contradictions.

## Procedure

1. Preserve existing IDs and source references. Match entries by the actual entity, owner and contract, not by similar labels.
2. Merge duplicate descriptions; keep distinct data, permission, runtime or rollout relationships separate.
3. Verify missing paths/symbols and conflicting owner, schema, state, enforcement or test claims against current sources.
4. Distinguish implementation evidence from product requirements. A map describes either and cannot silently redefine one from the other.

## Result

Return reconciled relationships, specific stale/conflicting entries and remaining decisions in the requested format. Recommend the next relevant source or skill where useful. Do not generate absent map families or implementation tasks unless requested.
