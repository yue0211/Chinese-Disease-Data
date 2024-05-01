import requests,bs4,re,json

data = {
    "十四經絡" : {
        "url" : "https://acupun.site/Search14_channel.aspx",
        "__VIEWSTATE" : "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",
        "__VIEWSTATEGENERATOR" : "64D098A0",
        "__EVENTVALIDATION" : "/wEdAEv5hhUsxbeJD7VwWAq0dtiQ+nnA2puEjF8AABRhJpKcodAye43Mf8N87hMBnj7ALGk2dj15cD40+RBSuGpkqZhP94aTqE6G7/Obw3PcjdF8qXmYkHS+SHHqI7G+fvLVIrvTSUfxNuRYdEGj/IyjlrblG54UD0ZJliRZvmJ5vEE05Yyx6LKLu5J519fDhLBZwAseV787VRyqjJiOkAfwmWLpZjY5Blkqko/caM82prENjh7pe8dcp1JdQi4fSq1d2UtJN7E2gK1UfqqhrKue3iobWqxmP/EQZ87DiYq33V7wHGARiK2iDLKlP7237WeRfNGxjNvgo+ZdxIifMCi+kRys2DBQmBCu6zJ8wVr9fSKkggKNJKbYO3CN0sphkiImu09fjsFvZB8XLuQlrwFFcMUFZy4orMRq8wWjNrioUCNIFeFkx6KrZ0AXPGkgBLwxUjfir0kScSwOBxrdOj5nF4j7I37dPUZ3EBTzB45i/e1jm6w8/Kec4HW0EYLtmw2Nkb1O4Bx/+pUVyXwTUM8C4TTvo6wNNO8phsZdkWN3dhqGcwcz3AdzDtTOwB9hmB0oy0+XxlYiBrMUEauzCsxP/BsAOeJQkSnkoBWg44smp3nQ83fSzuYjnqOD9B2Z/0SrSS0qRZlWrGCMM6JbMOrvTlmgreN6ApPYu77xvfPbaVyHzz/T9kK7pok41TgcKzAAWsFrTGNSLtZumB2o4yBgyJOF51+WFySEKci/AbNgprbinmpH4lfXrYh3nTtyXkcXXn5QdTodI126u3EMqVbYVQSS58Q8oe6uOm8aMR7QCatmA1ZePo8cyeTBdzmhTZADJBpd+Tf3ttkKTLcbr0y7zRi0BMJpQACLBYhq7hi1mjX8jbGdhraT/RFx3DUHSgvI7vQepgPSmUzZLzDqH2FJlkhhDeXSkMX78QPKa8BWgcKkTAOjpfCnxIkU249u4Wtl1IaVxtKOirxhHnKn/e8pDuRB2My5hn4eZHFfUYbUs8+NB/BeSQjrFDbd874+Mu6sOJOJnVOB8Hieti05XRzFqSq++qzf7fpHop/iiXfkj74Wr3MLoCaWVNmouOc2Z9NbOIMsUn1NcbqmVCnfrxD88mKMs++tRlPRVJewnf8fs+57I2AvIaby4v+gCdilkhc2zIFjSpZVaV/vtm7LJsQWjG6i7IA3LIV+bbDLSwkbp9Ao3zZTFbmh/6TOIMW3y6NmUzN73O9rsxsHhoUCm5zr1udZJIpzoUD6chsLBIk/8L88UjaxydCr6VAO1rLUncTn/JT6i33/G9yi8sI4nMmdUFK1CJNhpcwg8nFARaMEGRlN99mVdZ0eQiAFkN47Z8/fc/kDy8tj1ItJQ1btf5vm5U4JJo5acSKa4TuyujwFXmMRPQyaApvK2zMsy/our9N1AuzkuHf9GjdooyykYFb3mzI4QnowyOolyyoY9gJX6lpthJ16kjfeDqaAQIgLqkTXZ3R2Jt9kL4X8GGyJPIT8DC9xlZSqSKC6kM7O9+VINzJIccXGD5JcN8s+2KqBE/uzVxVRvzTckaBi+xAnoYBjKqniqgOCatg8aRJOXN3OLcogCa/DdGH9YviVsrgv5CwEwCSu+jZkKcVP+tvsei6agp4W4ZG55VTuPT92852KdVIo6Q=="
    }
}

Headers = {
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie":"ASP.NET_SessionId=b4jkrbwtcdzb0ceenbogbpaq"
}

numbers = [7, 8, 7, 8, 7, 7, 7, 7, 4, 4, 5]

all_symptom = set() #所有症狀

