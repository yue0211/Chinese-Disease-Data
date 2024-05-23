import pandas as pd
import json


with open("../final/data.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

all_symptom = set()

for acu in data.keys():
    for symptom in data[acu]["主治"]:
        if symptom != "":
            all_symptom.add(symptom)

result = {}
max_acu = 0

for symptom in all_symptom:
    temp = []
    for acu in data.keys():
        if symptom in data[acu]["主治"]:
            temp.append(acu)
    result[symptom] = temp
    max_acu = max(len(temp), max_acu)

excel_header = ['主治']
output_list = []

for value in range(1, max_acu+1):
    excel_header.append(f"穴位{value}")

for symptom in result:
    temp = [symptom]
    for acu in result[symptom]:
        temp.append(acu)
    output_list.append(temp)
print(output_list)
df = pd.DataFrame(output_list)


with pd.ExcelWriter("disease_match_acu.xlsx") as writer:
    df.to_excel(writer, sheet_name="Sheet1", header=excel_header, index=False)