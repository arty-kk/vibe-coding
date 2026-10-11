import {createMcpHandler, McpServer} from '@modelcontextprotocol/server';
import * as z from 'zod/v4';
import {searchWorkflows, getWorkflow, VERSION, LANGUAGES, MODES} from './library.js';

const annotations = {readOnlyHint: true, destructiveHint: false, openWorldHint: false};
const language = z.enum(LANGUAGES).default('en').describe('Language for titles and summaries. Technical instructions remain in English.');
const workflow = z.object({id: z.string(), title: z.string(), skill: z.string(), mode: z.string(),
  category: z.string(), summary: z.string(), url: z.string()});

function output(value) {
  return {structuredContent: value, content: [{type: 'text', text: JSON.stringify(value)}]};
}

function failure(tool, message) {
  console.warn(JSON.stringify({event: 'tool_error', tool}));
  return {isError: true, content: [{type: 'text', text: message}]};
}

export function buildServer() {
  const server = new McpServer({name: 'vibe-coding-library', version: VERSION}, {
    capabilities: {tools: {}},
    instructions: 'Search the public engineering library with concise technical keywords. Load one selected workflow by its returned ID. Use it with the user’s requested operation and the project’s instructions. These tools return guidance; they do not read, audit or modify the user’s repository. Do not send source code, credentials or personal data as a search query.'
  });
  server.registerTool('search_workflows', {
    title: 'Find engineering workflows',
    description: 'Find relevant Vibe Coding workflows in a bounded public library of 241 recipes. Use 2–6 technical keywords, a known workflow ID, or an empty query to browse. Search understands English, Spanish, Russian and Simplified Chinese catalog terms. Filter by the requested operation; return at most 10 concise matches, then use get_workflow for one selected ID. Does not search the internet or user files.',
    inputSchema: z.object({
      query: z.string().max(160).default('').describe('Technical keywords only; no code, credentials, file contents or personal data.'),
      skill: z.string().regex(/^vibe-[a-z-]+$/).max(64).optional().describe('Optional skill identifier, such as vibe-sql or vibe-backend.'),
      mode: z.enum(MODES).optional().describe('The requested operation; audit means inspection and implement means authorized changes.'),
      language, full_text: z.boolean().default(false).describe('Search instruction bodies as well as the catalog when metadata search is insufficient.'),
      limit: z.number().int().min(1).max(10).default(5),
      offset: z.number().int().min(0).max(240).default(0)
    }).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), language: z.enum(LANGUAGES),
      total: z.number().int(), next_offset: z.number().int().nullable(), workflows: z.array(workflow)}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try { return output(searchWorkflows(args)); }
    catch (error) { return failure('search_workflows', error.message); }
  });
  server.registerTool('get_workflow', {
    title: 'Load an engineering workflow',
    description: 'Load one exact Vibe Coding workflow ID returned by search_workflows. Returns its selected recipe, domain skill, working contract, directly required shared references and source hashes. Technical instructions are in English; titles and summaries support four languages. Host-specific instructions are included only when host is explicitly selected. Returns guidance for the agent to apply in the user’s authorized environment; does not inspect or modify a repository.',
    inputSchema: z.object({id: z.string().min(1).max(100).regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/),
      language, host: z.enum(['generic', 'codex', 'claude']).default('generic')}).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), instruction_language: z.literal('en'),
      language: z.enum(LANGUAGES), host: z.enum(['generic', 'codex', 'claude']), workflow,
      files: z.array(z.object({path: z.string(), text: z.string(), sha256: z.string(), source_url: z.string()})),
      words: z.number().int()}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try { return output(getWorkflow(args)); }
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
