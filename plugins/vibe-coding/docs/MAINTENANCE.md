# Maintenance

`SKILL.md` defines discovery and routing. Domain recipes live in each skill's `references/`; shared behavior belongs in `references/workflow.md`.

1. Find the owning recipe with `python3 scripts/catalog.py search <query>`.
2. Update that recipe and its discovery metadata if the trigger changed.
3. Add or update its `catalog.json` record when its identity, path or operation changes.
4. Run `python3 scripts/catalog.py refresh` and `python3 scripts/validate.py`.
5. Exercise meaningful behavior changes in a disposable repository with explicit expected outcomes.

Keep portable `plugin.json` and `.codex-plugin/plugin.json` metadata synchronized. Increment both versions for a release. Build with `python3 scripts/package.py --output ../vibe-coding.zip`.

Structural checks cover links, hashes, manifests and catalog consistency. They do not establish that every workflow has been executed against each supported external system.

## Catalog and translations

The offline catalog and public website share `assets/catalog/` and `scripts/catalog_site.py`. Add a workflow's title in all four locale JSON files; add category/summary entries for a new skill. Keep placeholders identical across locales. The CLI defaults to English and accepts `search <query> --lang en|es|ru|zh-CN`.

The validator checks the complete generated offline UI as well as recipe bodies, so regenerate it after changing templates, translations, metadata or scripts. Run the repository's `scripts/build_site.py` to refresh the public pages. Do not add another independent catalog template.

Use protocol/framework versions evidenced by the target repository. Recheck the linked official specification when updating version-sensitive MCP, web rendering or authentication guidance.
