import os
import json

inserteds = []
with open('leaders_with_path+calonid_4.txt', 'r') as f:
    for line in f:
        clean_line = line.rstrip(',\n')
        if clean_line:
            inserteds.append(json.loads(clean_line))
        else:
            print(line)

print("===================")

completes = []
with open('new_all_complete.json', 'r') as f:
    completes = json.load(f)
    completes = completes['candidates']


# insert_with_no_nomor_urut = []
# for ins in inserteds:
#     try:
#         ins['no_urut']
#     except:
#         insert_with_no_nomor_urut.append(f"{ins['name']}")

# open('result/insert_with_no_nomor_urut.txt', 'w').write('\n'.join(insert_with_no_nomor_urut))


matches = []
for com in completes:

    for ins in inserteds:
        com_community_id = com['communityID']
        ins_community_id = ins['communityID']

        com_name = com['name']
        ins_name = ins['name']

        com_title = com['title']
        ins_title = ins['title']

        com_no_urut = com['info']['no_urut']
        try:
            ins_no_urut = ins['no_urut']
        except:
            continue

        ins_path = ins['path']

        com_is_wakil = True if "Wakil" in com_title else False
        ins_is_wakil = True if "Wakil" in ins_title else False

        if (com_is_wakil == ins_is_wakil) and (com_no_urut == ins_no_urut) and (com_community_id == ins_community_id):
            com['path'] = ins_path

            matches.append(f"{ins_name} - {ins_path}")

            break

not_matches = []
matches_list_paths = [x.split(' - ')[1] for x in matches]

for ins in inserteds:
    if ins['path'] not in matches_list_paths:
        not_matches.append(f"{ins['name']} = {ins['path']}")

doubles = []
all_items = []
for ins in inserteds:
    if ins['path'] in all_items:
        doubles.append(ins['path'])
    else:
        all_items.append(ins['path'])

print(f"Total inserteds: {len(inserteds)}")
print(f"Total matches: {len(matches)}")
print(f"Total not matches: {len(not_matches)}")
print(f"Total doubles: {len(doubles)}")

open('result/matches.txt', 'w').write('\n'.join(matches))
open('result/not-matches.txt', 'w').write('\n'.join(not_matches))
open('result/matches_list_paths.txt', 'w').write('\n'.join(matches_list_paths))
open('result/doubles.txt', 'w').write('\n'.join(doubles))

completes = {
    "candidates": completes
}

with open('result/new_all_complete.json', 'w') as f:
    json.dump(completes, f, ensure_ascii=False, indent=2)