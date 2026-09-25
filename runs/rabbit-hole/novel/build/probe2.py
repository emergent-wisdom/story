import json, re, subprocess, sys
t=open('results/res-example-minimal-model-and-graph.txt').read()
base=json.loads(re.findall(r'```json\n(.*?)```', t, re.S)[1])['model']
def run(m,label):
    json.dump({'model':m}, open('inputs/probe-validate.json','w'))
    out=subprocess.run(['node','c.mjs','life_model_validate','inputs/probe-validate.json','probe-validate.json','600'],capture_output=True,text=True).stdout
    print(label, '=>', out.strip().split('\n')[-1][:500] if 'isError=true' in out else 'VALID')
kind, val = sys.argv[1], json.loads(sys.argv[2])
m=json.loads(json.dumps(base))
if kind=='region': m['meaning_model']['events'][4]['region']=val
elif kind=='event_extra': m['meaning_model']['events'][4].update(val)
else: m['meaning_model'][kind]=[val]
run(m, kind)
