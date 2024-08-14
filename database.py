import MySQLdb 
import json
import pandas as pd

connection = MySQLdb.connect(host="localhost",    # your host, usually localhost 
                     user="asx5566123",         # your username 
                     passwd="asx5566789",  # your password 
                     db="project")        # database name 


cursor = connection.cursor()

# 執行 SQL 查詢
cursor.execute("SELECT * FROM disease_id")

# 獲取所有症狀
disease_cursor = cursor.fetchall()
diseases = []

for disease in disease_cursor:
    diseases.append(disease[0])

print(len(diseases))

# 尚未配穴
acu_disease = {}

# 執行 SQL 查詢
cursor.execute("SELECT * FROM match_table")

# 獲取所有穴位症狀配對
acu_disease_cursor = cursor.fetchall()
print(len(acu_disease_cursor))

for disease in diseases:
    temp = []
    for row in acu_disease_cursor:
        temp_acu = row[0]
        temp_disease = row[1]
        if disease == temp_disease:
            temp.append(temp_acu)
    acu_disease[disease] = temp

print(len(acu_disease))


# 將資料寫入excel
excel_header = ['主治']
output_list = []

for symptom in acu_disease:
    temp = [symptom]
    output_list.append(temp)
print(output_list)
df = pd.DataFrame(output_list)

with pd.ExcelWriter("symptom.xlsx") as writer:
    df.to_excel(writer, sheet_name="Sheet1", header=excel_header, index=False)


# 建立配穴資料庫
cursor.execute("SELECT * FROM main_table")
match_acu_cursor = cursor.fetchall()
data = {}


for row in match_acu_cursor:
    acu = row[0]
    all_info = row[6]
    if all_info != None:
        all_info = all_info.split("。")
        temp_list = []
        for info in all_info:
            if '\xa0\xa0' in info or '\xa0' in info or info == '' or info == ' ':
                continue
            else:
                temp = info.split("：")
                dic = {
                    temp[0]:temp[1].split("、")
                }
                temp_list.append(dic)

    data[acu] = temp_list

with open("match_acu.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

