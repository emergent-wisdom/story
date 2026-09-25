// Minimal persistent MCP relay for the 2026-09-25 rabbit-hole story run. --serve keeps one server alive;
// any other invocation sends one command and prints the reply.
import { createRequire } from 'node:module';
import { randomUUID } from 'node:crypto';
import { readFile, writeFile, appendFile, mkdir, rename, readdir, stat } from 'node:fs/promises';
import { createWriteStream, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('./', import.meta.url));
const publish = process.env.MEANING_MODEL_DIR ?? fileURLToPath(new URL('../../../node_modules/@emergent-wisdom/meaning-model-mcp/', import.meta.url));
const relayDir = join(here, 'relay');
const transcript = join(here, 'mcp-transcript.jsonl');
const now = () => new Date().toISOString();
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const log = (value) => appendFile(transcript, JSON.stringify(value) + '\n');
const args = process.argv.slice(2);

if (args[0] === '--serve') {
  const require = createRequire(join(publish, 'mcp-server', 'package.json'));
  const { Client } = require('@modelcontextprotocol/client');
  const { StdioClientTransport } = require('@modelcontextprotocol/client/stdio');
  const client = new Client({ name: 'novel-relay', version: '0.1.0' });
  const transport = new StdioClientTransport({
    command: process.execPath, args: [join(publish, 'mcp-server', 'bin', 'meaning-model-mcp.mjs')],
    cwd: join(publish, 'mcp-server'), stderr: 'pipe',
    env: { ...process.env, 
      LIFE_SIM_STATE_FILE: join(here, 'engine-state.sqlite'),
      LIFE_SIM_ENGINE_BIN: join(publish, 'rust-engine', 'target', 'release', 'life-sim-engine') } });
  const stderr = createWriteStream(join(here, 'server-stderr.log'), { flags: 'a' });
  transport.stderr?.pipe(stderr);
  await client.connect(transport);
  for (const d of ['requests', 'replies', 'done']) await mkdir(join(relayDir, d), { recursive: true });
  let seq = 0;
  async function execute(c) {
    const a = c.argsFile ? JSON.parse(await readFile(resolve(here, c.argsFile), 'utf8')) : (c.args ?? {});
    switch (c.op) {
      case 'list_tools': { const r = await client.listTools(); return { tools: r.tools.map(({ name, description, annotations }) => ({ name, description, annotations })) }; }
      case 'tool_schema': { const r = await client.listTools(); const t = r.tools.find((x) => x.name === c.name); if (!t) throw new Error(`Unknown tool ${c.name}`); return t; }
      case 'list_resources': return client.listResources();
      case 'list_resource_templates': return client.listResourceTemplates();
      case 'list_prompts': return client.listPrompts();
      case 'read_resource': return client.readResource({ uri: c.uri });
      case 'get_prompt': return client.getPrompt({ name: c.name, arguments: a });
      case 'call': return client.callTool({ name: c.name, arguments: a });
      default: throw new Error(`Unknown op ${c.op}`);
    }
  }
  let busy = false;
  setInterval(async () => {
    if (busy) return; busy = true;
    try {
      for (const name of (await readdir(join(relayDir, 'requests'))).filter((n) => n.endsWith('.json')).sort()) {
        const path = join(relayDir, 'requests', name);
        const command = JSON.parse(await readFile(path, 'utf8'));
        const entry = { seq: ++seq, at: now(), command };
        let reply;
        try {
          const result = await execute(command);
          await log({ ...entry, event: 'result', result });
          if (command.save) { await mkdir(resolve(here, 'results'), { recursive: true }); await writeFile(resolve(here, 'results', command.save), JSON.stringify(result.structuredContent ?? result, null, 2) + '\n'); }
          reply = { seq: entry.seq, isError: result.isError ?? false, saved: command.save ?? null, result: command.quiet && command.save && !result.isError ? '(saved)' : (result.structuredContent ?? result) };
        } catch (error) {
          await log({ ...entry, event: 'failure', error: error.message });
          reply = { seq: entry.seq, error: error.message };
        }
        await writeFile(join(relayDir, 'replies', name + '.tmp'), JSON.stringify(reply));
        await rename(join(relayDir, 'replies', name + '.tmp'), join(relayDir, 'replies', name));
        await rename(path, join(relayDir, 'done', name));
      }
    } catch (error) { await log({ event: 'relay_error', at: now(), error: error.message }); }
    finally { busy = false; }
  }, 100);
  await writeFile(join(here, 'daemon.json'), JSON.stringify({ readyAt: now(), pid: process.pid, serverPid: transport.pid }, null, 2));
  console.log(JSON.stringify({ ready: true, pid: process.pid, serverPid: transport.pid }));
  for (const s of ['SIGINT', 'SIGTERM']) process.once(s, async () => { await client.close(); process.exit(0); });
} else {
  // client: node relay.mjs '<json command>'   or   node relay.mjs --file cmd.json
  const command = args[0] === '--file' ? JSON.parse(await readFile(args[1], 'utf8')) : JSON.parse(args[0]);
  while (!existsSync(join(here, 'daemon.json'))) await sleep(200);
  const name = `${Date.now()}-${randomUUID()}.json`;
  await mkdir(join(relayDir, 'requests'), { recursive: true });
  await writeFile(join(relayDir, 'requests', name + '.tmp'), JSON.stringify(command));
  await rename(join(relayDir, 'requests', name + '.tmp'), join(relayDir, 'requests', name));
  const replyPath = join(relayDir, 'replies', name);
  const deadline = Date.now() + 300_000;
  while (true) {
    try { const text = await readFile(replyPath, 'utf8'); console.log(text); break; }
    catch (e) { if (e.code !== 'ENOENT') throw e; }
    if (Date.now() > deadline) { console.log(JSON.stringify({ error: 'relay timeout' })); break; }
    await sleep(100);
  }
}
