# Contributing

Open an issue for a concrete defect or missing workflow. Include the selected skill, a minimal reproducible scenario, expected behavior and observed result. Remove private code, credentials and personal data.

Keep changes scoped to the rule's owner. Skill descriptions need clear triggers; recipes need a defined operation and observable outcome. Preserve the distinction between inspection and implementation.

Add every new workflow to its skill entrypoint, `catalog.json` and all four locale files under `plugins/vibe-coding/assets/catalog/locales/`. The shared renderer updates both offline and public catalogs; do not create a separate UI or hardcode counts. See [catalog maintenance](site/README.md).

Run from the repository root:

```sh
python3 -m pip install -r plugins/vibe-coding/requirements.txt
python3 plugins/vibe-coding/scripts/catalog.py refresh
python3 scripts/build_site.py
python3 plugins/vibe-coding/scripts/validate.py
python3 -m unittest discover -s tests -v
git diff --check
```

For behavioral changes, add or update a representative scenario under `review/`. State which checks actually ran and which require external services. Submit a focused pull request.

Review new plugin files individually and add approved paths to `plugins/vibe-coding/package-files.json` in sorted order. Validation blocks any unlisted file; never auto-approve the current directory contents as part of a release.

New recipes must define required input, domain invariants, the operation-specific method, evidence rules, completion criteria and an output contract. Audits need impact-based priorities and a finding acceptance gate; implementations need the owner/consumer change contract; checks need a bounded scenario matrix and passed/failed/blocked verdict rules. Evaluate behavior, not just headings or word counts.
