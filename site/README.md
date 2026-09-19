# Website localization

The public website defaults to English. The language selector supports `en`, `es`, `ru` and `zh-CN`; `?lang=zh` is also accepted for Simplified Chinese. A valid URL parameter takes precedence over the saved language. Without either, English is used regardless of the browser's language. Only explicit selector changes are saved in local storage.

Edit `locales/<language>.json` for interface strings, all 221 workflow titles, domain descriptions, prompt templates and policies. Keep skill names, workflow IDs, placeholders and product names unchanged. The technical instructions shown in the expandable section come directly from the plugin and remain in English.

Update all four locale files when adding a workflow. The build rejects missing translations, empty values and mismatched prompt placeholders. If a policy changes, update its English entry to match the root Markdown file and review the three translations.

Run from the repository root:

```sh
python3 scripts/build_site.py
python3 -m unittest discover -s tests -v
```

Generated pages live in `docs/`. Templates, CSS and JavaScript live here; do not edit the generated pages directly. The website build does not alter the published plugin package.

Before publishing, check all four languages on desktop and mobile: search, filters, prompt copying, a workflow deep link, language persistence and policy navigation. Search matches every translation and ignores accents, so a language change preserves the active search and filters.
