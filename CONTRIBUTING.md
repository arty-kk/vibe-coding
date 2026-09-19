# Contributing

Open an issue for a concrete defect or missing workflow. Include the selected skill, a minimal reproducible scenario, expected behavior and observed result. Remove private code, credentials and personal data.

Keep changes scoped to the rule's owner. Skill descriptions need clear triggers; recipes need a defined operation and observable outcome. Preserve the distinction between inspection and implementation.

Run from the repository root:

```sh
python3 plugins/vibe-coding/scripts/catalog.py refresh
python3 scripts/build_site.py
python3 plugins/vibe-coding/scripts/validate.py
python3 -m unittest discover -s tests -v
git diff --check
```

For behavioral changes, add or update a representative scenario under `review/`. State which checks actually ran and which require external services. Submit a focused pull request.
