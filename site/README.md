# Public website

The public site is static HTML generated from the plugin's catalog and Markdown instructions. `scripts/build_site.py` writes the GitHub Pages output to `docs/`. Do not edit generated pages directly.

## URLs and languages

- `/vibe-coding/` is English. `/es/`, `/ru/` and `/zh-CN/` contain fully rendered localized landing pages, topic directories and policies.
- `/vibe-coding/workflows/` and its localized equivalents list every workflow grouped by topic, with ordinary links and no search or pagination dependency. Landing pages and the footer link to these directories; article breadcrumbs match the same hierarchy.
- `/vibe-coding/workflows/<id>/` contains a complete English workflow, section anchors, related workflows, a versioned source link and copyable prompts for both hosts.
- Workflow instructions are not represented as translated pages. Their single English canonical URL has no invented language alternates. The prompt language selector changes the prompt, not the document's language or metadata.
- Every localized home/directory/policy page declares reciprocal `hreflang`, a self-canonical URL and an English `x-default`.
- Legacy `?lang=...#workflow-id` catalog links route to the matching new page. The public URL controls the page language; local storage cannot change the indexable English default. The offline catalog retains its saved-language behavior.

## Content and assets

Edit `site/content.json` for landing copy and FAQs. Counts use `{skills}` and `{recipes}`. Edit `plugins/vibe-coding/assets/catalog/locales/<language>.json` for shared catalog labels, titles, summaries, prompts and policies. Update all four languages together. The build checks translation completeness and placeholder parity. English policy text must match root `PRIVACY.md` and `TERMS.md`.

Public styles are independent of the offline catalog. The page renders every workflow link, localized description and full technical instruction without JavaScript. The interactive view displays 12 results per page, starting with 12 varied engineering tasks defined in `site/content.json`.

`site/catalog-engine.js` owns Unicode normalization, word-prefix matching, weighted ranking, intersecting filters, facet counts, pagination and safe return URLs. Default search uses multilingual titles, curated keywords, topics and task names. It does not mix in incidental mentions from long technical instructions. The explicit “Search inside instructions” option fetches the shared full-text index; those matches are labeled. Loading failures leave the ordinary search operational. Disabling full-text search ignores any cached body matches.

`q`, `topic`, `action`, `full` and `page` belong to the URL. Search edits replace history; filter and pagination changes add navigable history entries. These are views of a single complete catalog, not separately indexable paginated HTML documents. The static topic directory provides the full collection at a stable canonical URL.

Language links and workflow return links preserve the selection. Their `href` attributes stay canonical during initial rendering and filtering; optional navigation parameters are attached on click, middle-click or context-menu activation. Quick filters use buttons. Shared parameterized URLs still declare the clean canonical page. Invalid filters and page values are normalized. Search handles composition events and supports clearing only the query or each filter independently.

Scripts and styles use content hashes. Keep previously published assets: cached pages and already-open tabs may request an older script or lazily load its index after deployment. Builds preserve them instead of breaking those sessions.

`social-card.svg` is the editable 1200×630 sharing image source. `render_social.py` renders the committed PNG with Pillow and Arial; regenerate it when the title, host support or counts change. Site builds copy the PNG without requiring an image runtime or system fonts in CI.

```sh
python3 -m pip install -r plugins/vibe-coding/requirements.txt -r site/requirements.txt
python3 plugins/vibe-coding/scripts/catalog.py refresh
python3 scripts/build_site.py
python3 -m unittest discover -s tests -v
node --test tests/test_site_search.cjs
```

The offline `CATALOG.html` remains self-contained and uses the plugin's catalog renderer. Do not package public site dependencies into the plugin.

## Search and AI-search visibility

`sitemap.xml` lists exactly the canonical, indexable pages. Titles and descriptions derive from maintained copy or each recipe's actual goal/scenario. Policy descriptions are localized plain text, not raw Markdown. JSON-LD identifies the website, maintainer, open-source software, topic collections, technical articles and breadcrumbs. Articles point to their actual versioned source; policy pages do not claim the software itself is their main content. Visible claims and structured metadata must agree. There are no synthetic ratings, hidden keywords, automated doorway pages or special AI schema.

GitHub Pages hosts this project under `/vibe-coding/`. A `robots.txt` at that subpath would have no effect: crawlers consult `https://arty-kk.github.io/robots.txt`. The host-root URL returned 404 on 2026-09-21, so it does not impose a disallow rule. This project does not modify another repository to control that root.

After a release, submit `https://arty-kk.github.io/vibe-coding/sitemap.xml` through a verified Google Search Console or Bing Webmaster Tools property. Those account integrations are not part of the repository. Monitor crawl/index coverage, real-user Core Web Vitals, relevant search queries and AI citation traffic there. Publishing a sitemap is not evidence that a search engine has indexed it or that rankings have improved.

In Search Console, inspect Settings → Search generative AI for this URL-prefix property and any inherited parent setting. [Google's inclusion control](https://support.google.com/webmasters/answer/16908024) defaults to inclusion, but the live account setting cannot be inferred from HTML. [Bing AI Performance](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) reports citations rather than clicks or guaranteed placement. Neither account was connected during the website audit; do not report their results as checked. IndexNow can be added later for change notifications to participating engines; it is not a substitute for Google Search Console.

The implementation follows [Google's AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [localized-version guidance](https://developers.google.com/search/docs/specialty/international/localized-versions) and [canonical guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls). Google does not use `llms.txt` for Search; the site exposes its real content through ordinary HTML, links and standard metadata instead.

Before publishing, verify the four locales at desktop/mobile sizes, search, empty results, category/mode filters, legacy links, prompt language/host changes, clipboard behavior and policy navigation. Static tests validate every local link and section fragment, the exact sitemap set, JSON-LD, social metadata, HTML language, prompt templates and deterministic builds. Node regression tests cover ranking, body-search isolation, multilingual matching, filter intersections and counts, empty results, URL restoration, pagination and safe return links. Browser checks must also cover navigation back from a workflow, changing language with filters, keyboard focus, copy actions and the missing-index failure state.
