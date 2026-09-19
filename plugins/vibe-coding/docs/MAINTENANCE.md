# Maintenance

`SKILL.md` defines discovery and routing. Domain recipes live in each skill's `references/`; shared behavior belongs in `references/workflow.md`.

1. Find the owning recipe with `python3 scripts/catalog.py search <query>`.
2. Update that recipe and its discovery metadata if the trigger changed.
3. Add or update its `catalog.json` record when its identity, path or operation changes.
4. Run `python3 scripts/catalog.py refresh` and `python3 scripts/validate.py`.
5. Exercise meaningful behavior changes in a disposable repository with explicit expected outcomes.

Keep portable `plugin.json` and `.codex-plugin/plugin.json` metadata synchronized. Increment both versions for a release. Build with `python3 scripts/package.py --output ../vibe-coding.zip`.

Structural checks cover links, hashes, manifests and catalog consistency. They do not establish that every workflow has been executed against each supported external system.
