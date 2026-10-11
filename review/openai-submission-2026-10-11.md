# OpenAI distribution 1.4.1

The OpenAI package uses a platform-neutral listing and imports the version's release notes. The shared package, website, host compatibility, skill names and workflow IDs remain the same. Only `plugin.json` and `.codex-plugin/plugin.json` differ in this distribution.

Build and check the distribution:

```sh
python3 scripts/package_openai.py --output dist/vibe-coding-1.4.1-openai.zip
python3 -m unittest discover -s tests -p test_openai_distribution.py -v
```

The builder checks the applicable final-directory limits before packaging and rejects credentials in listing URLs, invalid metadata characters, duplicate prompts, escaping icons and runtime declarations in the skills-only package. The dedicated CI workflow runs these checks for changes to the package or distribution builder.

| Area | Verified result |
|---|---|
| Package identity | Existing `vibe-coding` plugin; version `1.4.1` |
| Listing | Supported category; bounded names, descriptions and starter prompts |
| Support and policies | Four public HTTPS listing URLs; privacy text explains hosting, host services, preferences, retention and controls |
| Assets | Contained PNG icons meet dimensions, size and color-contrast checks |
| Skills | 46 entrypoints and 241 focused recipes; 297 instruction fingerprints preserved |
| Runtime | No MCP, app, hook, screenshot or credential configuration added |
| Validation | 51 Python tests pass; extracted package validates |
| Reproducibility | Two package builds produce identical bytes and SHA256 |
| Portal import | All 372 files match the shared source after normalizing the portal's flattened root |
| Current portal | All 46 skill checks pass; no non-blocking metadata findings remain |

OpenAI distribution SHA256:

```text
17a36443193c2affd9036102e7cd3708dd88a8b9ec3479e7c11ec60eab41afea
```

The remaining portal finding is an eligibility restriction: “We are not accepting more skills-only submissions at this time.” Version 1.3.0 remains published and 1.4.1 remains a draft. This is not a package-validation failure or a completed review rejection. The eligibility of this existing-plugin update needs an OpenAI decision; package changes and successful scans do not grant it.

Publisher identity verification, rights, legal compliance and policy attestations remain publisher responsibilities. The portal's legal confirmations require the publisher's confirmation at submission time. This record does not assert directory approval or model execution across every workflow.

Applicable references, checked on 2026-10-11: [submission and updates](https://developers.openai.com/plugins/deploy/submission), [final metadata constraints](https://developers.openai.com/plugins/deploy/submission-errors), [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines), [skills](https://developers.openai.com/plugins/build/skills).
