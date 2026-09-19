import test from 'node:test';
import assert from 'node:assert/strict';
import { renameProject } from './actions.mjs';
import { loadProjectPage } from './page.mjs';
import { projects, reset } from './data.mjs';
import { withUser } from './session.mjs';

test('owner can load and rename a project', async () => {
  reset();
  await withUser({ id: 'alice' }, async () => {
    const page = loadProjectPage('p1');
    const result = await renameProject({ ...page.formDefaults, title: ' New roadmap ' });
    assert.equal(result.title, 'New roadmap');
    assert.equal(projects.get('p1').title, 'New roadmap');
  });
});

test('another user cannot open the project page', () => {
  reset();
  withUser({ id: 'bob' }, () => assert.throws(() => loadProjectPage('p1'), /Forbidden/));
});

test('blank title is rejected', async () => {
  reset();
  await withUser({ id: 'alice' }, async () => {
    await assert.rejects(renameProject({ projectId: 'p1', actorId: 'alice', title: ' ' }), /Invalid title/);
    assert.equal(projects.get('p1').title, 'Roadmap');
  });
});