common_viewstate = "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kI3nqLEfB2g8KwAEAQAWCB8EBQbkuLvmsrsfBQUG5Li75rK7HwYFBuS4u+ayux8HaBYCZg9kFoYBAgEPZBYGAgEPDxYCHgRUZXh0BQNCTDFkZAICDw8WAh8IBQbnnZvmmI5kZAIDDw8WAh8IBdAC6KeS6Iac54KO44CB6KaW57ay6Iac54KO77yM5aSc55uy77yM6KaW56We57aT54KO44CB6KaW56We57aT6JCO57iu44CB6Z2S5YWJ55y844CB5pep5pyf6LyV5bqm55m95YWn6Zqc77yM6KeS6Iac55m95paR44CB57+854uA6IOs6IKJ44CB55mU55eH5oCn5byx6KaW44CB6KaW57ay6Iac5YuV6ISI6Zi75aGe44CB6KaW57ay6Iac6Imy57Sg6K6K5oCn44CB57WQ6Iac54KO44CB5rea6IW654KO44CB5rea5ZuK54KO44CB5rKZ55y844CB6Zu75YWJ5oCn55y854KO44CB5pac6KaW44CB6Z2i56We57aT6bq755e544CB55y86Lyq5Yyd6IKM55eZ5pSj77yM5b+D5YuV6YGO6YCf77yM6L+R6KaW55y8ZGQCAg9kFgYCAQ8PFgIfCAUDQkwyZGQCAg8PFgIfCAUG5pSi56u5ZGQCAw8PFgIfCAXtAeWJjemhjeeXm+OAgeiCjOe3iuW8teaAp+mgreeXm+OAgee1kOiGnOeCjuOAgeinkuiGnOeCjuOAgea3muWbiueCjuOAgei/keimluOAgeimluelnue2k+eCjuOAgeimluelnue2k+iQjue4ruOAgemdouelnue2k+m6u+eXueOAgeeOu+eSg+mrlOa3t+a/geOAgee+nuaYjuOAgeecvOeevOS4i+WeguOAgem6peeykuiFq+OAgeWkseecoOOAgem8u+WhnuOAgeiCm+mWgOmDqOihk+W+jOeWvOeXm+OAgumhjeelnue2k+eXm2RkAgMPZBYGAgEPDxYCHwgFA0JMM2RkAgIPDxYCHwgFBuecieihnWRkAgMPDxYCHwgFOeecvOeevOeepOWLleOAgeecvOeevOS4i+WeguOAgee1kOiGnOeCjuOAgeS4ieWPieelnue2k+eXm2RkAgQPZBYGAgEPDxYCHwgFA0JMNGRkAgIPDxYCHwgFBuabsuW3rmRkAgMPDxYCHwgFJ+m8u+eC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HwgFBuWDleWPg2RkAgMPDxYCHwgFsQHohabohIrpq5Pohpzngo7jgIHnvo7lsLzniL7nl4fjgIHnsr7npZ7ntpPliIboo4Lnl4fjgIHouJ3pl5znr4Dnl5vvvIznpZ7ntpPmgKfpoK3nl5vvvIznmbLnmYfjgILpoK3nl5vjgIHnnKnmmojjgIHnm67otaTohavnl5vjgIHohbDnl5vku6Xlj4rotrPohp3nhKHlipvvvIzkuI3og73kuYXnq4vnrYnnl4Xnl4dkZAI+D2QWBgIBDw8WAh8IBQRCTDYyZGQCAg8PFgIfCAUG55Sz6ISJZGQCAw8PFgIfCAVC5aSW6Lid55eb77yM5LiL6IKi55e555eb77yM6IWw55eb77yM6aCt55eb77yM55my55mH77yM5bCP5YWS6ama6aKoZGQCPw9kFgYCAQ8PFgIfCAUEQkw2M2RkAgIPDxYCHwgFBumHkemWgGRkAgMPDxYCHwgFVOaApeaAp+iFsOaJreWCt+OAgeiQveaeleOAgeW/g+iCjOeCjuOAgeiDuOiGnOeCju+8jOiFpuiGnOeCju+8jOeZsueZju+8jOiFsOelnue2k+eXm2RkAkAPZBYGAgEPDxYCHwgFBEJMNjRkZAICDw8WAh8IBQbkuqzpqqhkZAIDDw8WAh8IBSvohbDohb/nl5ss6aCt55eb77yM6aC45by377yM55uu55yp77yM55my54uCZGQCQQ9kFgYCAQ8PFgIfCAUEQkw2NWRkAgIPDxYCHwgFBuadn+mqqGRkAgMPDxYCHwgFKumgreeXm++8jOmgheW8t++8jOebruecqe+8jOm8u+ihhO+8jOeZsueLgmRkAkIPZBYGAgEPDxYCHwgFBEJMNjZkZAICDw8WAh8IBQnotrPpgJrosLdkZAIDDw8WAh8IBVrog47kvY3kuI3mraPjgIHmu6/nlKLjgIHog47nm6Tmu6/nlZnjgILnpZ7ntpPmgKfpoK3nl5vvvIzohabmuqLooYDvvIzotrPpl5znr4Dngo7vvIzpm6PnlKJkZAJDD2QWBgIBDw8WAh8IBQRCTDY3ZGQCAg8PFgIfCAUG6Iez6ZmwZGQCAw8PFgIfCAXQAuinkuiGnOeCjuOAgeimlue2suiGnOeCju+8jOWknOebsu+8jOimluelnue2k+eCjuOAgeimluelnue2k+iQjue4ruOAgemdkuWFieecvOOAgeaXqeacn+i8leW6pueZveWFp+manO+8jOinkuiGnOeZveaWkeOAgee/vOeLgOiDrOiCieOAgeeZlOeXh+aAp+W8seimluOAgeimlue2suiGnOWLleiEiOmYu+WhnuOAgeimlue2suiGnOiJsue0oOiuiuaAp+OAgee1kOiGnOeCjuOAgea3muiFuueCjuOAgea3muWbiueCjuOAgeaymeecvOOAgembu+WFieaAp+ecvOeCjuOAgeaWnOimluOAgemdouelnue2k+m6u+eXueOAgeecvOi8quWMneiCjOeXmeaUo++8jOW/g+WLlemBjumAn++8jOi/keimluecvGRkZIHsMx1jKTf8+rsv2PUdzLVZGvZpClJRu2+3ZynouvLa"
common_eventalidation = "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"

