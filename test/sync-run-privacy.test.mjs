import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, realpathSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { DatabaseSync } from 'node:sqlite';

const script = fileURLToPath(new URL('../sync-run.mjs', import.meta.url));

function fixture(t, ignored = true) {
  const directory = mkdtempSync(join(tmpdir(), 'story-private-staging-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const repository = join(directory, 'repository');
  const source = join(directory, 'source');
  mkdirSync(repository);
  mkdirSync(join(source, 'novel', 'inputs'), { recursive: true });
  execFileSync('git', ['init', '--quiet', repository]);
  if (ignored) writeFileSync(join(repository, '.gitignore'), '.local-work/\n');
  const transcript = '{"event":"result","result":{"text":"Private staging fixture"}}\n';
  writeFileSync(join(source, 'novel', 'mcp-transcript.jsonl'), transcript);
  writeFileSync(join(source, 'novel', 'inputs', 'example.json'), '{"text":"Private input fixture"}\n');
  writeFileSync(join(source, 'novel', 'relay.mjs'), "import { fileURLToPath } from 'node:url';\nconst publish = 'source-package';\nconsole.log(publish);\n");
  const database = new DatabaseSync(join(source, 'novel', 'engine-state.sqlite'));
  database.exec("CREATE TABLE fixture (value TEXT); INSERT INTO fixture VALUES ('private state fixture');");
  database.close();
  return { repository, source, transcript };
}

test('saved runs stage privately without publishing raw state, transcript or inputs', (t) => {
  const { repository, source, transcript } = fixture(t);
  execFileSync(process.execPath, [script, source, 'example'], { cwd: repository });
  const destination = join(repository, '.local-work', 'imported-runs', 'example', 'novel');
  assert.equal(readFileSync(join(destination, 'mcp-transcript.jsonl'), 'utf8'), transcript);
  assert.equal(readFileSync(join(destination, 'inputs', 'example.json'), 'utf8'), '{"text":"Private input fixture"}\n');
  const database = new DatabaseSync(join(destination, 'engine-state.sqlite'), { readOnly: true });
  assert.equal(database.prepare('SELECT value FROM fixture').get().value, 'private state fixture');
  database.close();
  assert.equal(existsSync(join(repository, 'runs')), false);
  const relayEnvironment = { ...process.env };
  delete relayEnvironment.MEANING_MODEL_DIR;
  const packagePath = execFileSync(process.execPath, [join(destination, 'relay.mjs')], { env: relayEnvironment, encoding: 'utf8' }).trim();
  assert.equal(resolve(packagePath), join(realpathSync(repository), 'node_modules', '@emergent-wisdom', 'meaning-model-mcp'));
  execFileSync('git', ['check-ignore', '--quiet', '--', destination], { cwd: repository });
  assert.throws(() => execFileSync(process.execPath, [script, source, 'example'], { cwd: repository, stdio: 'pipe' }), /already exists/);
});

test('saved-run staging refuses unignored destinations and names that escape the private directory', (t) => {
  const { repository, source } = fixture(t, false);
  assert.throws(() => execFileSync(process.execPath, [script, source, 'example'], { cwd: repository, stdio: 'pipe' }), /must be ignored by Git/);
  assert.equal(existsSync(join(repository, '.local-work')), false);
  assert.throws(() => execFileSync(process.execPath, [script, source, '../public'], { cwd: repository, stdio: 'pipe' }), /simple directory name/);
  assert.equal(existsSync(join(repository, 'public')), false);
});

test('saved-run staging rejects source symlinks without rewriting their external targets', (t) => {
  const { repository, source } = fixture(t);
  const outside = join(repository, 'outside.txt');
  const original = `Original source location: ${source}/untouched\n`;
  writeFileSync(outside, original);
  symlinkSync(outside, join(source, 'novel', 'linked.txt'));
  assert.throws(() => execFileSync(process.execPath, [script, source, 'example'], { cwd: repository, stdio: 'pipe' }), /Refusing symbolic link/);
  assert.equal(readFileSync(outside, 'utf8'), original);
  assert.equal(existsSync(join(repository, 'runs')), false);
});
