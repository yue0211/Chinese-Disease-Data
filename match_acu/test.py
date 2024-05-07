import json, os, re

lines = ""

# 讀取JSON檔案
with open('../data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)



with open('prompt.txt', 'r', encoding='utf-8') as f:
    for line in f:
        lines += line

temp = lines

for name in data.keys():
    english_words = re.findall(r'[a-zA-Z]+', data[name]["臨床應用與配伍"])
    lines = temp
    lines = lines.replace("()",f"({english_words[0]})")
    lines = lines.replace("[]",f"({english_words[-1]})")
    lines = lines.replace("{}",name)
    lines = data[name]["臨床應用與配伍"] + "\n\n" +lines
    os.makedirs(name, exist_ok=True)
    file_path = os.path.join(name, f"{name}.txt")
    acu_path = os.path.join(name, f"配穴.json")
    with open(file_path, 'w') as file:
        file.write(lines)
    with open(acu_path, 'w') as file:
        pass


