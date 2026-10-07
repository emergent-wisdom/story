import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { gunzipSync } from 'node:zlib';
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

test('downloaded MCP bundles hold each complete history from its first revision and match the current viewer',async()=>{
  const manifest=await json('../public/PUBLICATION-MANIFEST.json');
  assert.deepEqual((await readdir(new URL('../models/',import.meta.url))).sort(),Object.values(manifest.importableBundles).map(entry=>entry.file).sort());
  for(const [key,entry]of Object.entries(manifest.importableBundles)) {
    const download=await readFile(new URL(`../models/${entry.file}`,import.meta.url));
    assert.equal(entry.compression,'gzip');assert.equal(download.length,entry.bytes);assert.equal(sha(download),entry.fileSha256);
    const bytes=gunzipSync(download);
    assert.equal(bytes.length,entry.unpackedBytes);assert.equal(sha(bytes),entry.unpackedSha256);
    assert(bytes.length<=256*1024*1024,'life_construction_import reads files of at most 256 MiB');
    const bundle=JSON.parse(bytes), story=manifest.stories[key];
    const snapshot=await json(`../public/models/${story.snapshot}`);
    assert.equal(bundle.bundleSha256,entry.constructionContentSha256);
    assert.equal(bundle.headGraphHash,story.graphHash);
    assert.equal(bundle.models.length,entry.modelCount);
    assert.equal(bundle.revisionCount,entry.graphRevisionCount);
    assert.equal(bundle.revisions.length,entry.graphRevisionCount);
    assert.equal(bundle.revisions[0].graphHash,entry.firstGraphHash,'The history must begin at its first graph revision');
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
    const record=await json(`../public/${manifest.publicationRepairs[key]}`);
    for(const {current,graphRevision} of record.hashMapping.graphs) assert.equal(bundle.revisions[graphRevision].graphHash,current,'Every former public revision must be found in the history');
    assert.equal(record.hashMapping.graphs.at(-1).current,story.graphHash);
    for(const {current} of record.hashMapping.models) assert(models.has(current),'Every former public model must be found in the history');
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

test('October 7 complete histories keep the current editions and omit private material',async()=>{
  const manifest=await json('../public/PUBLICATION-MANIFEST.json');
  assert.equal(manifest.date,'2026-10-07');
  const expectedProse={book:'4dbe1f5caa94aba8ef9d8d2a77a75e2faf56f3fff79e617d877672748fd97bb3',
    twelve:'e8f7ec3088978135b9143be4ad14c0012c1f6c97fc57398666ea20d59e0dd53a'};
  const privateCoordination=/Authorized\s*next-round\s*delegation\s*from\s*the\s*source\s*chat|Book\s*pass\s*completed\s*first|one\s*book\s*at\s*a\s*time|root\s*follow[\s-]*up|no\s*(?:publish\/commit|commit\/publish)/i;
  const personalOrLocal=/\bHenrik\b|Westerberg|\/Users\/|\/home\/[a-z]|[A-Z]:\\Users\\|\.local-work\//;
  for(const [key,entry]of Object.entries(manifest.stories)) {
    assert.equal(sha(await readFile(new URL(`../${entry.manuscript}`,import.meta.url))),expectedProse[key]);
    assert.equal(entry.proseEditionDate,manifest.proseEditionDates[key]);
    const record=await json(`../public/${manifest.publicationRepairs[key]}`);
    assert.equal(record.publicationDate,'2026-10-07');
    assert.equal(record.proseEditionDate,entry.proseEditionDate);
    assert.equal(record.redactions.fields.length,record.redactions.count);
    assert(record.redactions.fields.every(field=>Object.keys(field).every(name=>['where','path','rule','reason'].includes(name))),'Original values and their hashes stay private');
    const snapshot=await json(`../public/models/${entry.snapshot}`);
    assert(snapshot.inspection.graph.nodes.some(node=>node.id===entry.priorPublication.privacyProjection.disclosureNodeId),'The October 3 disclosure stays in the history');
    const bundle=gunzipSync(await readFile(new URL(`../models/${entry.bundle}`,import.meta.url))).toString('utf8');
    const author=manifest.authorLives[key==='book'?'nora':'faye'];
    for(const [path,text] of [[`../models/${entry.bundle}`,bundle],[`../public/models/${entry.snapshot}`,await readFile(new URL(`../public/models/${entry.snapshot}`,import.meta.url),'utf8')],
      [`../public/models/${author.snapshot}`,await readFile(new URL(`../public/models/${author.snapshot}`,import.meta.url),'utf8')]]) {
      assert.doesNotMatch(text,privateCoordination,path);
      assert.doesNotMatch(text,personalOrLocal,path);
    }
  }
});
