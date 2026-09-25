#!/usr/bin/env node
// Typeset a story as a book PDF. The text is the Meaning Model's own render of the story graph (life_narrative_render),
// as the extractor saved it in the page's data file; nothing is written outside the graph.
//   node book.mjs [name] [--out pdf/<name>.pdf]
// It needs Chrome or Chromium for the typesetting: set CHROME to its executable if it is not in the usual place.
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const argv = process.argv.slice(2);
const flag = (name) => { const index = argv.indexOf(name); return index >= 0 ? argv[index + 1] : null; };
const name = argv.find((value, index) => !value.startsWith('--') && argv[index - 1] !== '--out') ?? 'rabbit-hole';
const out = resolve(flag('--out') ?? `pdf/${name}.pdf`);
const data = JSON.parse(readFileSync(`public/data/${name}.json`, 'utf8'));
if (!data.story?.units?.length) throw new Error(`public/data/${name}.json holds no rendered story; run extract.mjs first.`);

const escape = (text) => String(text).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const inline = (text) => escape(text).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\*(.+?)\*/g, '<em>$1</em>').replace(/\n/g, ' ');
let title = null; const body = [];
for (const unit of data.story.units) for (const block of unit.text.split(/\n{2,}/).map((part) => part.trim()).filter(Boolean)) {
  const heading = block.match(/^(#{1,4})\s+([\s\S]*)$/);
  if (heading && heading[1].length === 1 && !title) { title = heading[2].trim(); continue; }
  if (heading) body.push(`<h${heading[1].length}>${inline(heading[2])}</h${heading[1].length}>`);
  else if (/^(\*\s*){3}$|^-{3,}$/.test(block)) body.push('<p class="break">*</p>');
  else body.push(`<p>${inline(block)}</p>`);
}
title ??= data.title ?? name;
const words = data.story.units.reduce((sum, unit) => sum + unit.text.split('\n').filter((line) => !/^\s*#/.test(line)).join(' ').split(/\s+/).filter(Boolean).length, 0);
const date = new Date().toISOString().slice(0, 10);
const short = (hash) => (hash ? `${hash.slice(0, 12)}…` : 'unknown');

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${escape(title)}</title><style>
  @page { size: 5.5in 8.5in; margin: 0.85in 0.72in 0.95in; @bottom-center { content: counter(page); font: 9.5pt "Iowan Old Style", Palatino, Georgia, serif; color: #555; } }
  @page front { @bottom-center { content: none; } }
  html { font-family: "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif; font-size: 10.8pt; line-height: 1.47; color: #111; }
  body { margin: 0; }
  .front { page: front; break-after: page; height: 6.6in; display: flex; flex-direction: column; }
  .title { justify-content: center; text-align: center; }
  .title h1 { font-size: 27pt; line-height: 1.12; font-weight: 600; margin: 0 0 18pt; }
  .title .by { font-size: 11pt; font-style: italic; color: #333; }
  .colophon { justify-content: flex-end; font-size: 8.6pt; line-height: 1.5; color: #333; }
  .colophon p { margin: 0 0 7pt; text-indent: 0; text-align: left; hyphens: none; }
  h2 { break-before: page; font-size: 15pt; font-weight: 600; text-align: center; margin: 0.9in 0 26pt; }
  h3, h4 { font-size: 11.5pt; font-weight: 600; margin: 18pt 0 8pt; break-after: avoid; }
  p { margin: 0; text-indent: 1.3em; text-align: justify; hyphens: auto; orphans: 2; widows: 2; }
  h2 + p, h3 + p, h4 + p, .break + p { text-indent: 0; }
  p.break { text-align: center; text-indent: 0; margin: 10pt 0; }
</style></head><body>
<section class="front title"><h1>${escape(title)}</h1><div class="by">A novel written by an AI agent with the Meaning Model,<br>from an idea by Henrik Westerberg</div></section>
<section class="front colophon">
  <p>${escape(title)}. ${words.toLocaleString('en-US')} words.</p>
  <p>The text is the Meaning Model's render of the story graph ${short(data.headGraphHash)} (projection ${short(data.story.projectionHash)}), made with life_narrative_render. The story, its world model and every step of their construction are at github.com/emergent-wisdom/story. The Meaning Model is at github.com/emergent-wisdom/meaning-model.</p>
  <p>Typeset ${date}.</p>
</section>
${body.join('\n')}
</body></html>`;

const chrome = process.env.CHROME ?? ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find(existsSync);
if (!chrome) throw new Error('Set CHROME to a Chrome or Chromium executable.');
const work = mkdtempSync(join(tmpdir(), 'story-book-')); const page = join(work, 'book.html');
try {
  writeFileSync(page, html); mkdirSync(dirname(out), { recursive: true });
  execFileSync(chrome, ['--headless=new', '--no-pdf-header-footer', '--disable-gpu', `--print-to-pdf=${out}`, pathToFileURL(page).href], { stdio: 'ignore' });
} finally { rmSync(work, { recursive: true, force: true }); }
console.log(`${out}: ${title}, ${words} words`);
