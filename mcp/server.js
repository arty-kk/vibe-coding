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
    instructions: 'Vibe Coding supplies engineering workflows for coding agents. When the appropriate workflow/topic is not already known, use search_workflows with view:catalog and an empty query to see actual domain keys. Choose a domain by meaning, then request its catalog with skill:<returned key>. Select a real topic key and requested mode, then search workflows by that topic and load a returned ID with get_workflow. Keywords are canonical English; catalog labels support four languages. Reuse discovered keys for the same library version. Do not invent keywords, treat zero text matches as a missing capability, or dump all instructions. Exact IDs and free-text search remain available. Use response_format:workflow for workflow results and step outlines. Execute guidance with project tools, existing permissions and evidence handoffs; repeat Patch Checking after corrections until a real clean pass or blocker. Default host is generic. Send no private code, secrets or personal data.'
  });
  server.registerTool('search_workflows', {
    title: 'Vibe Coding: choose a method for a coding task',
    description: 'Find a method for a coding task: bug diagnosis, implementation, review, planning or verification. Before inventing a search term, call view:catalog with an empty query to list actual domain keys; call it again with the chosen skill to get topic keys, English keywords, supported modes and workflow IDs. Select by the meaning of the user’s request, then use topic:<returned key> and mode to retrieve exact members. Reuse known keys for the same version. The calling model maps the user’s language to those fixed keys; no separate embedding API is required. Free-text queries in English, Spanish, Russian and Simplified Chinese and exact IDs also work. Use response_format:workflow for purposes and match reasons. Zero text matches mean use the catalog, not abandon the task. Load a returned ID with get_workflow. Catalogs contain metadata only; the tools do not inspect user files or perform project actions.',
    inputSchema: z.object({
      query: z.string().max(240).default('').describe('Optional free-text goal, symptom, title or exact ID; empty browses workflow records. Agents should discover catalog keys first when the topic is unknown. Examples: "исправить гидратацию SSR", "verificar reintentos de pagos", "缓存". No code, private file contents, secrets or personal data.'),
      view: z.enum(['workflows', 'catalog']).default('workflows').describe('Start with catalog to list actual domain keys. With skill, catalog lists that domain’s topic keys, English keywords, supported modes and workflow IDs. Catalog has no prompt bodies, is not paginated and requires an empty query. It always returns the structured catalog.'),
      skill: z.enum(SKILLS).optional().describe('Exact domain key returned by catalog, such as vibe-domain for application identity and permissions. Filters always intersect.'),
      topic: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).max(100).optional().describe('Copy a topic key from the domain catalog, for example auth-permissions or rbac-abac-policy. In workflow view this selects only that topic’s actual member IDs. Do not invent a keyword as a topic key.'),
      mode: z.enum(MODES).optional().describe('Optional exact operation filter: audit=inspect, implement=make an already-requested change, check=verify, review=review an existing patch, plan=prepare work. Omit when unsure; query verbs guide ranking without silently changing this filter.'),
      language, response_format: responseFormat,
      full_text: z.boolean().default(false).describe('Search instruction bodies as well as the catalog when metadata search is insufficient.'),
      limit: z.number().int().min(1).max(10).default(5),
      offset: z.number().int().min(0).max(240).default(0)
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
    title: 'Vibe Coding: load the next engineering workflow step',
    description: 'Get the actionable engineering instructions after choosing a result from search_workflows, or load a next-step ID from a previously returned execution outline. Use the returned file text as the method for your coding task with your own repository tools. With response_format:workflow, returns the current prompt, required foundations, source hashes and an execution outline with ordered/conditional next IDs, evidence handoffs and repair/recheck exits. Only the current prompt body is loaded; fetch later IDs when their transitions are reached. For an already-authorized audit-and-fix task, intent:improve composes audit → repair → relevant check → repeated Patch Checking; requested preserves a read-only audit/check/plan scope. A known implementation starts at its implementation ID. The library works with any coding agent: default host is generic, Codex/Claude additions are optional. Retrieval is instructions only, never an executed check or a clean verdict.',
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
