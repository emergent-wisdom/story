# Rabbit-hole story run, 2026-09-25

Henrik Westerberg's story idea (a comfortable "blue pill" world, the white rabbit, the rabbit hole of crypto and DeFi,
and Paleolithic emotions, medieval institutions and godlike technology), given to a fresh agent on the released tool,
as a user would. The story is visualized in this repo while it is written.

- **Tool.** Meaning Model 0.3.0, release [v0.3.0](https://github.com/emergent-wisdom/meaning-model/releases/tag/v0.3.0)
  (commit 9e7fc76): the release engine, the storytelling add-on, guides-first reading, and the Jev estimator
  configured with no cap.
- **The agent.** A fresh session opened in `novel/`, with no memory loaded, given `PROMPT.md`: the idea verbatim, the
  relay mechanics, 15-minute rounds, the safety rules and an export at the end.
- **The relay.** `novel/relay.mjs` holds one MCP connection to the server and logs every call and its full result to
  `novel/mcp-transcript.jsonl`. The agent writes a call's arguments to `novel/inputs/` and calls
  `node c.mjs <tool> inputs/<args>.json <save>.json`; the result is saved in `novel/results/`.
- **The operator.** While the agent works, the operator reads only the relay call log, never the agent's transcript.

## Log (UTC)

- 17:09: the relay started with a fresh engine state. Before the start the operator made one read-only call, the tool
  list, saved in `operator/`.
- 17:58: the desktop app quit, which stopped the agent (last call 17:52) and the relay. The relay was restarted; the
  engine state and the log were unchanged.
- 17:59: the agent resumed on the restarted relay.
- About 18:15: Henrik asked the agent to finish the whole story, about 16,000 words in twelve parts, in one pass
  rather than 15-minute rounds, with the story inside the graph and nothing written outside it. The PDF is made by
  the operator from the graph.

## This copy

`novel/engine-state.sqlite` is an online backup of the engine state, taken while the agent works. `novel/relay.mjs`
names the published package instead of the operator's checkout. The relay's queue files, process ids and logs are
left out. `sync-run.mjs` at the repo root makes this copy and refuses to write one that holds a local path or a
configured credential.
