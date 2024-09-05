# 爬蟲: 知識圖譜
import requests,bs4,json
import pandas as pd


excel_header = ['證候', "症狀", "關聯的中醫疾病", "關聯的西醫疾病", "門類"]
output_list = []
data = []


for page in range(1, 14):
    Headers = {"Content-Type":"application/json;charset=UTF-8","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
    payload = {"nodeTypeId": "5", "currentPage": page, "pageSize": 50, "lang": "zh"}
    Response = requests.post(url="http://112.124.18.136:8082/api/front/getSyndromesWithPage", headers=Headers, json=payload)
    Response.encoding = "utf-8" #為了避免爬蟲爬到的文字變成亂碼
    text = json.loads(Response.text)
    for number in range(0, 50):
        if page == 13 and number == 24:
                break
        else:
            one = {
                "證候" : text["data"][number]["syndromename"],
                "症狀" : text["data"][number]["symptom"],
                "關聯的中醫疾病" : text["data"][number]["diseasetcm"],
                "關聯的西醫疾病" : text["data"][number]["diseasemm"],
                "門類" : text["data"][number]["men"]
            }
            data.append(one)

for item in data:
    temp = [item.get('證候', ''),
            item.get('症狀', ''),
            item.get('關聯的中醫疾病', ''),
            item.get('關聯的西醫疾病', ''),
            item.get('門類', '')]
    output_list.append(temp)

# 將資料轉換為 DataFrame
df = pd.DataFrame(output_list, columns=excel_header)

# 將 DataFrame 寫入 Excel
df.to_excel('output.xlsx', index=False)