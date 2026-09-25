# Story Landscape

A live view of a story as an agent builds it with the [Meaning Model](https://github.com/emergent-wisdom/meaning-model).

**The story.** *Twelve Words*, a novel in twelve parts (about 8,400 words), written by an AI agent with the Meaning
Model from an idea by Henrik Westerberg. Read it as [text](runs/rabbit-hole/novel/novel.md) or as a
[book PDF](pdf/rabbit-hole.pdf); both are renders of the story graph, and everything that built it is in
[`runs/rabbit-hole/`](runs/rabbit-hole/).

**The Meaning Model.**
- Source, releases and documentation: [github.com/emergent-wisdom/meaning-model](https://github.com/emergent-wisdom/meaning-model).
  This story was made with [release v0.3.0](https://github.com/emergent-wisdom/meaning-model/releases/tag/v0.3.0).
- The MCP server on npm: [@emergent-wisdom/meaning-model-mcp](https://www.npmjs.com/package/@emergent-wisdom/meaning-model-mcp).
- The paper: *The Meaning Model: Constructing Worlds and Stories at Progressive Resolution*,
  [doi:10.5281/zenodo.22313515](https://doi.org/10.5281/zenodo.22313515).
- [Emergent Wisdom](https://emergentwisdom.org).

The agent does not just write the story: it models the world first, as processes over time. This page shows that
model as a landscape.

- **Every function over time is a ridge.** That covers each person's life, periods and shocks. It covers the
  processes their life runs through (body, kin, work, meaning and the rest), what they want, feel and expect as Cut
  series, and the world's long developments behind them.
- **Events stand as beams of light, decisions as diamonds.** A diamond glows when the model has drawn the decision.
- **The mind floats above.** Understanding Nodes, world stages, the director's findings, drawn decisions and prose
  hang over the terrain, threaded to the moments they are about.
- **Press play to watch it emerge.** The construction replays in the order the agent built it, with the agent's own
  reasons as captions.

When a story reaches into deep time, the axis becomes years before the present on a log scale. The story in this repo
reaches back to hunter-gatherers.

## Run it

```sh
git clone https://github.com/emergent-wisdom/story && cd story
npm install
npm run serve
```

It needs Node.js 22.18 or later. Open http://localhost:8765, which is `landscape.html?data=rabbit-hole`. Add `&play`
to start the replay, `&live` to follow a
running story, `&still` to stop the slow orbit, and `&read` to open the story. **Read the story** shows the text as
the Meaning Model renders it from the story graph (`life_narrative_render`), up to the replay's moment.

**The processes view** is http://localhost:8765/processes.html. It shows every named process the agent modeled
(Kieran's belonging to the Sharehouse, Laura's exhaustion, Barbara's guilt, the bitcoin price, intensive-care
occupancy and the rest) as a curtain of light on its own scale over the story's years. The events that move them run
as threads through every process they touch, with the decisions the model drew, the love-or-fear split behind the
acts, and the causal links between events. The heights follow each process's authored path in the model, read by
`measures.mjs`. Press play to sweep through the years. Both views take `&title=` to show another title.

## Make data from a story run

The extractor reads a run's relay call log and an online SQLite backup of its engine database. It never calls the
run's own server, so it is safe while the agent works. It needs the Meaning Model with its engine: `npm install` brings
the published package, then `npx meaning-model-mcp --install-engine` fetches the engine for your platform. A checkout
named by `MEANING_MODEL_DIR` works too.

```sh
node extract.mjs --run <run folder> --out public/data/<name>.json
./live.sh <run folder> <name>   # refresh every minute while the agent works
node sync-run.mjs <run folder> <name>   # copy the run into runs/<name>/ for this repo
node export-run.mjs <run folder> <graph hash> <access scope>   # the construction export, made in process
```

## The story in this repo

`runs/rabbit-hole/` is the story's whole run, from 25 September 2026. Henrik Westerberg's brief (`PROMPT.md`), about a
comfortable "blue pill" world, the white rabbit, and Paleolithic emotions, medieval institutions and godlike
technology, was given to a fresh agent on the released tool. The folder holds the operator's `PROTOCOL.md`; every tool
call the agent made with its arguments and full result (`novel/inputs/`, `novel/results/` and the call log
`novel/mcp-transcript.jsonl`); the scripts it wrote (`novel/build/`); a backup of the Meaning Model's engine state
(`novel/engine-state.sqlite`); the whole construction history (`novel/construction-export.json`); and the tool's render
of the story (`novel/novel.md`). The story lives in the engine state: the world, the lives, the decisions and the
prose, in story graph `6e840daa…` on story model revision 17.

Rebuild the page's data from it with the published tool:

```sh
npm install
npx meaning-model-mcp --install-engine
node extract.mjs --run runs/rabbit-hole --out public/data/rabbit-hole.json
npm run serve
```

Typeset the story as a book PDF from the same render. It needs Chrome or Chromium; set `CHROME` if it is elsewhere.

```sh
node book.mjs rabbit-hole   # writes pdf/rabbit-hole.pdf
```

## Open the story's model with your own agent

The story's world model opens in the published Meaning Model server. From the repo folder, install the engine once,
work on a copy of the state, and add the server to Claude Code:

```sh
npx meaning-model-mcp --install-engine
cp runs/rabbit-hole/novel/engine-state.sqlite story-state.sqlite
claude mcp add story-model -e LIFE_SIM_STATE_FILE="$PWD/story-state.sqlite" -e MEANING_MODEL_ADDONS=storytelling -e MEANING_MODEL_READING=guides -- npx meaning-model-mcp
```

The story graph is `6e840daa393fbdd16608dff4c81c045dca622386be4e9f8d5d7c95816d45eb29`, read with the access scope
`story-author`. `life_narrative_render` on it gives the novel; `life_narrative_query` and `life_model_inspect` show how
it is built. Two known limits of this history: `life_construction_export` stops the server on it (the export is
already in `novel/construction-export.json`), and `life_model_questions` does not see the notes and draws, whose links
broke when the graph was rebound.

## License

The code is MIT, in [LICENSE](LICENSE). three.js is vendored under its own MIT license.
