# Prompt Skill Sync Audit

## Scope

Maintain the selected Vibe Coding package: skill discovery, domain recipes, shared workflow, catalog and validation.
Inspect and report without editing.

Read the package manifests, selected SKILL.md entrypoints, referenced recipes and catalog entries. Each skill needs a distinct trigger; every recipe must be reachable; relative links must resolve inside the package. Keep inspection and implementation instructions consistent with the requested operation. Preserve domain invariants when simplifying repeated guidance.

Report supported findings with file and recipe evidence and one concrete repair direction.

Run `python3 scripts/validate.py` from the plugin root. For a behavior change, use a representative task in a disposable fixture and record the actual result. Structural validation establishes package consistency; task execution establishes observed model behavior.

For a composed workflow, trace one realistic request from discovery through its entry prompt, handoff, domain check and Patch Checking loop. Verify that every next prompt can consume the preceding output, that review-only work cannot silently become repair, and that blocked/no-progress outcomes cannot be rendered clean.

For MCP distribution, inspect the actual tool descriptions, argument/result schemas, search ranking and the selected context returned by retrieval. Check exact IDs and natural-language discovery separately. Verify that the served snapshot matches the reviewed source rather than assuming an edited Markdown file is already live. Report the failed transition or retrieval case as a concrete maintenance input.
