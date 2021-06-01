from da_concept_extractor import DA_Concept

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

# システムの対話行為とシステム発話を紐づけた辞書
uttdic = {"open-prompt": "ご用件をどうぞ",
          "ask-place": "地名を言ってください",
          "ask-date": "日付を言ってください",
          "ask-type": "情報種別を言ってください"}

class User():
    def __init__(self, n, i):
        self.name = n
        self.id = i
        self.frame = {"place": "", "date": "", "type": ""}
    
    def update_frame(self, da, conceptdic, pre_conceptdic):
        for k, v in conceptdic.items():
            if k == "place" and v not in places:
                conceptdic[k] = ""
            elif k == "date" and v not in dates:
                conceptdic[k] = ""
            elif k == "type" and v not in types:
                conceptdic[k] = ""
        if da == "advocate":
            for k, v in conceptdic.items():
                self.frame[k] = v
        elif da == "agree":
            for k, v in pre_conceptdic.items():
                self.frame[k] = v
        elif da == "oppose":
            pass
        elif da == "initialize":
            self.frame = {"place": "", "date": "", "type": ""}
        elif da == "correct-info":
            for k, v in conceptdic.items():
                if self.frame[k] == v:
                    self.frame[k] = ""

class Facilitator():
    def __init__(self):
        super().__init__()
    
    def next_system_da(self):
        pass

# 発話から得られた情報をもとにフレームを更新
def update_frame(frame, da, conceptdic):
    # 値の整合性を確認し，整合しないものは空文字にする
    for k,v in conceptdic.items():
        if k == "place" and v not in places:
            conceptdic[k] = ""
        elif k == "date" and v not in dates:
            conceptdic[k] = ""
        elif k == "type" and v not in types:
            conceptdic[k] = ""
    if da == "advocate":
        for k,v in conceptdic.items():
            # コンセプトの情報でスロットを埋める
            frame[k] = v
    elif da == "initialize":
        frame = {"place": "", "date": "", "type": ""}
    elif da == "correct-info":
        for k,v in conceptdic.items():
            if frame[k] == v:
                frame[k] = ""
    return frame

# フレームの状態から次のシステム対話行為を決定
def next_system_da(frame):
    # すべてのスロットが空であればオープンな質問を行う
    if frame["place"] == "" and frame["date"] == "" and frame["type"] == "":
        return "open-prompt"
    # 空のスロットがあればその要素を質問する
    elif frame["place"] == "":
        return "ask-place"
    elif frame["date"] == "":
        return "ask-date"
    elif frame["type"] == "":
        return "ask-type"
    else:
        return "tell-info"

if __name__ == '__main__':
    # 対話行為タイプとコンセプトの推定器
    da_concept = DA_Concept()    

    # フレーム
    frame = {"place": "", "date": "", "type": ""}    
    pre_conceptdic = ""

    # システムプロンプト
    print("SYS> こちらはファシリテーションシステムです")
    print("SYS> 話し合いを始めましょう")
    print("SYS> 話し合うのは遠足の日程・場所・遊ぶ内容の3点です")

    # ユーザ入力の処理
    while True:
        text = input("> ")

        # 現在のフレームを表示
        print("frame=", frame)

        # 手入力で対話行為タイプとコンセプトを入力していた箇所を
        # 自動推定するように変更
        da, conceptdic = da_concept.process(text)        
        print(da, conceptdic)

        # 対話行為タイプとコンセプトを用いてフレームを更新
        frame = update_frame(frame, da, conceptdic)

        # 更新後のフレームを表示    
        print("updated frame=", frame)    

        # フレームからシステム対話行為を得る   
        sys_da = next_system_da(frame)

        # 遷移先がtell_infoの場合は情報を伝えて終了
        if sys_da == "tell-info":
            print("天気をお伝えします")
            break
        else:
            # 対話行為に紐づいたテンプレートを用いてシステム発話を生成
            sysutt = uttdic[sys_da]
            print("SYS>", sysutt)    

    # 終了発話
    print("ご利用ありがとうございました") 