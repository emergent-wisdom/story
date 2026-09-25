import json, sys, re
# usage: replace_parts.py <graphHash> <newtext file> <requestId>
G, src, req = sys.argv[1], sys.argv[2], sys.argv[3]
cur = json.load(open('results/query-full.json'))
T = {n['id']: n['text'] for n in cur['nodes'] if n['id'] in ('part.01', 'part.07')}
old = {}
for nid, start in (('part.01', 1), ('part.07', 7)):
    chunks = T[nid].split('\n\n## ')
    parts = [chunks[0]] + ['## ' + c for c in chunks[1:]]
    for i, t in enumerate(parts): old[f'p{start+i:02d}'] = t
new = [p.strip() for p in open(src).read().split('\n=====\n') if p.strip()]
ops = []
for t in new:
    m = re.match(r'## (\w+):', t)
    num = ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve'].index(m.group(1)) + 1
    pid = f'p{num:02d}'
    ops.append({"kind": "replace_text", "nodeId": pid, "expectedText": old[pid], "text": t})
    print(pid, len(old[pid].split()), '->', len(t.split()))
json.dump({"requestId": req, "graphHash": G, "accessScopes": ["story-author"], "reason": "Voice revision (the human asked to enhance the character voices): each speaker's words and perceptions rewritten from their modeled lives, per assessment.voice.before.", "operations": ops}, open(f'inputs/{req}.json', 'w'))
