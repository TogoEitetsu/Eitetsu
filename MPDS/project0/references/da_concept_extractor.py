import MeCab
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill
import sklearn_crfsuite
from crf_util import word2features, sent2features, sent2labels
import re

# 発話文から対話行為タイプとコンセプトを抽出するクラス
class DA_Concept:

    def __init__(self):
        # MeCabの初期化
        self.mecab = MeCab.Tagger()
        self.mecab.parse('')

        # SVMモデルの読み込み
        with open("svc.model","rb") as f:
            self.vectorizer = dill.load(f)
            self.label_encoder = dill.load(f)
            self.svc = dill.load(f)

        # CRFモデルの読み込み
        with open("crf.model","rb") as f:
            self.crf = dill.load(f)

    # 発話文から対話行為タイプをコンセプトを抽出
    def process(self,utt):
        lis = []
        for line in self.mecab.parse(utt).splitlines():
            if line == "EOS":
                break
            else:
                word, feature_str = line.split("\t")
                features = feature_str.split(',')
                postag = features[0]
                lis.append([word, postag, "O"])
        # print(lis) [['今日', '名詞', 'O'], ['の', '助詞', 'O'], ['天気', '名詞', 'O']]

        words = [x[0] for x in lis]
        print(words)
        tokens_str = " ".join(words)
        # print(tokens_str) 今日 の 天気

        ################################################## ここからの作業が正直わからん
        X = self.vectorizer.transform([tokens_str])
        '''
        print(X)
        (0, 340)	0.3406053626816097
        (0, 199)	0.5841572425319899
        (0, 188)	0.4334973928340906
        (0, 181)	0.3467954033921295
        (0, 55)	0.39583668305534153
        (0, 31)	0.27906017603705585
        '''
        Y = self.svc.predict(X)
        '''
        print(Y)
        [2]
        '''
        # 数値を対応するラベルに戻す
        da = self.label_encoder.inverse_transform(Y)[0]
        # print(da) request-weather
        
        X = [sent2features(s) for s in [lis]]
        '''
        print(X)
        [
            [
                {'bias': 1.0, 'word': '今日', 'postag': '名詞', 'BOS': True, '+1:word': 'の', '+1:postag': '助詞'}, 
                {'bias': 1.0, 'word': 'の', 'postag': '助詞', '-1:word': '今日', '-1:postag': '名詞', '+1:word': '天気', '+1:postag': '名詞'}, 
                {'bias': 1.0, 'word': '天気', 'postag': '名詞', '-1:word': 'の', '-1:postag': '助詞', 'EOS': True}
            ]
        ]
        '''
        ################################################## ここからの作業が正直わからん
        
        # 各単語に対応するラベル列
        labels = self.crf.predict(X)[0]
        '''
        print(labels)
        ['B-date', 'O', 'B-type']
        '''

        # 単語列とラベル系列の対応を取って辞書に変換
        conceptdic = {}
        buf = ""
        last_label = ""
        for word, label in zip(words, labels): # words=['今日', 'の', '天気'], labels=['B-date', 'O', 'B-type']
            if re.search(r'^B-', label):
                if buf != "":
                    _label = last_label.replace('B-', '').replace('I-', '')
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
        
        return da, conceptdic

if __name__ ==  '__main__':
    da_concept = DA_Concept()
    da, conceptdic = da_concept.process("東京の天気は？")
    print(da, conceptdic)