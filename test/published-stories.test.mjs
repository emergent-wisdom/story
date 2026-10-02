import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { viewerArguments } from '../serve.mjs';
import { applyNarrativeDefinitionDelta } from '@emergent-wisdom/meaning-model-mcp/mcp-server/src/narrative-delta.mjs';
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
    assert.equal(sha(await readFile(new URL(`../public/models/${entry.snapshot}`,import.meta.url))),entry.snapshotFileSha256);
    assert.equal(snapshot.capabilities.construction,true,'Retained multi-revision history must be playable');
    assert.equal(snapshot.constructionTiming,'order');
    assert.equal(snapshot.steps.length,entry.viewerConstruction.steps);
    assert.equal(snapshot.steps.length,entry.constructionHistory.graphRevisions+entry.constructionHistory.storyModelRevisions);
    assert(snapshot.steps.every(step=>step.at===null),'Ordinal replay must not invent clock times');
  }
});

test('default public viewer contains exactly the selected stories and author lives',async()=>{
  const manifest=await json('../public/PUBLICATION-MANIFEST.json');
  const expected=[...Object.values(manifest.stories),...Object.values(manifest.authorLives)].map(entry=>entry.snapshot).sort();
  assert.deepEqual((await readdir(new URL('../public/models/',import.meta.url))).sort(),expected);
  const args=viewerArguments([]);assert.equal(args[0],'--data');assert.ok(args[1].endsWith('/public/models/'));
});

test('downloaded MCP bundles retain complete public revision chains and match the current viewer',async()=>{
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
    assert.equal(bundle.revisionCount,entry.graphRevisionCount);
    assert.equal(bundle.revisions.length,entry.graphRevisionCount);
    assert.equal(bundle.revisions[0].graphHash,manifest.initialPublicationCleanup.stories[key].graphHash,
      'The existing publication root must not be replaced');
    const models=new Map(bundle.models.map(model=>[model.modelHash,model.definition]));
    assert.equal(models.size,bundle.models.length,'Model definitions must be unique');
    let definition=null, previousHash=null;
    const graphHashes=new Set();
    for(const [index,revision] of bundle.revisions.entries()) {
      assert(!graphHashes.has(revision.graphHash),'Each revision must occur once');
      graphHashes.add(revision.graphHash);
      if(revision.definition) definition=revision.definition;
      else {
        assert(definition,'A delta must have its complete predecessor');
        definition=applyNarrativeDefinitionDelta(definition,revision.delta);
      }
      assert.equal(definition.revision.number,index);
      assert.equal(definition.revision.previous_graph_hash??null,previousHash,'No predecessor may be dropped');
      assert(models.has(definition.source.model_hash),'Every bound native model must be included');
      previousHash=revision.graphHash;
    }
    assert.equal(previousHash,story.graphHash);
    assert.equal(definition.source.model_hash,story.modelHash);
    assert.deepEqual(definition.nodes,snapshot.inspection.graph.nodes);
    assert.deepEqual(definition.edges,snapshot.inspection.graph.edges);
    assert.deepEqual(bundle.models.find(model=>model.modelHash===story.modelHash).definition,snapshot.inspection.model);
    for(const model of bundle.models) {
      const revision=model.definition.revision, parent=revision.previous_model_hash;
      if(parent) {
        assert(models.has(parent),'Native model ancestry must be included');
        assert.equal(models.get(parent).id,model.definition.id);
        assert.equal(models.get(parent).revision.number+1,revision.number);
      } else assert.equal(revision.number,0);
    }
    const author=manifest.authorLives[key==='book'?'nora':'faye'];
    const authorSnapshot=await json(`../public/models/${author.snapshot}`);
    assert.deepEqual(bundle.models.find(model=>model.modelHash===author.modelHash).definition,authorSnapshot.inspection.model);
  }
});

test('publication repair records name the delivered bundles without private working paths',async()=>{
  const manifest=await json('../public/PUBLICATION-MANIFEST.json');
  for(const [key,path] of Object.entries(manifest.publicationRepairs)) {
    const repair=await json(`../public/${path}`), story=manifest.stories[key];
    const publication=repair.publication??repair;
    assert.equal(publication.headGraphHash,story.graphHash);
    const bundleEntry=manifest.importableBundles[key];
    assert.equal(publication.fileSha256,bundleEntry.fileSha256);
    assert.equal(repair.manuscript?.sha256??repair.manuscriptSha256,story.proseSha256);
    assert.doesNotMatch(JSON.stringify(repair),/\/Users\/|\/home\/|[A-Z]:\\Users\\/i);
  }
});
