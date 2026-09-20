import test from 'node:test';
import assert from 'node:assert/strict';
import handler from './handler.mjs';

test('accepts the event', async () => {
  const writes = [];
  const env = { STORE: { put: async (...args) => { writes.push(args); } } };
  const response = await handler.fetch(new Request('https://example.invalid', {
    method: 'POST', body: JSON.stringify({ id: 'event-1', value: 'note' })
  }), env, { waitUntil() {} });
  assert.equal(response.status, 201);
  assert.equal(writes.length, 1);
});
