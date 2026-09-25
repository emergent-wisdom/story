// Export a run's whole construction (life_construction_export) from its saved engine state, with the published package.
//   node export-run.mjs <run folder> <graph hash> <scope,...>
import { copyFileSync, rmSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
const [run, graphHash, scopes = ''] = process.argv.slice(2);
const PUBLISH = resolve(process.env.MEANING_MODEL_DIR ?? 'node_modules/@emergent-wisdom/meaning-model-mcp');
const snapshot = join(tmpdir(), `export-run-${process.pid}.sqlite`); copyFileSync(join(run, 'novel', 'engine-state.sqlite'), snapshot);
process.env.LIFE_SIM_STATE_FILE = snapshot;
const { LifeSimulationService } = await import(`${PUBLISH}/mcp-server/src/service.mjs`);
const { exportConstructionHistory } = await import(`${PUBLISH}/mcp-server/src/construction-record.mjs`);
const service = new LifeSimulationService();
try { await service.initialize(); const history = await exportConstructionHistory(service, { graphHash, accessScopes: scopes.split(',').filter(Boolean) });
  writeFileSync(join(run, 'novel', 'construction-export.json'), JSON.stringify(history)); console.log(`construction-export.json: ${history.models?.length} model revisions, ${history.revisions?.length} graph revisions`);
} finally { await service.close?.(); for (const s of ['', '-wal', '-shm']) rmSync(snapshot + s, { force: true }); }
