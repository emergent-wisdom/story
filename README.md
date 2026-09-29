# Twelve Words and The Book of Conditions

Two stories built with the [Meaning Model](https://github.com/emergent-wisdom/meaning-model), with their worlds, character processes, physical settings and authored understanding available in one shared viewer.

**[Explore both stories in the interactive viewer](https://emergentwisdom.org/meaning-model/twelve-words/?reading=off&view=together&everything=&timeView=together)** — opens in your browser without installation. Use **Model** to switch between the books and their fictional authors' lives.

**Current editions, September 29, 2026:**

- **[Twelve Words](stories/twelve-words.md)** — the continuing version of the novel first written live at the Stockholm Claude Community event on September 25.
- **[The Book of Conditions](stories/the-book-of-conditions.md)** — an alternative history of Babbage, Lovelace and a bounded calculating undertaking.

These Markdown files are exact renders of the current public story graphs. The viewer's **Read full story** opens the same complete manuscript. The **Model** menu also opens the modeled lives of the fictional authors, Faye Titcombe and Nora Vale.

These examples are separate downloads. Installing Meaning Model MCP or the standalone viewer does **not** download either story. This repository and its release assets provide the optional models.

## Download a story model

- [Download The Book of Conditions](https://github.com/emergent-wisdom/story/raw/refs/heads/main/models/the-book-of-conditions.meaning-model.json)
- [Download Twelve Words](https://github.com/emergent-wisdom/story/raw/refs/heads/main/models/twelve-words.meaning-model.json)

Save the JSON file on your computer. With [Meaning Model MCP installed in your AI app](https://github.com/emergent-wisdom/meaning-model#readme), tell the assistant:

> Import the Meaning Model story file I downloaded, then open its latest graph in the viewer.

Give it the downloaded file's location. The assistant uses `life_construction_import` with that absolute file path, then `life_model_viewer_open` with the returned `headGraphHash`. The Book uses the access scope `book.07r2.authoring`; Twelve Words uses `story-author`. Each download includes its fictional author's modeled life. The viewer makes that life available alongside the story. Import both files and ask **“Open these stories together”** to switch between them. You can continue writing from either imported edition.

These are native MCP construction bundles; no code, extraction step or source checkout is needed. They contain the current published world, prose and attributed understanding, including story reviews. They start new publication lineages so importing or exporting them does not bring in the earlier private working history. Exact download checksums are the `fileSha256` values in the [publication manifest](public/PUBLICATION-MANIFEST.json).

## Open the viewer

Use the [interactive viewer on Emergent Wisdom](https://emergentwisdom.org/meaning-model/twelve-words/?reading=off&view=together&everything=&timeView=together), or run the same viewer locally:

```sh
git clone https://github.com/emergent-wisdom/story && cd story
npm install
npm run serve
```

Requires Node.js 22.18 or later. Open the local URL printed by the command. The reviewed snapshots load immediately; no engine installation is needed just to explore them.

**Show it as** switches between Processes (together or layers), Tree, Terrain, Graph, Structure and Space in one page. **Coarse view** gives the overview; more detail reveals subprocesses. Select a record to inspect its meaning and links. Use **Recenter** or Home to restore the overview. Physical positions come from declared coordinates and reference frames; the other graph layouts are not geography.

This repository uses the [shared viewer launcher](https://github.com/emergent-wisdom/meaning-model-viewer) and the exact interface bundled with **Meaning Model MCP 0.6.0**. Existing `/processes.html` and `/landscape.html` event links open the current Twelve Words edition in their corresponding representation. An explicit current dataset choice remains selected. There is no separate story-specific viewer to maintain.

For your own models, install Meaning Model MCP in your AI app and ask **“Open this model.”** The assistant returns a local snapshot link. Ask **“Open these models together”** to compare selected models. When writing, ask **“Keep the viewer following as we work.”** The assistant opens the story's `graphHash` with `mode: "live"`; saved graph revisions update the model and prose at the same local URL. Updates preserve your reading context through guarded page refreshes and pause while you interact or play. A fork or inaccessible revision pauses following. Exact snapshot links remain available. No separate viewer checkout is required for normal MCP use. The hosted website shows the reviewed published editions and does not follow private drafts.

## What is published

[`models/`](models/) holds the two importable MCP downloads. [`public/models/`](public/models/) holds matching viewer snapshots for the stories and their fictional authors. The [publication manifest](public/PUBLICATION-MANIFEST.json) identifies the exact graph and model revisions, manuscript checksums and downloadable file checksums. The models are the same in the downloads, manuscripts and viewer.

The public models retain authored thoughts, critical story reviews, revision findings, process values, spatial declarations and passage-to-Event links. Private user conversation and incidental execution details are summarized. Working databases, relay transcripts and earlier private construction histories are not included in these current editions. Publication projections have their own genuine model and graph identities; the original private authoring graphs remain unchanged. Twelve Words also includes the audited initial author-life model because historical story records explicitly refer to it.

## Original September 25 event archive

The original *Twelve Words* run was made for the Stockholm Claude Community event **Push the limits with Fable 5.1 n Opus 5.5**, September 25, 2026. A participant at the event described what they wanted the story to be about and supplied the prompt: a comfortable “blue pill” world, the white rabbit, and Paleolithic emotions, medieval institutions and godlike technology. **Claude Opus 5.5 Max** then wrote the novel autonomously, live at the event, using Meaning Model [v0.3.0](https://github.com/emergent-wisdom/meaning-model/releases/tag/v0.3.0).

The original event [text](runs/rabbit-hole/novel/novel.md) and [book PDF](pdf/rabbit-hole.pdf) remain unchanged. They differ from the current editions linked above. The [`runs/rabbit-hole/`](runs/rabbit-hole/) archive preserves the event's brief, protocol, call inputs/results, scripts, construction history and database for reproducibility, with the prompt and writing credits corrected in the protocol; it does not contain the later private Writer workspace.

[![The original event processes view](media/the-rabbit-hole-processes.png)](media/the-rabbit-hole-processes.mp4)

**[Watch the original interface (51-second video)](media/the-rabbit-hole-processes.mp4).** A new recording of the current interface is being prepared.

To inspect the original run using today's shared interface:

```sh
npx meaning-model-mcp --install-engine
npm run serve -- --run runs/rabbit-hole
```

The launcher reads an online backup and does not change the archive. The engine is needed to extract a run, but not to view the already prepared current snapshots.

## Work with a saved run

```sh
npx meaning-model-mcp --install-engine
npm run extract -- --run runs/rabbit-hole --out .local-work/rabbit-hole.json
npm run serve -- --data .local-work
```

Generated exports include the author's model, notes and construction record. Keep them in the ignored `.local-work/` directory until reviewed for publication. A story's authored understanding and critical reviews can remain part of its public model; private conversations, personal information and secrets must be removed deliberately.

For an agent actively working in a saved run, `npm run serve -- --run <folder> --live` checks the run once a minute and follows revisions in every representation. It waits for playback to pause before reloading the current view. Ordinary MCP links remain immutable snapshots unless the assistant opens a story graph with `mode: "live"`.

Existing Writer contributors can use `npm run view:writer` with their already running Writer relay. `MEANING_MODEL_RELAY` may name that relay's `relay.mjs`; the default is this checkout's ignored `work/relay.mjs`. This adapter discovers the latest unambiguous saved story and asks the existing MCP (0.5.1 or later) to open it in live mode. The same link follows later saved revisions. It starts no second database writer and is not needed to view the public snapshots.

For the current stories, use the downloads above. To reproduce the original event world with your own agent, use a private copy of the archived database:

```sh
npx meaning-model-mcp --install-engine
mkdir -p .local-work
cp runs/rabbit-hole/novel/engine-state.sqlite .local-work/story-state.sqlite
claude mcp add story-model -e LIFE_SIM_STATE_FILE="$PWD/.local-work/story-state.sqlite" -e MEANING_MODEL_ADDONS=storytelling -e MEANING_MODEL_READING=guides -- npx meaning-model-mcp
```

The original event graph is `6e840daa393fbdd16608dff4c81c045dca622386be4e9f8d5d7c95816d45eb29`, with scope `story-author`. Ask the agent to inspect and render that graph. Use the publication manifest to distinguish it from the later current public editions.

## Meaning Model

- [Source, releases and documentation](https://github.com/emergent-wisdom/meaning-model)
- [MCP package on npm](https://www.npmjs.com/package/@emergent-wisdom/meaning-model-mcp)
- [Paper: The Meaning Model](https://doi.org/10.5281/zenodo.22313515)
- [Emergent Wisdom](https://emergentwisdom.org)

The code is MIT; see [LICENSE](LICENSE). Third-party viewer notices ship with the MCP package.
