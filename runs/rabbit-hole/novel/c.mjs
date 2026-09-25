// Usage: node c.mjs <tool> <inputs/args.json> <saveName> [maxChars]
// Sends one tools/call through the relay, saves the full result under results/, prints a compact view.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
const [tool, argsFile, save, max = '2500'] = process.argv.slice(2);
const cmd = JSON.stringify({ op: 'call', name: tool, argsFile, save, quiet: true });
const reply = JSON.parse(execFileSync(process.execPath, ['relay.mjs', cmd], { encoding: 'utf8', maxBuffer: 1 << 28 }));
let body = null;
try { body = JSON.parse(readFileSync(`results/${save}`, 'utf8')); } catch { body = reply.result ?? reply; }
const text = body?.content?.[0]?.text ?? JSON.stringify(body, null, 1);
console.log(`seq=${reply.seq} isError=${reply.isError ?? false}${reply.error ? ' relayError=' + reply.error : ''}`);
console.log(text.length > Number(max) ? text.slice(0, Number(max)) + `\n... [${text.length} chars; full in results/${save}]` : text);
