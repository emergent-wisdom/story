import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { viewerArguments } from '../serve.mjs';
const json=async(relative)=>JSON.parse(await readFile(new URL(relative,import.meta.url),'utf8'));
const sha=(text)=>createHash('sha256').update(text).digest('hex');

test('published story text matches the current viewer renders and recorded publication identities',async()=>{
  const manifest=await json('../public/PUBLICATION-MANIFEST.json');
  for(const [key,filename]of[['book','the-book-of-conditions.md'],['twelve','twelve-words.md']]) {
    const entry=manifest.stories[key], snapshot=await json(`../public/models/${entry.snapshot}`);
    const text=await readFile(new URL(`../stories/${filename}`,import.meta.url),'utf8');
    assert.equal(snapshot.headGraphHash,entry.graphHash);assert.equal(snapshot.modelHash,entry.modelHash);
    assert.equal(text,snapshot.story.units.map(unit=>unit.text).join('\n\n'));
    assert.equal(sha(text),entry.proseSha256);
  }
});

test('default public viewer contains exactly the selected stories and author lives',async()=>{
  const manifest=await json('../public/PUBLICATION-MANIFEST.json');
  const expected=[...Object.values(manifest.stories),...Object.values(manifest.authorLives)].map(entry=>entry.snapshot).sort();
  assert.deepEqual((await readdir(new URL('../public/models/',import.meta.url))).sort(),expected);
  const args=viewerArguments([]);assert.equal(args[0],'--data');assert.ok(args[1].endsWith('/public/models/'));
});

test('downloaded MCP bundles contain the same current models and graph without private predecessors',async()=>{
  const manifest=await json('../public/PUBLICATION-MANIFEST.json');
  assert.deepEqual((await readdir(new URL('../models/',import.meta.url))).sort(),Object.values(manifest.importableBundles).map(entry=>entry.file).sort());
  for(const [key,entry]of Object.entries(manifest.importableBundles)) {
    const bytes=await readFile(new URL(`../models/${entry.file}`,import.meta.url));
    const bundle=JSON.parse(bytes), story=manifest.stories[key];
    const snapshot=await json(`../public/models/${story.snapshot}`);
    assert.equal(bytes.length,entry.bytes);assert.equal(sha(bytes),entry.fileSha256);
    assert.equal(bundle.bundleSha256,entry.constructionContentSha256);
    assert.equal(bundle.headGraphHash,story.graphHash);
    assert.equal(bundle.models.length,entry.modelCount);
    assert.equal(bundle.revisionCount,1);assert.equal(bundle.revisions.length,1);
    const graph=bundle.revisions[0];
    assert.equal(graph.graphHash,story.graphHash);assert.equal(graph.definition.revision.number,0);
    assert.equal(graph.definition.revision.previous_graph_hash??null,null);
    assert.equal(graph.definition.source.model_hash,story.modelHash);
    assert.deepEqual(graph.definition.nodes,snapshot.inspection.graph.nodes);
    assert.deepEqual(graph.definition.edges,snapshot.inspection.graph.edges);
    assert.deepEqual(bundle.models.find(model=>model.modelHash===story.modelHash).definition,snapshot.inspection.model);
    for(const model of bundle.models) {
      assert.equal(model.definition.revision.number,0);
      assert.equal(model.definition.revision.previous_model_hash??null,null);
    }
    const author=manifest.authorLives[key==='book'?'nora':'faye'];
    const authorSnapshot=await json(`../public/models/${author.snapshot}`);
    assert.deepEqual(bundle.models.find(model=>model.modelHash===author.modelHash).definition,authorSnapshot.inspection.model);
  }
});