result = {}


def get_cookie(form_data):
    url = data["十四經絡"]["url"]
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    session = requests.session()
    cookies = session.post(url=url, data = form_data ,headers=headers).cookies
    cookies = requests.utils.dict_from_cookiejar(cookies)
    print(cookies)
    return cookies

def GetAllAcu(options):
    
    for option in options:
        print(option.text)
        print()

        form_data = {
            '__VIEWSTATE': data["十四經絡"]["__VIEWSTATE"],
            '__VIEWSTATEGENERATOR': data["十四經絡"]["__VIEWSTATEGENERATOR"],
            '__EVENTVALIDATION': data["十四經絡"]["__EVENTVALIDATION"],
            'btn_DoSearch':'確定查詢',
            'DropDownList1_1':option.text
        }

        # print(form_data)
        
        Response = requests.post(data["十四經絡"]["url"], data = form_data, headers=Headers)

        # print(Response.text)

        root = bs4.BeautifulSoup(Response.text,"html.parser")

        table = root.find("table")

        if not table: # 有些一點資料都沒有
            continue
        
        trs = table.find_all("tr")[1:] # 把主治去掉

        print(f"穴道個數 : {len(trs)}\n")

        
        for tr, number in zip(trs, range(2, len(trs) + 2)): # 處理不同穴位
            print("第",number,"個穴位")
            if number < 10:
                choice = "grd_PickSearch$ctl0" + str(number) + "$ctl00"
            else:
                choice = "grd_PickSearch$ctl" + str(number) + "$ctl00"

            form_datas = {
                '__VIEWSTATE': common_viewstate,
                '__VIEWSTATEGENERATOR': data["十四經絡"]["__VIEWSTATEGENERATOR"],
                '__EVENTVALIDATION': common_eventalidation,
                'DropDownList1_1':option.text,
                choice : "選取"
            }

            Response = requests.post(data["十四經絡"]["url"], data = form_datas, headers=Headers)
            
            root = bs4.BeautifulSoup(Response.text,"html.parser")
            tables = root.find_all("table")
            print("table數量: ",len(tables))
            if len(tables) == 1:
                # print(Response.text)
                continue
            print(tables[0].find_all("td")[1].text)
            print(tables[1].find_all("td")[1].text) # 穴道名稱 0、1
            print(tables[2].find_all("td")[1].text) # 經絡名稱 0、1
            print()
            # print(tables[18].find_all("td")[0].text) # 臨床應用與配伍


            symptom_text = tr.find_all("td")[3].text # 症狀名稱
            # print(symptom_text)
            symptoms = re.split(r'[，、()。\s]\s*', symptom_text) # 切割字串得到症狀
            # print(symptoms)

            acu_info = tables[0].find_all("td") # 穴道代碼 0、1
            acu_title_code = acu_info[0].text
            acu_code = acu_info[1].text

            acu_name = tables[1].find_all("td")[1].text # 穴道名稱

            meridian_info = tables[2].find_all("td") # 經絡名稱 0、1
            meridian_title = meridian_info[0].text
            meridian_name = meridian_info[1].text

            matching_acu_info = tables[18].find_all("td") # 臨床應用與配伍
            matching_acu_name = matching_acu_info[0].text
            matching_acu_text = ""
            for info in matching_acu_info[1:]:
                matching_acu_text += info.text

            result[acu_name] = {
                acu_title_code : acu_code,
                meridian_title : meridian_name,
                "主治" : symptoms,
                matching_acu_name : matching_acu_text
            }

            # print(result)
            # break
        
        
        print("\n-------------------\n")
        # break
    
    print(f"十四經絡, 總共的穴位數量: {len(result.keys())}")

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False)




if __name__ == '__main__':
    session = requests.session()
    
    Response = requests.get(url=data["十四經絡"]["url"], headers=Headers)

    root = bs4.BeautifulSoup(Response.text,"html.parser")

    options = root.find("select").find_all("option")[7:]

    GetAllAcu(options)





