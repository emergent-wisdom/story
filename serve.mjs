// Open the reviewed story snapshots through the same viewer shipped in the MCP.
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { existsSync } from 'node:fs';
import { main } from 'meaning-model-viewer/serve.mjs';

export function viewerArguments(argv = process.argv.slice(2)) {
  if (argv.includes('--run') || argv.includes('--data') || argv.includes('--help')) return argv;
  const snapshots = fileURLToPath(new URL('./public/models/', import.meta.url));
  if (!existsSync(snapshots)) throw new Error('Reviewed story snapshots are missing. Use a complete story release, or pass --run runs/rabbit-hole to view the original event run.');
  return ['--data', snapshots, ...argv];
}

export async function openViewer(argv = process.argv.slice(2)) {
  const currentEditions = !argv.includes('--run') && !argv.includes('--data');
  const server = await main(viewerArguments(argv));
  if (server && currentEditions) server.prependListener('request', (request) => {
    // Event links referred to The Rabbit Hole before this collection included both books.
    // Preserve that identity while the shared server redirects to the current interface.
    try {
      const url = new URL(request.url, 'http://localhost');
      if (!['/processes.html', '/landscape.html'].includes(url.pathname)) return;
      const name = url.searchParams.get('data');
      if (!name || name === 'rabbit-hole') {
        url.searchParams.set('data', 'twelve');
        request.url = `${url.pathname}${url.search}`;
      }
    } catch { /* The shared server handles malformed requests. */ }
  });
  return server;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { await openViewer(); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
