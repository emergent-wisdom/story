import test from 'node:test';
import assert from 'node:assert/strict';
import { openStory } from '../open-model.mjs';

const graphId = 'rabbit-hole-novel';
const graphHash = 'a'.repeat(64);
const head = { graphId, graphHash, revision: 158 };

test('opens the declared current saved head through the public MCP', async () => {
  const calls = [];
  const opened = await openStory(async (name, args) => {
    calls.push({ name, args });
    return name === 'life_saved_work_list'
      ? { heads: [head], window: { nextOffset: null } }
      : { graphHash, url: 'http://127.0.0.1:5000/example/', mode: 'live' };
  });
  assert.equal(opened.graphHash, graphHash);
  assert.deepEqual(calls.map((call) => call.name), ['life_saved_work_list', 'life_model_viewer_open']);
  assert.deepEqual(calls[1].args, { graphHash, accessScopes: ['story-author'], mode: 'live' });
});

test('finishes catalog paging before deciding whether the story has one head', async () => {
  const pages = [];
  await assert.rejects(openStory(async (name, args) => {
    assert.equal(name, 'life_saved_work_list');
    pages.push(args.offset);
    return args.offset === 0 ? { heads: [head], window: { nextOffset: 25 } }
      : { heads: [{ ...head, graphHash: 'b'.repeat(64) }], window: { nextOffset: null } };
  }), /2 branch heads/);
  assert.deepEqual(pages, [0, 25]);
});

test('does not treat an unrelated author life as the story', async () => {
  await assert.rejects(openStory(async () => ({ heads: [{ ...head, graphId: 'author-life' }], window: { nextOffset: null } })), /No visible saved story/);
});

test('refuses a viewer for a different revision', async () => {
  await assert.rejects(openStory(async (name) => name === 'life_saved_work_list'
    ? { heads: [head], window: { nextOffset: null } }
    : { graphHash: 'b'.repeat(64), url: 'http://127.0.0.1:5000/example/' }), /selected story revision/);
});

test('does not promise live following when an older MCP returns a fixed snapshot', async () => {
  await assert.rejects(openStory(async (name) => name === 'life_saved_work_list'
    ? { heads: [head], window: { nextOffset: null } }
    : { graphHash, url: 'http://127.0.0.1:5000/example/', mode: 'snapshot' }), /did not open a live view/);
});
