import library from './generated/library.json' with { type: 'json' };
import engine from './generated/catalog-engine.js';
import {buildExecution} from './workflow.js';
import {createDiscovery} from './discovery.js';
import {VERSION, INSTRUCTION_VERSION, MODES, SKILLS} from './metadata.js';

export {LANGUAGES, MODES, SKILLS, VERSION, DIGEST, INSTRUCTION_VERSION, libraryStatus} from './metadata.js';
const byId = new Map(library.recipes.map(row => [row.id, row]));
const discovery = createDiscovery(library);
const topics = Object.fromEntries(SKILLS.map(skill => [skill,
  Object.values(library.locales).map(locale => locale.categories[skill])]));
const actions = Object.fromEntries(MODES.map(mode => [mode, Object.values(library.locales).map(locale => locale.modes[mode])]));
let prepared;
let bodies;

function metadata(row, language) {
  const locale = library.locales[language];
  return {id: row.id, title: locale.titles[row.id], skill: row.skill, mode: row.mode,
    category: locale.categories[row.skill], summary: locale.summaries[row.skill], purpose: row.purpose,
    url: `https://arty-kk.github.io/vibe-coding/workflows/${row.id}/`};
}

function rankWorkflows(query, {skill = '', mode = '', full_text = false} = {}) {
  prepared ??= engine.prepare(library.recipes.map(row => ({...row,
    titles: Object.values(library.locales).map(locale => locale.titles[row.id])})), topics, actions, library.searchLexicon);
  if (full_text && !bodies) {
    bodies = Object.fromEntries(library.recipes.map(row => [row.id, {
      body: library.files[row.path].text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    }]));
  }
  return engine.select(prepared, {q: query, topic: skill, action: mode, full: full_text}, bodies).matches;
}

export function searchWorkflows({query = '', skill, mode, topic, view = 'workflows', language = 'en', full_text = false, limit = 5, offset = 0}) {
  if (skill && !SKILLS.includes(skill)) throw new Error('Unknown skill. Use a skill identifier returned by search_workflows.');
  if (view === 'catalog' || topic && !discovery.byTopic.has(topic)) {
    if (view === 'catalog' && query.trim()) throw new Error('Catalog view lists available keys. Leave query empty, choose a returned skill/topic key, then use view:workflows to search.');
    const catalog = discovery.catalog({skill, mode, topic, language});
    return {version: VERSION, instruction_version: INSTRUCTION_VERSION, language,
      total: view === 'catalog' ? (catalog.level === 'domains' ? catalog.domains.length : catalog.topics.length) : 0,
      next_offset: null, workflows: [], catalog,
      suggested_action: catalog.status === 'unknown_topic'
        ? 'The supplied topic key does not exist. Choose a key from this actual catalog; do not invent a keyword or stop at the unknown key.'
        : catalog.status === 'scope_conflict'
          ? 'That topic does not support the supplied domain/operation combination. The catalog lists alternatives within the same explicit scope; select one only if it fits the task.'
        : catalog.status === 'empty_scope'
          ? 'No catalog topics support these domain/operation filters. Preserve explicit user constraints. Check whether your inferred operation/domain was correct; do not substitute an unrelated workflow.'
        : catalog.level === 'domains'
          ? 'Choose the domain key that fits the user’s goal, then call search_workflows with view:catalog and skill:<that key>. The catalog contains metadata only, not prompt bodies.'
          : 'Choose a returned topic key and call search_workflows with topic:<that key> and the requested mode. Reuse known keys for this library version. Then load a returned workflow ID with get_workflow.'};
  }
  const matches = rankWorkflows(query, {skill, mode, full_text});
  const scoped = topic ? matches.filter(({entry}) => discovery.byTopic.get(topic).recipe_ids.includes(entry.id)) : matches;
  const page = scoped.slice(offset, offset + limit);
  return {version: VERSION, instruction_version: INSTRUCTION_VERSION, language, total: scoped.length,
    next_offset: offset + page.length < scoped.length ? offset + page.length : null,
    workflows: page.map(({entry, match}) => ({...metadata(entry, language), match: {kind: match.kind, terms: match.terms}})),
    suggested_action: page.length
      ? 'Choose the workflow whose purpose and operation fit the task, then call get_workflow with its ID and response_format:workflow. Titles are localized; the purpose and instructions are English. This search has not inspected your project.'
      : 'Retry with a short technical area and one concrete symptom. If the area is unclear, use view:catalog with an empty query to choose a listed domain or topic. Keep the supplied filters. If the client lacks view:catalog, browse with an empty query and the same filters.'};
}

function workflowForQuery(query) {
  const [first, second] = rankWorkflows(query);
  if (!first) throw new Error('No workflow matches that goal. Retry with one technical area and one symptom, or browse domains with search_workflows.');
  if (second?.match.score === first.match.score) {
    throw new Error('Several workflows match equally. Compare them with search_workflows or specify the goal or symptom more precisely.');
  }
  return first.entry.id;
}

export function getWorkflow({id, query, language = 'en', host = 'generic', intent = 'requested', include_context = true}) {
  const hasId = id !== undefined;
  if (hasId ? query !== undefined : !query?.trim()) throw new Error('Provide one workflow ID or one nonempty task description.');
  const identity = hasId ? id : workflowForQuery(query.trim());
  const row = byId.get(identity);
  if (!row) throw new Error('Unknown workflow ID. Search the public library with search_workflows first.');
  const foundation = ['references/workflow.md', 'references/cycles.md', `skills/${row.skill}/SKILL.md`];
  const paths = [...new Set([...(include_context ? foundation : []), row.path,
    ...row.dependencies.filter(path => include_context || !foundation.includes(path)),
    ...(host === 'generic' || !include_context ? [] : ['references/hosts.md'])])];
  const files = paths.map(path => ({...library.files[path],
    source_url: `https://github.com/arty-kk/vibe-coding/blob/v${INSTRUCTION_VERSION}/plugins/vibe-coding/${path}`}));
  return {version: VERSION, instruction_version: INSTRUCTION_VERSION, instruction_language: 'en',
    language, host, context_included: include_context, workflow: metadata(row, language), files,
    execution: buildExecution(library, identity, intent),
    words: files.reduce((count, file) => count + file.text.trim().split(/\s+/u).length, 0)};
}
