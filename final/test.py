import os, json


directory = "../match_acu"


with open("../data.json", 'r', encoding='utf-8') as file:
    data = json.load(file)



for root, dirs, files in os.walk(directory):
    if '配穴.json' in files:
        file_path = os.path.join(root, '配穴.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            info = json.load(file)
        acu_name = next(iter(info))
        data[acu_name]["配穴資訊"] = info[acu_name]
        del data[acu_name]['臨床應用與配伍']

with open("data.json", 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(data)