import re
import json
import pandas as pd
from fastapi import FastAPI, Body
import MeCab

app = FastAPI()
mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

@app.get("/")
async def hello():
    return {"text": "hello world!"}

@app.post("/post")
async def chat(body=Body(...)):
    morphs = sentence_to_morphs(mecab, body["text"])
    morph_df = pd.DataFrame(morphs)
    url = ''
    for row in morph_df['surface']:
        if '人間科学部' in row:
            url = 'https://www.waseda.jp/fhum/hum/about/'
        elif '受験' in row:
            url = 'https://www.waseda.jp/fhum/hum/applicants/'
        elif 'キャンパス' in row:
            url = 'https://www.waseda.jp/fhum/hum/campus-life/'
        elif '施設' in row:
            url = 'https://www.waseda.jp/fhum/hum/facility/'
        elif '問合' in row:
            url = 'https://www.waseda.jp/fhum/hum/contact/'
        elif 'ゼミ' in row:
            url = 'http://www.f.waseda.jp/kikuchi/'
    return {"body": 'こちらのurlを参照してください→{}'.format(url)}

def sentence_to_morphs(parser, sentence, delimiters='[\t,]'):
    morphs = []
    sentence = parser.parse(sentence).split("\n")
    for s in sentence:
        if s == "EOS" or s == "":
            continue
        s = re.split(delimiters, s)
        if len(s) != 10:
            # maybe neologd only return 8? (no read, pronouce)
            # or error?
            s = s + ["*"] * (10-len(s))
        info = {
            "surface": s[0],
            "pos": s[1],  # part-of-speech
            "pos1": s[2],
            "pos2": s[3],
            "pos3": s[4],
            "type": s[5], # practical type?
            "form": s[6],
            "base": s[7],
            "read": s[8],
            "pronounce": s[9],
        }
        morphs.append(info)
    return morphs

def defalt(url):
    if url is not '':  
        print('以下↓のurlを参照してください。')
        print(url)