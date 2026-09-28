import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { viewerArguments, openViewer } from '../serve.mjs';

test('explicit run and snapshot requests pass unchanged to the shared viewer', () => {
  for (const args of [['--run','runs/rabbit-hole'],['--data','reviewed','--port','9000'],['--help']]) assert.deepEqual(viewerArguments(args),args);
});

test('the story depends on the shared viewer and MCP release rather than a copied interface', async () => {
  const pkg=JSON.parse(await readFile(new URL('../package.json',import.meta.url),'utf8'));
  assert.equal(pkg.dependencies['@emergent-wisdom/meaning-model-mcp'],'0.5.2');
  assert.equal(pkg.dependencies['meaning-model-viewer'],'github:emergent-wisdom/meaning-model-viewer#v0.5.2');
  assert.equal(pkg.scripts.serve,'node serve.mjs');
  assert.equal(pkg.version,'0.5.2');
  assert.equal(pkg.private,true);
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
