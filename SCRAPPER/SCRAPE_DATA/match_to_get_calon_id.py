import os
import json

kpus = []
with open('KPU_WITH_PATH_4.json') as f:
    kpus = json.load(f)
    # only get communityID and name info.calon_id
    new_kpus = []
    for i in kpus:
        communityID = i['communityID']
        name = i['name']
        try:
          calon_id = i['info']['calon_id']
        except KeyError:
          print(f"Calon ID not found for {name}")
          calon_id = None
        
        new_kpus.append({'communityID': communityID, 'name': name, 'calon_id': calon_id})
        
    kpus = new_kpus
    

candidates = []
with open('candidates.json') as f:
    candidates = json.load(f)
    
    
for c in candidates:
  if c['calon_id'] == "1":
    c['calon_id'] = None
  
  for k in kpus:
      c_name = c['name'].lower().replace(' ', '').replace('.', '').replace(',', '')
      k_name = k['name'].lower().replace(' ', '').replace('.', '').replace(',', '')
    
      if c['communityID'] == k['communityID'] and c_name == k_name:
        c['calon_id'] = k['calon_id']
        break
          
          
with open('candidates_with_calon_id.json', 'w') as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)