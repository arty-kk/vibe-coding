# Changelog

## 1.3.0

- Support Claude Code with a native plugin manifest, a public GitHub marketplace and a repository-root entry for directory distribution. Keep all 46 skills and 241 workflows shared with Codex.
- Add host integration for Codex repository rules, Claude `CLAUDE.md`/scoped rules, Cowork shared files, namespaced skill invocation, relative resource paths and actual tool/permission availability. Remove Codex-only assumptions from planning and probe instructions.
- Add Codex/Claude Code prompt selection in the offline catalog and `--host claude` in CLI search, with English, Spanish, Russian and Simplified Chinese prompts.
- Publish fully rendered landing and policy pages in four languages, plus 241 English workflow pages with complete instructions, section anchors, related workflows and versioned source links.
- Add canonical URLs, reciprocal language alternates, a 253-URL sitemap, software/article/breadcrumb structured data and a 1200×630 social image. Preserve legacy language/hash links.
- Reduce initial English HTML from about 1.58 MB to 132 KB; load full-text search on demand and retain title/category search on network failure.
- Add cross-host packaging, static SEO, link, language, metadata and search-index regression checks, plus native Claude manifest validation in CI. Preserve earlier behavioral records as historical evidence; this release does not claim full model execution in every host or workflow.

## 1.2.0

- Add 13 workflows for API/schema evolution, transactional delivery, build trust, incident response and serverless/edge invocation lifecycles; expand to 46 skills and 241 workflows.
- Rebuild all 20 workflows introduced in 1.1.0 and 1.2.0 around explicit input, domain invariants, evidence rules, operation-specific execution, completion gates and output contracts.
- Make audit priorities and finding acceptance explicit; require owner/consumer completion for implementation and an evidenced passed/failed/blocked verdict for checks.
- Package only an explicitly approved file inventory; block unexpected, sensitive and escaping paths before creating a release archive.
- Parse full YAML metadata and validate catalog fields before use, including clear failures for malformed or duplicate metadata.
- Share ranked multilingual keyword/body search across CLI, website and offline catalog.
- Clarify overlapping skill ownership and preserve previously granted authorization for routine tool operations.
- Add release evaluation records with input/instruction fingerprints, routing cases, real loopback HTTP checks and a real React SSR/browser hydration fixture. External provider and host coverage remains explicitly bounded.

## 1.1.0

- Add MCP server/client and web rendering skills with six focused audit, implementation and verification workflows.
- Add OAuth/OIDC session verification, including transaction binding, issuer/audience checks, replay and refresh behavior.
- Make MCP guidance protocol-version aware, including the 2026-07-28 HTTP changes and legacy compatibility boundaries.
- Ship one English-first, four-language catalog in both the plugin ZIP and website; translate skill UI metadata and add multilingual CLI search/output.
- Remove obsolete task-creation instructions from 22 audits and strengthen localization workflow checks.
- Validate translation completeness, generated UI freshness and independent execution of the packaged catalog.
- Expand to 45 skills and 228 workflows. Two new skill behaviors were exercised in isolated fixtures; transport/host compatibility and browser hydration require their own integration checks.

## 1.0.3

- Improve plugin card color contrast against light backgrounds.

## 1.0.2

- Normalize catalog paths across Windows, macOS and Linux.

## 1.0.1

- Public marketplace installation for Codex.
- 43 skills and 221 workflows covering product, backend, data, infrastructure and AI.
- Portable Agent Plugins manifest and Codex compatibility manifest.
- Searchable catalog, reproducible packaging, validation and CI.
- English and Russian documentation.
