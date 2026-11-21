import {createMcpHandler, McpServer} from '@modelcontextprotocol/server';
import * as z from 'zod/v4';
import {searchWorkflows, getWorkflow, VERSION, LANGUAGES, MODES, SKILLS} from './library.js';

const annotations = {readOnlyHint: true, destructiveHint: false, openWorldHint: false};
const instructions = [
  'Vibe Coding provides engineering workflows for planning or building a website, improving an existing page, diagnosing a software symptom, and preparing or reviewing a patch.',
  'At the start of one of these tasks, find a workflow from the user’s ordinary goal or symptom with search_workflows. This includes a website plan or architecture question that asks for no edits. Examples include "I want a nice site for my studio; what sections do I need?" and "the backend sometimes hangs after I submit the form."',
  'Use a short description in the user’s language, then load the matching ID with get_workflow and response_format:workflow before completing the requested work. A known matching ID can be loaded directly. Follow the current step and fetch further steps when reached.',
  'If the first search is empty, inspect the catalog within the requested scope. Apply the workflow with the host’s tools and permissions. Keep plans read-only. Send only public technical goals or symptoms.'
].join(' ');
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
    instructions
  });
  server.registerTool('search_workflows', {
    title: 'Find a workflow for a site plan, design, bug or patch',
    description: 'Find the method to start a website plan or build, improve an existing page, investigate a software bug, or prepare or review a patch. Use at the start of these tasks from the goal or symptom in the user’s words, including planning questions without edits. For example, "какие разделы нужны красивому сайту студии", "бэкэнд глючит, форма висит", or "how should I structure this app?". Send a short public description as query; special terms or a library mention are unnecessary. The result ranks applicable workflow IDs. Load a matching ID with get_workflow. Use view:catalog with an empty query to recover from no match or browse known domains and topics. Read-only public guidance; keep source code, credentials and personal data out of queries.',
    inputSchema: z.object({
      query: z.string().max(240).default('').describe('Short task or symptom in ordinary language, a title, or an exact ID. Keep the purpose and relevant symptom or constraint. Example: "хочу красивый сайт, какие разделы нужны?". Omit source code, credentials and personal data.'),
      view: z.enum(['workflows', 'catalog']).default('workflows').describe('Workflows ranks a task description by default. Catalog lists domain keys, or topic keys and workflow IDs for the supplied skill. Catalog requires an empty query and returns metadata only.'),
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
    title: 'Load the workflow for the current task or step',
    description: 'Load a matching workflow to guide the requested plan, build, diagnosis or review. Pass the ID from search_workflows, or load a known matching ID directly. Start an undefined website offer at web-offer-synthesis, a question about sections at web-page-architecture, a stack or modular code layout at web-project-architecture, an existing homepage inspection at homepage-landing-audit, and a vague backend hang at instant-backend-probe. Use response_format:workflow for instructions and conditional next IDs. Apply the current step with the host’s tools, carry forward actual evidence, and fetch subsequent steps when reached. The tool returns instructions and does not execute the workflow.',
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
