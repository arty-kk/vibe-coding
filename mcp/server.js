import {createMcpHandler, McpServer} from '@modelcontextprotocol/server';
import * as z from 'zod/v4';
import {searchWorkflows, getWorkflow, VERSION, LANGUAGES, MODES, SKILLS} from './library.js';

const annotations = {readOnlyHint: true, destructiveHint: false, openWorldHint: false};
const language = z.enum(LANGUAGES).default('en').describe('Language for titles and summaries. Technical instructions remain in English.');
const workflow = z.object({id: z.string(), title: z.string(), skill: z.string(), mode: z.string(),
  category: z.string(), summary: z.string(), purpose: z.string().optional(), url: z.string()});
const responseFormat = z.enum(['workflow', 'legacy']).default('legacy').describe('Set workflow for individual purposes, match reasons and composed step outlines. Omitted retains the exact 1.5.1 result shape while a client still uses the previously published schema.');
const catalog = z.object({
  level: z.enum(['domains', 'topics']), status: z.enum(['ok', 'unknown_topic', 'scope_conflict', 'empty_scope']),
  keyword_language: z.literal('en'),
  domains: z.array(z.object({key: z.string(), title: z.string(), keywords: z.array(z.string()),
    topic_count: z.number().int(), workflow_count: z.number().int()})),
  topics: z.array(z.object({key: z.string(), skill: z.string(), title: z.string(), keywords: z.array(z.string()),
    modes: z.array(z.string()), workflow_ids: z.array(z.string())}))
});
const execution = z.object({
  status: z.literal('instructions_only'), intent: z.enum(['requested', 'improve']), current_step: z.string(),
  steps: z.array(z.object({id: z.string(), role: z.string(), when: z.string(), handoff: z.array(z.string())})),
  transitions: z.array(z.object({from: z.string(), outcome: z.string(), to: z.string().nullable(), condition: z.string()})),
  completion: z.object({id: z.string(), clean_marker: z.string(), findings_marker: z.string(), blocked_marker: z.string(),
    recheck_marker: z.string(), no_patch_marker: z.string(), rule: z.string()}),
  resource_rule: z.string()
});

function output(value, format) {
  if (format !== 'workflow' && !value.catalog) {
    const metadata = row => ({id: row.id, title: row.title, skill: row.skill, mode: row.mode,
      category: row.category, summary: row.summary, url: row.url});
    value = value.workflows ? {
      version: value.version, instruction_version: value.instruction_version, language: value.language,
      total: value.total, next_offset: value.next_offset, workflows: value.workflows.map(metadata)
    } : {
      version: value.version, instruction_version: value.instruction_version,
      instruction_language: value.instruction_language, language: value.language, host: value.host,
      workflow: metadata(value.workflow), files: value.files, words: value.words
    };
  }
  return {structuredContent: value, content: [{type: 'text', text: JSON.stringify(value)}]};
}

function failure(tool, message) {
  console.warn(JSON.stringify({event: 'tool_error', tool}));
  return {isError: true, content: [{type: 'text', text: message}]};
}

