import urllib.request
import json
import scripts
import pickle
from datetime import date

hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
url = "https://www3.nhk.or.jp/news/easy/news-list.json"
req = urllib.request.Request(url, headers=hdr)
response = urllib.request.urlopen(req)
news_list = json.loads(response.read())
date_today = date.today()
try:
    last_check = pickle.load(open('last_check.p','rb'))
    if type(last_check)==list:
        date_check=last_check[0]
        nb_downloaded=last_check[1]
    else:
        date_check=last_check
        nb_downloaded=0
except:
    date_check = date(1,1,1)
    nb_downloaded=0
try:
    current_file = open("yomichan/term_bank_1.json", 'r', encoding='utf8')
    yomi_json = json.loads(current_file.read())
except:
    yomi_json=list()
initial_count = len(yomi_json)
print("Initial number of entries in the dictionary: "+str(initial_count)+'\n')

counter_today=nb_downloaded*(date_check==date_today)
last_count = initial_count
for items in news_list[0]:
    year = int(items[0:4])
    month = int(items[5:7])
    day = int(items[8:10])
    article_date = date(year,month,day)
    if article_date>=date_check:
        for i in reversed(range(len(news_list[0][items]))):
            if len(news_list[0][items])-i>nb_downloaded or article_date>date_check:
                news_id = news_list[0][items][i]['news_id']
                print(items)
                print("easy news "+news_id)
                url = "https://www3.nhk.or.jp/news/easy/"+news_id+"/"+news_id+".out.dic"
                req = urllib.request.Request(url, headers=hdr)
                response = urllib.request.urlopen(req)
                print("dictionary downloaded")
                dic_str = response.read().decode('utf-8')
                dic_str = scripts.clean_ruby2(dic_str)
                print("ruby cleaned")
                dic_json = scripts.json.loads(dic_str)
                dic_json = scripts.add_readings(dic_json)
                print("added readings")
                yomi_json = scripts.to_yomichan(dic_json,yomi_json)
                print("updated dictionnary")
                counter_dl = len(yomi_json)-last_count
                last_count = len(yomi_json)
                print(str(counter_dl)+" words added\n")
                if article_date==date.today():
                    counter_today=counter_today+1
        
added = last_count-initial_count
print(str(added)+" words added in this session")
yomi_json = sorted(yomi_json, key=scripts.gojuon_entry)
for i in range(len(yomi_json)):
    yomi_json[i][4] = 0
    yomi_json[i][-2] = i
output_json = json.dumps(yomi_json, ensure_ascii=False)
yomi_file = open("yomichan/term_bank_1.json", 'w', encoding='utf8')
yomi_file.write(output_json)
yomi_file.close()
last_check = [date_today, counter_today]
filehandler = open('last_check.p','wb')
pickle.dump(last_check,filehandler)
filehandler.close()
