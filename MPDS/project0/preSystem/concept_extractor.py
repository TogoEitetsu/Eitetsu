import re
import dill
import json
import MeCab
import sklearn_crfsuite
from crf_util import word2features, sent2features, sent2labels

# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')

# CRFモデルの読み込み
with open("crf.model","rb") as f:
    crf = dill.load(f)
    
# 発話文からコンセプトを抽出
def extract_concept(utt):
    lis = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            features = feature_str.split(',')
            postag = features[0]
            lis.append([word, postag, "O"])

    words = [x[0] for x in lis]            
    X = [sent2features(s) for s in [lis]]
    
    # 各単語に対応するラベル列
    labels = crf.predict(X)[0]
    '''
    X = {
        {'bias': 1.0, 'word': '大阪', 'postag': '名詞', 'BOS': True, '+1:word': 'の', '+1:postag': '助詞'},
        {'bias': 1.0, 'word': 'の', 'postag': '助詞', '-1:word': '大阪', '-1:postag': '名詞', '+1:word': '明日', '+1:postag': '名詞'},
        {'bias': 1.0, 'word': '明日', 'postag': '名詞', '-1:word': 'の', '-1:postag': '助詞', '+1:word': 'の', '+1:postag': '助詞'},
        {'bias': 1.0, 'word': 'の', 'postag': '助詞', '-1:word': '明日', '-1:postag': '名詞', '+1:word': '天気', '+1:postag': '名詞'},
        {'bias': 1.0, 'word': '天気', 'postag': '名詞', '-1:word': 'の', '-1:postag': '助詞', 'EOS': True}
    }
    words = ['大阪', 'の', '明日', 'の', '天気']
    labels = ['B-place', 'O', 'B-date', 'O', 'B-type']
    '''

    
    # 単語列とラベル系列の対応を取って辞書に変換
    conceptdic = {}
    buf = ""
    last_label = ""
    for word, label in zip(words, labels): # word='明日', label='B-date'
        if re.search(r'^B-',label):
            if buf != "":
                _label = last_label.replace('B-','').replace('I-','')
                conceptdic[_label] = buf            
            buf = word
        elif re.search(r'^I-',label):
            buf += word
        elif label == "O":
            if buf != "":
                _label = last_label.replace('B-','').replace('I-','')
                conceptdic[_label] = buf
                buf = ""
        last_label = label
    if buf != "":
        _label = last_label.replace('B-','').replace('I-','')
        conceptdic[_label] = buf
        
    return conceptdic

if __name__ ==  '__main__':
    for utt in ["明日の遠足", "もう一度はじめから", "明日は鬼ごっこをしましょう"]:    
        conceptdic = extract_concept(utt)
        print(utt, conceptdic)