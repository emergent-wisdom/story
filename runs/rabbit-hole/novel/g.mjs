// Usage: node g.mjs <results/file.json> <dot.path>   prints one value from a saved result
import { readFileSync } from 'node:fs';
const [file, path] = process.argv.slice(2);
let v = JSON.parse(readFileSync(file, 'utf8'));
if (v?.content?.[0]?.text && !v.structuredContent) { try { v = JSON.parse(v.content[0].text); } catch {} }
for (const k of path.split('.')) v = v?.[k];
console.log(typeof v === 'string' ? v : JSON.stringify(v));
