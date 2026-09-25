# Calling the Meaning Model tools in this folder

A relay process is already running here. It holds one live MCP connection to the Meaning Model server (base tools plus the storytelling add-on; the Jev estimator is configured). Run every command from this folder.

- Call a tool: write its arguments as JSON to `inputs/<name>.json`, then
  `node c.mjs <tool_name> inputs/<name>.json <save-name>.json [maxChars]`.
  A compact view prints; the full result is saved in `results/<save-name>.json`.
- Lists: `node relay.mjs '{"op":"list_tools","save":"tools.json","quiet":true}'`, and the same with `list_resources` and `list_prompts`.
- Read a resource: `node relay.mjs '{"op":"read_resource","uri":"<uri>","save":"<name>.json","quiet":true}'`, then read `results/<name>.json` (the text is in `contents[0].text`).
- Get a prompt: `node relay.mjs '{"op":"get_prompt","name":"<prompt name>","save":"<name>.json","quiet":true}'`.
- A tool's input schema: `node relay.mjs '{"op":"tool_schema","name":"<tool name>","save":"schema-<tool>.json","quiet":true}'`.
- One value from a saved result: `node g.mjs results/<file>.json <dot.path>`.

Results can be large; read saved files in pieces rather than printing them whole.
