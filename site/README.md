# Public website

The public site is static HTML generated from the plugin's catalog and Markdown instructions. `scripts/build_site.py` writes the GitHub Pages output to `docs/`. Do not edit generated pages directly.

## URLs and languages

- `/vibe-coding/` is English. `/es/`, `/ru/` and `/zh-CN/` contain fully rendered localized landing pages and policies.
- `/vibe-coding/workflows/<id>/` contains a complete English workflow, section anchors, related workflows, a versioned source link and copyable prompts for both hosts.
- Workflow instructions are not represented as translated pages. Their single English canonical URL has no invented language alternates. The prompt language selector changes the prompt, not the document's language or metadata.
- Every localized home/policy page declares reciprocal `hreflang`, a self-canonical URL and an English `x-default`.
- Legacy `?lang=...#workflow-id` catalog links route to the matching new page. The public URL controls the page language; local storage cannot change the indexable English default. The offline catalog retains its saved-language behavior.

## Content and assets

Edit `site/content.json` for landing copy and FAQs. Counts use `{skills}` and `{recipes}`. Edit `plugins/vibe-coding/assets/catalog/locales/<language>.json` for shared catalog labels, titles, summaries, prompts and policies. Update all four languages together. The build checks translation completeness and placeholder parity. English policy text must match root `PRIVACY.md` and `TERMS.md`.

Public styles and JavaScript are versioned with content hashes. The page renders all catalog links and complete workflow instructions without JavaScript. Search fetches the shared full-text index only after a query; if that request fails, title/category filtering still works and shows its limitation. Scripts enhance filtering and copying without supplying the page's core content.

`social-card.svg` is the editable 1200×630 sharing image source. `render_social.py` renders the committed PNG with Pillow and Arial; regenerate it when the title, host support or counts change. Site builds copy the PNG without requiring an image runtime or system fonts in CI.

```sh
python3 -m pip install -r plugins/vibe-coding/requirements.txt -r site/requirements.txt
python3 plugins/vibe-coding/scripts/catalog.py refresh
python3 scripts/build_site.py
python3 -m unittest discover -s tests -v
```

The offline `CATALOG.html` remains self-contained and uses the plugin's catalog renderer. Do not package public site dependencies into the plugin.

## Search and AI-search visibility

`sitemap.xml` lists exactly the canonical, indexable pages. Titles and descriptions derive from maintained copy or each recipe's actual goal/scenario. JSON-LD identifies the website, open-source software, technical articles and breadcrumbs; visible claims and structured metadata must agree. There are no synthetic ratings, hidden keywords, automated doorway pages or special AI schema.

GitHub Pages hosts this project under `/vibe-coding/`. A `robots.txt` at that subpath would have no effect: crawlers consult `https://arty-kk.github.io/robots.txt`. The host-root URL returned 404 on 2026-09-21, so it does not impose a disallow rule. This project does not modify another repository to control that root.

After a release, submit `https://arty-kk.github.io/vibe-coding/sitemap.xml` through a verified Google Search Console or Bing Webmaster Tools property. Those account integrations are not part of the repository. Monitor crawl/index coverage, real-user Core Web Vitals, relevant search queries and AI citation traffic there. Publishing a sitemap is not evidence that a search engine has indexed it or that rankings have improved.

The implementation follows [Google's AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [localized-version guidance](https://developers.google.com/search/docs/specialty/international/localized-versions) and [canonical guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls). Google does not use `llms.txt` for Search; the site exposes its real content through ordinary HTML, links and standard metadata instead.

Before publishing, verify the four locales at desktop/mobile sizes, search, empty results, category/mode filters, legacy links, prompt language/host changes, clipboard behavior and policy navigation. Static tests validate every local link and section fragment, the exact sitemap set, JSON-LD, social metadata, HTML language, prompt templates and deterministic builds.
