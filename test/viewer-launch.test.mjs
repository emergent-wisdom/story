import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { viewerArguments, openViewer } from '../serve.mjs';
import { meaningModelRoot } from 'meaning-model-viewer/meaning-model.mjs';

test('explicit run and snapshot requests pass unchanged to the shared viewer', () => {
  for (const args of [['--run','runs/rabbit-hole'],['--data','reviewed','--port','9000'],['--help']]) assert.deepEqual(viewerArguments(args),args);
});

test('the story depends on the shared viewer and MCP release rather than a copied interface', async () => {
  const pkg=JSON.parse(await readFile(new URL('../package.json',import.meta.url),'utf8'));
  assert.equal(pkg.dependencies['@emergent-wisdom/meaning-model-mcp'],'https://github.com/emergent-wisdom/meaning-model/releases/download/v0.6.8/emergent-wisdom-meaning-model-mcp-0.6.8.tgz');
  assert.equal(pkg.overrides['@emergent-wisdom/meaning-model-mcp'],'$@emergent-wisdom/meaning-model-mcp');
  assert.equal(pkg.dependencies['meaning-model-viewer'],'github:emergent-wisdom/meaning-model-viewer#v0.6.1');
  assert.equal(pkg.scripts.serve,'node serve.mjs');
  assert.equal(pkg.version,'0.6.8');
  assert.equal(pkg.private,true);
  const suppliedRoot=process.env.MEANING_MODEL_DIR;
  delete process.env.MEANING_MODEL_DIR;
  try {
    const resolved=JSON.parse(await readFile(`${meaningModelRoot()}/package.json`,'utf8'));
    assert.equal(resolved.version,pkg.version,
      'The shared launcher must serve the selected MCP version, not an older nested dependency');
  } finally {
    if(suppliedRoot!==undefined) process.env.MEANING_MODEL_DIR=suppliedRoot;
  }
});

test('original event URLs open Twelve Words while explicit current choices remain intact',async()=>{
  const server=await openViewer(['--port','0']);
  try {
    const base=`http://127.0.0.1:${server.address().port}`;
    const manifest=JSON.parse(await readFile(new URL('../public/PUBLICATION-MANIFEST.json',import.meta.url),'utf8'));
    for(const [path,key,view]of[
      ['/processes.html?title=The%20Rabbit%20Hole','twelve','together'],
      ['/landscape.html?data=rabbit-hole&at=2020','twelve','terrain'],
      ['/processes.html?data=book&view=layers','book','layers'],
    ]) {
      const response=await fetch(`${base}${path}`,{redirect:'manual'});
      assert.equal(response.status,302);
      const destination=new URL(response.headers.get('location'),base);
      assert.equal(destination.searchParams.get('view'),view);
      if(path.includes('at=2020')) assert.equal(destination.searchParams.get('at'),'2020');
      const snapshot=await (await fetch(new URL('data/model.json',destination))).json();
      assert.equal(snapshot.headGraphHash,manifest.stories[key].graphHash);
    }
  } finally {await new Promise(resolve=>server.close(resolve));}
});
