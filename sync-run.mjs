#!/usr/bin/env node
// Copy a story run into runs/<name>/ for this repo: the agent's own record, without the operator's machinery.
//   node sync-run.mjs <run folder> <name>
// It copies the brief, the agent's inputs, results, build scripts and notes, the relay call log and an online
// backup of the engine state. It leaves out the relay's queue files, process ids and logs, and the public
// PROTOCOL.md, which is written by hand. The relay names the published package instead of a local checkout.
// It stops if a local path or a configured credential would be copied.
import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, relative, resolve } from 'node:path';

const [source, name] = process.argv.slice(2);
if (!source || !name) throw new Error('usage: node sync-run.mjs <run folder> <name>');
const run = resolve(source); const out = resolve('runs', name);
const SKIP = new Set(['daemon.json', 'relay-serve.log', 'server-stderr.log', 'relay', '__pycache__',
  'engine-state.sqlite', 'engine-state.sqlite-shm', 'engine-state.sqlite-wal', 'PROTOCOL.md']);

function copy(from, to) {
  mkdirSync(to, { recursive: true });
  for (const entry of readdirSync(from)) {
    if (SKIP.has(entry) || entry.startsWith('.')) continue;
    const a = join(from, entry); const b = join(to, entry);
    if (statSync(a).isDirectory()) copy(a, b); else cpSync(a, b);
  }
}
copy(run, out);
execFileSync('sqlite3', [join(run, 'novel', 'engine-state.sqlite'), `.backup '${join(out, 'novel', 'engine-state.sqlite')}'`]);

// The relay starts the published package (npm install; npx meaning-model-mcp --install-engine), or MEANING_MODEL_DIR.
const relay = join(out, 'novel', 'relay.mjs');
if (existsSync(relay)) {
  const text = readFileSync(relay, 'utf8').replace(/^const publish = '[^']*';$/m,
    "const publish = process.env.MEANING_MODEL_DIR ?? fileURLToPath(new URL('../../../node_modules/@emergent-wisdom/meaning-model-mcp/', import.meta.url));");
  writeFileSync(relay, text);
}

// Nothing local or secret leaves this machine.
const secrets = [];
for (const file of [join(homedir(), '.config', 'typesafe', 'env')]) {
  if (!existsSync(file)) continue;
  for (const line of readFileSync(file, 'utf8').split('\n')) {
    const value = line.replace(/^export\s+/, '').split('=').slice(1).join('=').trim().replace(/^["']|["']$/g, '');
    if (value.length >= 12) secrets.push(Buffer.from(value));
  }
}
const home = Buffer.from(homedir()); const problems = [];
(function scan(dir) {
  for (const entry of readdirSync(dir)) {
    const path = join(dir, entry);
    if (statSync(path).isDirectory()) { scan(path); continue; }
    const bytes = readFileSync(path);
    if (bytes.includes(home)) problems.push(`${relative(out, path)}: a local path`);
    if (secrets.some((secret) => bytes.includes(secret))) problems.push(`${relative(out, path)}: a configured credential`);
  }
})(out);
if (problems.length) { console.error(problems.join('\n')); process.exit(1); }
console.log(`runs/${name}: copied and checked`);
