import http from 'node:http';
import React from 'react';
import {renderToString} from 'react-dom/server';
import {build} from 'esbuild';
import {App} from './App.mjs';
const bundle = await build({entryPoints: ['client.mjs'], bundle: true, write: false, format: 'esm', define: {'process.env.NODE_ENV': '"development"'}});
http.createServer((req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.url === '/client.js') {
    res.setHeader('Content-Type', 'text/javascript');
    res.end(bundle.outputFiles[0].text);
  } else {
    res.setHeader('Content-Type', 'text/html');
    res.end('<!doctype html><html lang="en"><title>Hydration fixture</title><div id="root">' + renderToString(React.createElement(App)) + '</div><p id="errors">Hydration errors: 0</p><pre id="error-detail"></pre><script type="module" src="/client.js"></script></html>');
  }
}).listen(8766, '127.0.0.1', () => console.log('Hydration fixture: http://127.0.0.1:8766'));
