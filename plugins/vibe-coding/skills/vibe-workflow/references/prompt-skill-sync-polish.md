# Improve Prompt Skill Sync

## Scope

Maintain the selected Vibe Coding package: skill discovery, domain recipes, shared workflow, catalog and validation.
Implement the requested maintenance change and preserve unrelated entries.

Read the package manifests, selected SKILL.md entrypoints, referenced recipes and catalog entries. Each skill needs a distinct trigger; every recipe must be reachable; relative links must resolve inside the package. Keep inspection and implementation instructions consistent with the requested operation. Preserve domain invariants when simplifying repeated guidance.

Update affected catalog entries and discovery metadata. Run `python3 scripts/catalog.py refresh` after recipe changes.

Run `python3 scripts/validate.py` from the plugin root. For a behavior change, use a representative task in a disposable fixture and record the actual result. Structural validation establishes package consistency; task execution establishes observed model behavior.

Repair the selected trigger, handoff or decision rule, then replay the request that exposed it. Keep domain invariants when removing repeated prose. For composed workflows, make the next prompt ID, required input, completion condition and repair/recheck transition explicit. A workflow is not complete because all its prompts exist independently.

When MCP retrieval is affected, rebuild its snapshot and exercise the real search/get tools against representative and negative cases. Keep package version, instruction version, catalog hashes and source links consistent. Distinguish instruction walkthroughs, deterministic transport tests and actual model execution in the reported evidence. Preserve historical releases/evaluations; use a new revision record for changed inputs.

Finish the maintenance patch through Patch Checking. Publication is a separate action in the user's authorized scope; do not edit an installed plugin cache as a substitute for updating its source/distribution.
