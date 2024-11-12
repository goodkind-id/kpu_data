import json
import os

kpus = []
with open('KPU_WITH_PATH.json', 'r') as f:
    kpus = json.load(f)

no_urut_empty = []
for k in kpus:
    try:
        k['info']['no_urut']
    except:
        no_urut_empty.append(k['name'])

print(f"Total kpus: {len(kpus)}")
print(f"Total no urut empty: {len(no_urut_empty)}")

open('no_urut_empty.txt', 'w').write('\n'.join(no_urut_empty))