import json, sys, re
G = sys.argv[1]; src = sys.argv[2]; req = sys.argv[3]; start = int(sys.argv[4])
text = open(src).read()
parts = [p.strip() for p in re.split(r'\n=====\n', text) if p.strip()]
PROV = ["rabbit-hole-run; prose written by the calling LLM under delegation, directly into the graph"]
nodes, edges = [], []
for i, p in enumerate(parts):
    n = start + i
    nid = f"part.{n:02d}"
    nodes.append({"id": nid, "node_type": "story_part", "role": "story_passage", "text": p, "render": "include", "training": "exclude",
                  "epistemic_status": "fictional_artifact", "evidence_type": "fictional_canon",
                  "authority": {"source": "calling-llm-under-delegation", "weight": 1}, "provenance": PROV})
    edges.append({"id": f"story.contains.{nid}", "source": {"kind": "node", "node_id": "story"}, "target": {"kind": "node", "node_id": nid},
                  "family": "structural", "relation": "contains", "order": 1000 + n, "provenance": PROV})
b = {"requestId": req, "previousGraphHash": G, "narrativeBatch": {"schema": "life-sim-rust-narrative-batch/v1", "previous_graph_hash": G,
     "reason": f"Add prose parts {start}-{start+len(parts)-1}.", "provenance": PROV, "add_roots": [], "add_nodes": nodes, "add_edges": edges}}
json.dump(b, open(f"inputs/{req}.json", "w"))
print(len(parts), sum(len(p.split()) for p in parts))
