import json
import pykakasi
import re

def clean_ruby2(dic_str):
    dic_str=dic_str.replace('<ruby><rb>',"")
    dic_str=re.sub("</rb><rt>.*?</rt></ruby>","",dic_str)
    dic_str=re.sub("<span class=.*?</span>","",dic_str)
    return(dic_str)

def add_readings(dic_json):
    for x in dic_json["reikai"]["entries"]:
        kks = pykakasi.kakasi()
        for i in range(len(dic_json["reikai"]["entries"][x])):
            hyouki = str()
            for char in dic_json["reikai"]["entries"][x][i]["hyouki"]:
                if char!='[' and char!=']' and char!='"':
                    hyouki = hyouki + char
            result = kks.convert(hyouki)
            katakana, hiragana, romaji = '', '', ''
            for item in result:
                katakana += item['kana']
                hiragana += item['hira']
                romaji += item['hepburn']
            if hyouki == katakana or hyouki == hiragana:
                kana = ''
            else: kana = hiragana
            dic_json["reikai"]["entries"][x][i]["hyouki"] = hyouki
            dic_json["reikai"]["entries"][x][i]["hiragana"] = kana
            dic_json["reikai"]["entries"][x][i]["romaji"] = romaji
    return dic_json

def to_yomichan(dic_json,yomi_json):
    for x in dic_json["reikai"]["entries"]:
        hyouki=dic_json["reikai"]["entries"][x][0]["hyouki"]
        k=0
        doublon=False
        while k<len(yomi_json) and doublon==False:
            if hyouki==yomi_json[k][0]:
                doublon=True
            k=k+1
        if doublon==False:
            kana=dic_json["reikai"]["entries"][x][0]["hiragana"]
            yomi_json.append(list())
            defi=list()
            for i in range(len(dic_json["reikai"]["entries"][x])):
                defi.append(dic_json["reikai"]["entries"][x][i]["def"])
            yomi_json[-1].append(hyouki)
            yomi_json[-1].append(kana)
            yomi_json[-1].append("")
            yomi_json[-1].append("")
            yomi_json[-1].append(0)
            yomi_json[-1].append(defi)
            yomi_json[-1].append("")
            yomi_json[-1].append("")
    return yomi_json

def gojuon_entry(entry):
    kks = pykakasi.kakasi()
    result = kks.convert(entry[0])
    hiragana = ''
    for item in result:
        hiragana += item['hira']
    return hiragana