import json, re, subprocess, sys
t=open('results/res-example-minimal-model-and-graph.txt').read()
base=json.loads(re.findall(r'```json\n(.*?)```', t, re.S)[1])['model']
def probe(mutate, label):
    m=json.loads(json.dumps(base)); mutate(m)
    json.dump({'model':m}, open('inputs/probe-validate.json','w'))
    out=subprocess.run(['node','c.mjs','life_model_validate','inputs/probe-validate.json','probe-validate.json','600'],capture_output=True,text=True).stdout
    print(label, '=>', out.strip().split('\n')[-1][:400] if 'isError=true' in out else out[:300].replace('\n',' '))
fields=json.loads(sys.argv[1])
probe(lambda m: m['meaning_model'].__setitem__('concepts',[fields]), 'concept')
