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
running story, and `&still` to stop the slow orbit. `index.html` is a flat 2D view of the same data.

## Make data from a story run

The extractor reads a run's relay call log and an online SQLite backup of its engine database. It never calls the
run's own server, so it is safe while the agent works. It needs the Meaning Model with its engine: `npm install` brings
the published package, then `npx meaning-model-mcp --install-engine` fetches the engine for your platform. A checkout
named by `MEANING_MODEL_DIR` works too.

```sh
node extract.mjs --run <run folder> --out public/data/<name>.json
./live.sh <run folder> <name>   # refresh every minute while the agent works
```

`public/data/rabbit-hole.json` is *The Exceptions Queue*, a story written by an agent with Meaning Model 0.3.0 on
25 September 2026, from a brief about a comfortable "blue pill" world, a white rabbit, and Paleolithic emotions in a
world of godlike technology.

## License

MIT for the code. D3 and three.js are vendored under their own licenses.
