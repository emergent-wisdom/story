# Rabbit-hole story run, 2026-09-25

A participant at the event described what they wanted the story to be about and supplied the prompt: a comfortable "blue pill" world,
the white rabbit, the rabbit hole of crypto and DeFi, and Paleolithic emotions, medieval institutions and godlike
technology. Claude Opus 5.5 Max then wrote the story autonomously using the released Meaning Model.
The story is visualized in this repo while it is written.

- **Tool.** Meaning Model 0.3.0, release [v0.3.0](https://github.com/emergent-wisdom/meaning-model/releases/tag/v0.3.0)
  (commit 9e7fc76): the release engine, the storytelling add-on, guides-first reading, and the Jev estimator
  configured with no cap.
- **The agent.** Claude Opus 5.5 Max, in a fresh session opened in `novel/`, with no memory loaded, given `PROMPT.md`: the brief verbatim, the
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
- About 18:35: the agent wrote the twelve parts into the graph, about 5,800 words (short of 16,000 because of the stage
  deadline), and saved the tool's render as `novel/novel.md`. The final graph is `abe50dac…`. The relay then dropped
  ("Not connected"), so the agent could not run the export.
- About 18:40 to 18:47: Henrik asked the agent for stronger character voices and more processes. The server behind the
  relay had stopped; the agent asked Henrik, and with his yes restarted the relay. The estimator was not configured
  after the restarts. The agent split the prose into twelve part nodes, recorded a voice assessment before and after
  the revision with quotes per character, replaced each part in place, and added 15 processes and sampled whole-life
  trajectories for the three principals. The story was retitled *Twelve Words*. The final graph is `6e840daa…`, the
  story model is at revision 17 (`cf7514e6…`), and the text is about 8,400 words.
- `life_construction_export` stopped the server each time it was called on this history (three of three, in the
  agent's report). The operator made `novel/construction-export.json` for the final graph from the saved engine state
  with `export-run.mjs` and the published package.
- Open at the end, in the agent's report: `life_model_questions` shows no thoughts and eight undrawn decisions because
  repeated rebinds broke the links to the notes and draws, which are themselves in the graph; the prose went in as
  direct graph additions and edits, not through the scene reviews and the release step; and the story is short of
  the 16,000 words agreed.

## This copy

The original event manuscript and PDF, model-building scripts, and selected call inputs/results remain public.
On October 3, 2026, the raw `novel/engine-state.sqlite`, `novel/mcp-transcript.jsonl`, their hash-bound construction
export, the obsolete viewer snapshot, and redundant inputs/results containing quoted human coordination were
withdrawn from the current tree. They were preserved privately before removal. The account above describes the
historical procedure; its file references do not promise that every original operational artifact is distributed.

The removed export was not edited in place: changing its notes would change the recorded graph hashes and require
a new replayed publication lineage. Exact raw operational replay is no longer available from this checkout. The
current clean Twelve Words download has its own selected publication lineage and is not claimed to be a complete
replacement for the original event history. The event's readable text and retained model sources are unchanged.

`sync-run.mjs` now stages saved runs only in ignored `.local-work/imported-runs/`; publication requires a separate
review of a selected export. The existing relay and model-building scripts document how the event was conducted,
but should be used with a private run rather than treated as a complete executable copy of the original archive.
