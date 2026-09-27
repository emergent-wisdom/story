// Open this story through the same running MCP that the writer uses.
// No second engine, database copy, extraction step, or separate viewer server.
import { execFile } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const run = promisify(execFile);
const root = dirname(fileURLToPath(import.meta.url));

export async function openStory(call, { graphId = 'rabbit-hole-novel', accessScopes = ['story-author'] } = {}) {
  const heads = [];
  const seenOffsets = new Set();
  let offset = 0;
  do {
    if (seenOffsets.has(offset)) throw new Error('The saved-work catalog repeated a page; no model was opened.');
    seenOffsets.add(offset);
    const page = await call('life_saved_work_list', { graphId, accessScopes, offset, limit: 25 });
    if (!Array.isArray(page.heads)) throw new Error('The MCP did not return a saved-work catalog. Use a current Meaning Model build with the bundled viewer.');
    heads.push(...page.heads.filter((head) => head.graphId === graphId));
    offset = page.window?.nextOffset ?? null;
  } while (offset !== null);
  const unique = [...new Map(heads.map((head) => [head.graphHash, head])).values()];
  if (unique.length === 0) throw new Error(`No visible saved story '${graphId}' was found. Ask the connected assistant to import or select the intended story with its access scopes.`);
  if (unique.length !== 1) throw new Error(`The story has ${unique.length} branch heads. Ask the connected assistant to select the intended branch before opening it.`);
  const selected = unique[0];
  const viewer = await call('life_model_viewer_open', { graphHash: selected.graphHash, accessScopes });
  if (!viewer.url || viewer.graphHash !== selected.graphHash) throw new Error('The MCP did not return a viewer for the selected story revision.');
  return { ...viewer, graphId, revision: selected.revision };
}

async function runningRelay(path) {
  let daemon;
  try { daemon = JSON.parse(await readFile(join(dirname(path), 'daemon.json'), 'utf8')); }
  catch { throw new Error('No running Writer relay was found. Connect the current Meaning Model MCP in your AI app and ask "Open this model". Existing Writer contributors can set MEANING_MODEL_RELAY to their running relay.mjs; see README.md.'); }
  if (!Number.isSafeInteger(daemon.pid) || daemon.pid < 1) throw new Error('The Writer relay has no valid running-process record. Restart your existing Writer workflow before opening its model.');
  try { process.kill(daemon.pid, 0); }
  catch (error) { if (error.code !== 'EPERM') throw new Error('The recorded Writer relay is no longer running. Restart that existing Writer workflow; do not start a second MCP against its database.'); }
  return async (name, args) => {
    const { stdout } = await run(process.execPath, [path, JSON.stringify({ op: 'call', name, args })], { maxBuffer: 4 * 1024 * 1024, timeout: 330_000 });
    const reply = JSON.parse(stdout);
    if (reply.error || reply.isError) throw new Error(`Writer MCP call ${name} failed: ${reply.error ?? JSON.stringify(reply.result)}. Use the current MCP with life_saved_work_list and life_model_viewer_open.`);
    const result = reply.result;
    return result?.structuredContent ?? (result?.content?.[0]?.text ? JSON.parse(result.content[0].text) : result);
  };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const relay = resolve(process.env.MEANING_MODEL_RELAY || join(root, 'work', 'relay.mjs'));
    const viewer = await openStory(await runningRelay(relay));
    console.log(viewer.url);
    console.log(`Opened ${viewer.graphId}, revision ${viewer.revision}, in the bundled Meaning Model viewer.`);
    console.log('This link shows a saved revision. Run this command again after writing changes. Keep the Writer MCP running while viewing.');
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
