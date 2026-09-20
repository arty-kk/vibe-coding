# Website localization

The website and the plugin's offline `CATALOG.html` use the same templates, scripts and translations in `plugins/vibe-coding/assets/catalog/`. Both default to English and support `en`, `es`, `ru` and `zh-CN`; `?lang=zh` is an alias for Simplified Chinese. A valid URL parameter takes precedence over the saved choice; otherwise English is used regardless of the browser language. Only explicit selector changes are saved.

Edit `plugins/vibe-coding/assets/catalog/locales/<language>.json` for interface strings, workflow titles, domain descriptions, prompt templates and policies. Keep skill names, workflow IDs, placeholders and product names unchanged. Technical recipe instructions remain in English. Update all four locales for a new workflow. The build rejects missing translations, empty values and mismatched placeholders.

The shared renderer is `plugins/vibe-coding/scripts/catalog_site.py`. Counts and versions are derived from the package, including localized descriptions. Policy pages use `site/policy.html`; update the English policy entry to match the root Markdown file and review the other translations when a policy changes.

Run from the repository root:

```sh
python3 -m pip install -r plugins/vibe-coding/requirements.txt
python3 plugins/vibe-coding/scripts/catalog.py refresh
python3 scripts/build_site.py
python3 -m unittest discover -s tests -v
```

Do not edit generated HTML directly. Before publishing, check all four languages on desktop and mobile: search, filters, prompt copying, workflow links, saved preferences and policy navigation. Search ranks titles, translations and explicit keywords above recipe-body matches and ignores accents. CLI, website and offline catalog share the generated index. For the packaged catalog, verify that runtime resources are local and policy links lead to the public website.
