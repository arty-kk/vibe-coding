# Refresh Repository Maps

## Scope

Update the existing maps affected by the requested change, supplied diff or freshness findings. Preserve their locations, structure, stable IDs and useful source references.

## Procedure

1. Locate affected entries by file/symbol, entity and direct relationship; do not load every map or create absent families.
2. Verify the new description against current code, schemas, configuration, tests and accepted product decisions.
3. Update changed owners, paths, contracts, relations and verification links. Remove obsolete entries or mark the exact unresolved fact.
4. Distinguish product intent from observed implementation when they disagree; do not erase the requirement to match a bug.

## Verification

Check updated file/symbol links, IDs and relationships. Review the map diff for accidental unrelated rewrites. Complete all requested map updates; name a real missing decision or environment rather than stopping after an arbitrary subset. Product code and other documentation are outside a map-only update.

Feed the changed entries and source revision into Map Staleness Check again. Repair remaining stale links or claims from that check, then repeat it. Once the maintained maps agree with the required source state, review the resulting documentation patch with Patch Checking. Stop blocked when a required product decision or inaccessible source cannot be resolved; do not replace the missing fact with a plausible description.
