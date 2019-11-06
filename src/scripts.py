import json
from pykakasi import kakasi as kaka
import re

def clean_ruby2(dic_str):
    dic_str=dic_str.replace('<ruby><rb>',"")
    dic_str=re.sub("</rb><rt>.*?</rt></ruby>","",dic_str)
    dic_str=re.sub("<span class=.*?</span>","",dic_str)
    return(dic_str)

def add_readings(dic_json):
    for x in dic_json["reikai"]["entries"]:
        for i in range(len(dic_json["reikai"]["entries"][x])):
            kakasi = kaka()
            hyouki=str()
            for char in dic_json["reikai"]["entries"][x][i]["hyouki"]:
                if char!='[' and char!=']' and char!='"':
                    hyouki=hyouki+char
            kakasi.setMode('J', 'H')  # J(Kanji) to H(Hiragana)
            kakasi.setMode("H", None) # Hiragana default: no conversion
            conv = kakasi.getConverter()
            hiragana = conv.do(hyouki)
            kakasi.setMode('H', 'a')
            conv = kakasi.getConverter()
            romaji = conv.do(hiragana)
            if hiragana==romaji: # katakana
                kakasi.setMode('K', 'H')
                conv = kakasi.getConverter()
                hiragana = ""
                kakasi.setMode('K', 'a')
                conv = kakasi.getConverter()
                romaji = conv.do(hyouki)
            dic_json["reikai"]["entries"][x][i]["hyouki"]=hyouki
            dic_json["reikai"]["entries"][x][i]["hiragana"]=hiragana
            dic_json["reikai"]["entries"][x][i]["romaji"]=romaji
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
            yomi_json[-1].append("")
            yomi_json[-1].append(defi)
            yomi_json[-1].append("")
            yomi_json[-1].append("")
    return yomi_json
