import os
import json

completes = []
with open('all_complete.json', 'r') as f:
    completes = json.load(f)
    completes = completes['candidates']

no_pics = []
for com in completes:
    try:
        if com['picUrl'] == '' and ('Bupati' in com['title'] or 'Wali Kota' in com['title'] or 'Walikota' in com['title']):
            no_pics.append(f"{com['name']} - {com['title']}")
        else:
            continue
    except:
        no_pics.append(f"{com['name']} - {com['title']}")


open('no_pics.txt', 'w').write('\n'.join(no_pics))
