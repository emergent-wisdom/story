# Story Landscape

A live view of a story as an agent builds it with the [Meaning Model](https://github.com/emergent-wisdom/meaning-model).
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
npm run serve
```

Open http://localhost:8765/landscape.html?data=rabbit-hole. Add `&play` to start the replay, `&live` to follow a
running story, `&still` to stop the slow orbit, and `&read` to open the story. **Read the story** shows the text as
the Meaning Model renders it from the story graph (`life_narrative_render`), up to the replay's moment.

## Make data from a story run

The extractor reads a run's relay call log and an online SQLite backup of its engine database. It never calls the
run's own server, so it is safe while the agent works. It needs the Meaning Model with its engine: `npm install` brings
the published package, then `npx meaning-model-mcp --install-engine` fetches the engine for your platform. A checkout
named by `MEANING_MODEL_DIR` works too.

```sh
node extract.mjs --run <run folder> --out public/data/<name>.json
./live.sh <run folder> <name>   # refresh every minute while the agent works
node sync-run.mjs <run folder> <name>   # copy the run into runs/<name>/ for this repo
```

## The story in this repo

`runs/rabbit-hole/` is the story's run, copied while the agent works: the brief (`PROMPT.md`), the operator's
`PROTOCOL.md`, every tool call the agent made with its arguments and full result (`novel/inputs/`, `novel/results/`
and the call log `novel/mcp-transcript.jsonl`), the scripts it wrote (`novel/build/`), and a backup of the Meaning
Model's engine state (`novel/engine-state.sqlite`). The story lives in that state: the world, the lives, the
decisions, and the prose as it is written.

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

`public/data/rabbit-hole.json` is *The Exceptions Queue*, a story written by an agent with Meaning Model 0.3.0 on
25 September 2026, from a brief about a comfortable "blue pill" world, a white rabbit, and Paleolithic emotions in a
world of godlike technology.

## License

MIT for the code. three.js is vendored under its own license.