export function buildServer() {
  const server = new McpServer({name: 'vibe-coding-library', version: VERSION}, {
    capabilities: {tools: {}},
    instructions: 'Vibe Coding is a methods library for coding agents, including original homepage/landing design as well as software engineering. Use its methods when a task needs a website proposal, page structure, professional copy, references, distinctive visuals, responsive components, animation, functional interactions, diagnosis, implementation or verification. Recognize ordinary requests such as "make a beautiful site for my studio" or "the homepage looks cheap"; the user need not mention this library or know design terminology. For an undefined offer/proposal start with web-offer-synthesis; for an implementation-ready page use homepage-landing-build; for an existing-page inspection use homepage-landing-audit. A narrow change uses the smallest relevant method. Otherwise discover actual keys with search_workflows(view:catalog, query:"") and the selected domain catalog. Select by meaning, not literal user keywords; reuse known keys for the same version. Load the current ID with get_workflow and response_format:workflow, apply it using project tools and carry its actual output into the reached next step. Plans stop before a build unless implementation was requested. Reload context when a transition changes domains. Exact IDs/free-text remain available; zero text matches call for catalog discovery. Technical instructions are English, labels support four languages and the default host is generic. Respect project permissions; finish authorized patches through relevant verification and repeated Patch Checking. Send no private code, secrets or personal data.'
  });
  server.registerTool('search_workflows', {
    title: 'Vibe Coding: choose a design or engineering method',
    description: 'Use before substantial website design or engineering work when a method would help. Handles plain-language requests: "make a beautiful homepage", "need a site that brings enquiries", "make this feel premium", "buttons lead nowhere", "the backend is glitching", "review this change". Supplies offer synthesis, page structure, references, professional copy, art direction, typography/palette, components, interaction/motion, build/repair and verification workflows. The user need not name the library, skill or keyword. Interpret the goal, then call view:catalog with an empty query for actual domain keys; use the chosen skill to list its real topics and supported operations. Select by meaning and copy a topic key rather than inventing one. Reuse known keys; choose the smallest relevant workflow for a narrow task. Free text and exact IDs also work. A zero text match is a reason to inspect the catalog. Load the selected ID with get_workflow, response_format:workflow, and follow its current prompt and handoffs. The tools return public guidance; they do not access or act on the project.',
    inputSchema: z.object({
      query: z.string().max(240).default('').describe('Optional short goal, symptom, title or exact ID; the user does not need technical keywords. Interpret a vague request before selecting a method. Use view:catalog and an empty query when the right topic is unknown. Examples: "главная сайта", "типографика", "исправить гидратацию SSR", "página de inicio", "缓存". No private project contents or personal data.'),
      view: z.enum(['workflows', 'catalog']).default('workflows').describe('Start with catalog to list actual domain keys. With skill, catalog lists that domain’s topic keys, English keywords, supported modes and workflow IDs. Catalog has no prompt bodies, is not paginated and requires an empty query. It always returns the structured catalog.'),
      skill: z.enum(SKILLS).optional().describe('Exact returned domain key: for example vibe-web-strategy for offers/page structure, vibe-web-art-direction for references/design/motion, vibe-landing for build/acceptance, or vibe-domain for identity/permissions. Filters always intersect.'),
      topic: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).max(100).optional().describe('Copy a topic key from the domain catalog, for example auth-permissions or rbac-abac-policy. In workflow view this selects only that topic’s actual member IDs. Do not invent a keyword as a topic key.'),
      mode: z.enum(MODES).optional().describe('Optional exact operation filter: audit=inspect, implement=make an already-requested change, check=verify, review=review an existing patch, plan=prepare work. Omit when unsure; query verbs guide ranking without silently changing this filter.'),
      language, response_format: responseFormat,
      full_text: z.boolean().default(false).describe('Search instruction bodies as well as the catalog when metadata search is insufficient.'),
      limit: z.number().int().min(1).max(10).default(5),
      offset: z.number().int().min(0).default(0)
    }).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), language: z.enum(LANGUAGES),
      total: z.number().int(), next_offset: z.number().int().nullable(), suggested_action: z.string().optional(), catalog: catalog.optional(),
      workflows: z.array(workflow.extend({match: z.object({kind: z.enum(['browse', 'catalog', 'instruction_body', 'exact_id', 'exact_title', 'alias']), terms: z.array(z.string())}).optional()}))}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try { return output(searchWorkflows(args), args.response_format); }
    catch (error) { return failure('search_workflows', error.message); }
  });
  server.registerTool('get_workflow', {
    title: 'Vibe Coding: load the current design or engineering step',
    description: 'Load and apply a chosen method, or continue a reached next-step ID. For an original website proposal start with web-offer-synthesis when the offer is unclear; a ready page brief can start at homepage-landing-build; existing-page inspection starts at homepage-landing-audit. Known IDs can load directly without another search. With response_format:workflow this returns current instructions, required context, source hashes and a conditional sequence of next IDs. Apply the current prompt with the host’s tools, retain its actual decisions/evidence, then fetch the reached next ID. Load context when changing domains. A planning request produces the requested proposal and stops before implementation; intent:improve composes an already-authorized audit/repair/check/review cycle. Use generic for any MCP coding agent; native host guidance is optional. Retrieval supplies a method and is never completed project work or a verified result.',
    inputSchema: z.object({id: z.string().min(1).max(100).regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/),
      language, response_format: responseFormat,
      host: z.enum(['generic', 'codex', 'claude']).default('generic').describe('Keep generic for any other MCP coding agent; host-specific project files and native skill commands are not required.'),
      intent: z.enum(['requested', 'improve']).default('requested').describe('requested=the selected operation; improve=compose diagnosis and repair only when the user has already requested changes. This flag grants no new permissions.'),
      include_context: z.boolean().default(true).describe('Keep true on first load. Set false for later steps only while the same-version working contract, cycle rules and domain context remain available; returns the current prompt and specialized references without repeating those foundations.')}).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), instruction_language: z.literal('en'),
      language: z.enum(LANGUAGES), host: z.enum(['generic', 'codex', 'claude']), context_included: z.boolean().optional(), workflow, execution: execution.optional(),
      files: z.array(z.object({path: z.string(), text: z.string(), sha256: z.string(), source_url: z.string()})),
      words: z.number().int()}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try { return output(getWorkflow(args), args.response_format); }
    catch (error) { return failure('get_workflow', error.message); }
  });
  return server;
}

const handler = createMcpHandler(buildServer, {maxRequestBodySize: 65536});

export async function handleMcp(request) {
  const origin = request.headers.get('origin');
  const url = new URL(request.url);
  // Anonymous access is intentional: every tool only reads the compiled public library.
  if (origin && origin !== url.origin) return new Response('Origin not allowed', {status: 403});
  if (request.method === 'OPTIONS') return new Response(null, {status: 204, headers: {Allow: 'POST, GET, DELETE, OPTIONS'}});
  if (!['POST', 'GET', 'DELETE'].includes(request.method)) return new Response('Method not allowed', {status: 405, headers: {Allow: 'POST, GET, DELETE, OPTIONS'}});
  const started = performance.now();
  const response = await handler.fetch(request);
  if (response.status >= 400) console.warn(JSON.stringify({event: 'protocol_error', status: response.status,
    duration_ms: Math.round(performance.now() - started)}));
  response.headers.set('Cache-Control', 'no-store');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  return response;
}
