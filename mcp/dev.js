import {createServer} from 'node:http';
import {handleMcp} from './server.js';
import {libraryStatus} from './library.js';

export function startServer(port = 0) {
  const server = createServer(async (incoming, outgoing) => {
    try {
      const chunks = []; let size = 0;
      for await (const chunk of incoming) {
        size += chunk.length;
        if (size > 65536) { outgoing.writeHead(413); outgoing.end('Request too large'); return; }
        chunks.push(chunk);
      }
      const base = `http://127.0.0.1:${server.address().port}`;
      let response;
      if (incoming.url === '/health') response = Response.json(libraryStatus());
      else if (incoming.url === '/mcp') {
        const body = Buffer.concat(chunks);
        const request = new Request(base + incoming.url, {method: incoming.method, headers: incoming.headers,
          ...(['GET', 'HEAD'].includes(incoming.method) ? {} : {body})});
        response = await handleMcp(request);
      } else response = new Response('Not found', {status: 404});
      outgoing.writeHead(response.status, Object.fromEntries(response.headers));
      outgoing.end(Buffer.from(await response.arrayBuffer()));
    } catch {
      outgoing.writeHead(500); outgoing.end('Internal server error');
    }
  });
  return new Promise(resolve => server.listen(port, '127.0.0.1', () => resolve(server)));
}

if (process.argv[1] === new URL(import.meta.url).pathname) {
  const server = await startServer(Number(process.env.PORT || 3105));
  console.log(`Vibe Coding MCP: http://127.0.0.1:${server.address().port}/mcp`);
}
