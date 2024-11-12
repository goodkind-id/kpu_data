# merged all files in the data folder to one file called merge.json

import json
import os

data = []

communities = []
with open('communities.json') as f:
    communities = json.load(f)
    
def get_community(region):
    for community in communities:
        if region == "KABUPATEN KEP":
            region = "KABUPATEN KEPULAUAN SIAU TAGULANDANG BIARO"

        if region == "KABUPATEN KAB PEGUNUNGAN BINTANG":
            region = "KABUPATEN PEGUNUNGAN BINTANG"

        if region == "KABUPATEN PANGKAJENE KEPULAUAN":
            region = "KABUPATEN PANGKAJENE DAN KEPULAUAN"

        if region == "KOTABARU":
            region = "KABUPATEN KOTABARU"

        if region == "KOTAWARINGIN BARAT":
            region = "KABUPATEN KOTAWARINGIN BARAT"

        if region == "KOTAWARINGIN TIMUR":
            region = "KABUPATEN KOTAWARINGIN TIMUR"
        
        if "SUMATERA" in region:
            region = region.replace("SUMATERA", "SUMATRA")
        
        community_path = community['path'].replace('-', '').lower()
        
        region_path = region.replace(' ', '').lower()

        if region_path == community_path:
            return community

    return None

candidates = []

def merge_files(parent_dir):    
    for filename in os.listdir(parent_dir):
        with open(parent_dir + '/' + filename) as f:
            # region remove [number]- from filename and .json extension
            region = filename.split('-')[1].split('.')[0]
            
            item = json.load(f)
            
            for i in item:
                i['region'] = region
                i['communityID'] = get_community(region)['communityID']
                
                try:
                    cs = i['data']
                except:
                    cs = None
                
                if cs is not None:
                    for c in cs:
                        c['communityID'] = get_community(region)['communityID']
                        c['no_urut'] = i['no_urut']
                        
                        candidates.append(c)
                    
            
            data.append(item)

merge_files('data/Gubernur')
merge_files('data/Bupati')
merge_files('data/Walikota')

list_no_community_id = []
list_no_no_urut = []
list_no_calon_id = []

list_community_not_found = []

for c in candidates:
    if c['communityID'] is None or c['communityID'] == "":
        list_no_community_id.append(c)
    
    if c['no_urut'] is None or c['no_urut'] == "":
        list_no_no_urut.append(c)
        
    if c['calon_id'] is None or c['calon_id'] == "":
        list_no_calon_id.append(c)
        

community_exists = [i['communityID'] for i in candidates]

for c in communities:
    if c['communityID'] not in community_exists:
        list_community_not_found.append(c)
        
print(f"Total candidates: {len(candidates)}")
print(f"Total candidates with no community_id: {len(list_no_community_id)}")
print(f"Total candidates with no no_urut: {len(list_no_no_urut)}")
print(f"Total candidates with no calon_id: {len(list_no_calon_id)}")
print(f"Total community not found: {len(list_community_not_found)}")
        
# with open('merge.json', 'w') as f:
#     json.dump(data, f, ensure_ascii=False, indent=2)
    
# with open('candidates.json', 'w') as f:
#     json.dump(candidates, f, ensure_ascii=False, indent=2)