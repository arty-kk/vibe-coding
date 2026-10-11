import library from './generated/library.json' with { type: 'json' };
import engine from './generated/catalog-engine.js';

export const LANGUAGES = ['en', 'es', 'ru', 'zh-CN'];
export const MODES = [...new Set(library.recipes.map(row => row.mode))].sort();
export const SKILLS = [...new Set(library.recipes.map(row => row.skill))].sort();
export const VERSION = library.version;
export const DIGEST = library.digest;
export const INSTRUCTION_VERSION = library.instructionVersion;
const byId = new Map(library.recipes.map(row => [row.id, row]));
const topics = Object.fromEntries(SKILLS.map(skill => [skill,
  Object.values(library.locales).flatMap(locale => [locale.categories[skill], locale.summaries[skill]])]));
const actions = Object.fromEntries(MODES.map(mode => [mode, Object.values(library.locales).map(locale => locale.modes[mode])]));
const prepared = engine.prepare(library.recipes.map(row => ({...row,
  titles: Object.values(library.locales).map(locale => locale.titles[row.id])})), topics, actions);
const bodies = Object.fromEntries(library.recipes.map(row => [row.id, {body: library.files[row.path].text}]));

function metadata(row, language) {
  const locale = library.locales[language];
  return {id: row.id, title: locale.titles[row.id], skill: row.skill, mode: row.mode,
    category: locale.categories[row.skill], summary: locale.summaries[row.skill],
    url: `https://arty-kk.github.io/vibe-coding/workflows/${row.id}/`};
}

export function searchWorkflows({query = '', skill, mode, language = 'en', full_text = false, limit = 5, offset = 0}) {
  if (skill && !SKILLS.includes(skill)) throw new Error('Unknown skill. Use a skill identifier returned by search_workflows.');
  const {matches} = engine.select(prepared, {q: query, topic: skill || '', action: mode || '', full: full_text}, bodies);
  const page = matches.slice(offset, offset + limit);
  return {version: VERSION, instruction_version: INSTRUCTION_VERSION, language, total: matches.length,
    next_offset: offset + page.length < matches.length ? offset + page.length : null,
    workflows: page.map(({entry}) => metadata(entry, language))};
}

export function getWorkflow({id, language = 'en', host = 'generic'}) {
  const row = byId.get(id);
  if (!row) throw new Error('Unknown workflow ID. Search the public library with search_workflows first.');
  const paths = [...new Set(['references/workflow.md', `skills/${row.skill}/SKILL.md`, row.path,
    ...row.dependencies, ...(host === 'generic' ? [] : ['references/hosts.md'])])];
  const files = paths.map(path => ({...library.files[path],
    source_url: `https://github.com/arty-kk/vibe-coding/blob/v${INSTRUCTION_VERSION}/plugins/vibe-coding/${path}`}));
  return {version: VERSION, instruction_version: INSTRUCTION_VERSION, instruction_language: 'en',
    language, host, workflow: metadata(row, language), files,
    words: files.reduce((count, file) => count + file.text.trim().split(/\s+/u).length, 0)};
}

export function libraryStatus() {
  return {service: 'Vibe Coding Library', version: VERSION, instruction_version: INSTRUCTION_VERSION,
    workflows: library.recipes.length, skills: library.skillCount, digest: DIGEST,
    tools: ['search_workflows', 'get_workflow'], authentication: 'none'};
}
