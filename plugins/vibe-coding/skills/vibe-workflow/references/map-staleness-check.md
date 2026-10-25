# Check Map Freshness

## Scope

Inspect the existing maps selected by the user or referenced by the changed behavior. Use the supplied diff, changed-file list or current working-tree changes. If no change or map target is supplied, identify that gap; do not generate map families.

## Procedure

1. Search the selected maps for affected file paths, symbols, entities and relationships.
2. Compare those entries with current defining code, schemas, tests, configuration or product decisions.
3. Check deleted/renamed references, moved owners, changed contracts and assertions that no longer support the mapped claim.
4. Separate a stale description from a product defect. A map does not redefine intended behavior from the current implementation.

## Result

Report affected map entries, direct source evidence and the narrow required update; or no stale entries within the inspected scope. Name unresolved evidence. Do not edit maps or product files during this check.

Use `MAPS_FRESH`, `MAPS_STALE`, `NO_MAINTAINED_MAPS`, or `MAP_CHECK_BLOCKED`. Pass stale entry IDs/sections, the contradicting source and the required description change to Map Refresh. NO_MAINTAINED_MAPS is not an instruction to create maps. A fresh verdict applies only to the inspected maps and source state.
