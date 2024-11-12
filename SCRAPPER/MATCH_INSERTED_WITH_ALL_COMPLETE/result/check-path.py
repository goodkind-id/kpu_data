import os
import json

exists = []
with open('latest_all_complete.json', 'r') as f:
    exists = json.load(f)
    exists = exists['candidates']


walikotas = []
for x in exists:
    if "Bupati" in x['title']:
        walikotas.append(x)
exists = walikotas

empties = []
paths = []
for i in exists:
    try:
        if i['path'] == '':
            empties.append(f"{i['communityID']}-{i['name']}")
        else:
            paths.append(i['path'])
    except:
        empties.append(f"{i['communityID']}-{i['name']}")

existing_paths = []
double_paths = []
for p in paths:
    if p in existing_paths:
        double_paths.append(p)
    else:
        existing_paths.append(p)

print(f"Total exists: {len(exists)}")
print(f"Total empties: {len(empties)}")
print(f"Total doubles: {len(double_paths)}")
print(f"Total paths: {len(paths)}")

open('empties.txt', 'w').write('\n'.join(empties)) 
open('doubles.txt', 'w').write('\n'.join(double_paths)) 
open('paths.txt', 'w').write('\n'.join(paths)) 