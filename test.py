import pandas as pd


df = pd.read_excel("disease_match_acu.xlsx")

all_symptom = df.iloc[:, 0].tolist()

print("資料庫內包含的症狀數量:", len(all_symptom))


symptoms = ["打噴嚏", "流鼻涕或流鼻水", "鼻塞", "眼睛癢"]  # 眼睛分泌物增多(資料庫沒此症狀)
no_symptoms = ["全身酸痛", "發燒", "咽喉痛"]
print("\n有以下病名和症狀: ", symptoms)
print("\n沒有以下病名和症狀: ", no_symptoms)

# 未包含配穴
acus = []
for symptom in symptoms:
    temp = df.iloc[all_symptom.index(symptom), 1:].dropna().tolist()
    acus.append(temp)
    # print(f"\n{symptom}:", temp)
acus = set(sum(acus, []))
print("\n穴道個數: ",len(acus))
print("未包含配穴資訊: ",acus)



# 列出不能存在的穴道
no_acus = []
for symptom in no_symptoms:
    temp = df.iloc[all_symptom.index(symptom), 1:].dropna().tolist()
    no_acus.append(temp)
    # print(f"\n{symptom}:", temp)
no_acus = set(sum(no_acus, []))
# print("\n不能包含以下穴道: ",no_acus)

# 將不能存在的穴道刪除
for no_acu in no_acus:
    if no_acu in acus:
        acus.discard(no_acu)
print("\n穴道個數: ",len(acus))
print("未包含配穴資訊: ",acus)



