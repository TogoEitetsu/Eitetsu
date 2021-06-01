import MeCab
import re
import random
import json
import xml.etree.ElementTree

# 遊び場のリスト
places = ['第1公園', '第2公園', '第3公園', '第4公園', '第5公園', '第6公園', '第7公園', '第8公園', '第9公園',
         '第10公園', '第一公園', '第二公園', '第三公園', '第四公園', '第五公園', '第六公園', '第七公園', '第八公園', '第九公園',
         '第十公園', '保育園', '校庭']

# 日付のリスト
dates = ["今日", "明日", "明後日", "明明後日"]
'''
for m in range(1, 13):
    for d in range(1, 32):
        date = "{}.{}".format(m, d)
        dates.append(date)
        date = "{}/{}".format(m, d)
        dates.append(date)
        date = "{}月{}日".format(m, d)
        dates.append(date)
'''

# 種目のリスト
types = ["鬼ごっこ", "かくれんぼ", "ボール遊び", "サッカー", "キックベース", "ドッチボール", "縄跳び", "缶蹴り"]

# サンプル文に含まれる単語を置き換えることで学習用事例を作成
def random_generate(root):
    buf = ""
    pos = 0
    posdic = {}
    # タグがない文章の場合は置き換えしないでそのまま返す
    if len(root) == 0:
        return root.text, posdic
    # タグで囲まれた箇所を同じ種類の単語で置き換える
    for elem in root:
        if elem.tag == "place":
            place = random.choice(places)
            buf += place
            posdic["place"] = (pos, pos+len(place))
            pos += len(place)
        elif elem.tag == "date":
            date = random.choice(dates)
            buf += date
            posdic["date"] = (pos, pos+len(date))
            pos += len(date)
        elif elem.tag == "type":
            _type =  random.choice(types)
            buf += _type
            posdic["type"] = (pos, pos+len(_type))
            pos += len(_type)
        if elem.tail is not None:
            buf += elem.tail
            pos += len(elem.tail)
    return buf, posdic

# 現在の文字位置に対応するタグをposdicから取得
def get_label(pos, posdic):
    for label, (start, end) in posdic.items():
        if start <= pos and pos < end:
            return label
    return "O"

# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')

# 学習用ファイルの書き出し先 
fp = open("concept_samples.dat","w")

da = ''
# eamples.txt ファイルの読み込み
for line in open("examples_excursion.txt","r"):
    line = line.rstrip()
    # da= から始まる行から対話行為タイプを取得
    if re.search(r'^da=',line):
        da = line.replace('da=','')
    # 空行は無視
    elif line == "":
        pass
    else:
        # タグの部分を取得するため，周囲にダミーのタグをつけて解析
        root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
        # 各サンプル文を1000倍に増やす
        for i in range(1000):
            sample, posdic = random_generate(root)

            # lis は[単語，品詞，ラベル]のリスト
            lis = []
            pos = 0
            prev_label = ""
            for line in mecab.parse(sample).splitlines():
                if line == "EOS":
                    break
                else:
                    word, feature_str = line.split("\t")
                    features = feature_str.split(',')
                    # 形態素情報の0番目が品詞
                    postag = features[0]
                    # 現在の文字位置に対応するタグを取得
                    label = get_label(pos, posdic)
                    # label がOでなく，直前のラベルと同じであればラベルに'I-'をつける
                    if label == "O":
                        lis.append([word, postag, "O"])
                    elif label == prev_label:
                        lis.append([word, postag, "I-" + label])
                    else:
                        lis.append([word, postag, "B-" + label])
                    pos += len(word)
                    prev_label = label
            
            # 単語，品詞，ラベルを学習用ファイルに書き出す
            for word, postag, label in lis:
                fp.write(word + "\t" + postag + "\t" + label + "\n")
            fp.write("\n")

fp.close()