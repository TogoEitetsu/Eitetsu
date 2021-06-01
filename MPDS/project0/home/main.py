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

class User():
    def __init__(self, n):
        self.name = n
        self.frame = {"place": "", "date": "", "type": ""}
    
    def update_frame(self, da, conceptdic, pre_conceptdic):
        '''
        スロットの更新

        da: str
        conceptdic: dic
        pre_conceptdic: dic
        '''
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
            pass
        elif da == "disagree":
            pass
        elif da == "initialize":
            self.frame = {"place": "", "date": "", "type": ""}
        elif da == "correct-info":
            for k, v in conceptdic.items():
                if self.frame[k] == v:
                    self.frame[k] = ""

class Facilitator():
    def __init__(self, users):
        self.users = users # user をリストでまとめる
        self.dialogues = [] # dialogues[n]: {"user": "A", "da": "advocate", {"place": "第一公園", "date": "", "type": ""}}
        self.users_frame = {}

        # 各話者の frame の初期設定
        self.frame = {"place": "", "date": "", "type": ""}
        for user in self.users:
            self.users_frame[user] = {"place": "", "date": "", "type": ""}
        
        # システムの発話辞書
        self.uttdic = {
            "open-prompt": "まだ内容が一個も決まってないよ！",
            "confirm": "内容の確認",
            "consensus": "意見が食い違った場合"
            }
    
    def update_dialogues(self, user, da, conceptdic, updated_frame):
        ''' 
        対話内容の更新

        user: str
        da: str
        conceptdic: dic
        updated_frame: dic
        '''
        dialogue = {"user": user, "da": da, "conceptdic": conceptdic}
        self.dialogues.append(dialogue)

        # frame の更新
        if user in self.users:
            self.users_frame[user] = updated_frame
        else:
            print("知らない人が混じっています")        
    
    def next_system_da(self):
        '''
        システムの行動制御部
        '''
        pass

    def time_manager(self):
        '''
        時間管理
        '''
        pass


if __name__ == '__main__':
    # 対話行為タイプとコンセプトの推定器
    da_concept = DA_Concept()

    users = ["A", "B"]
    participants = {}
    for user in users:
        participants[user] = User(user)

    sys = Facilitator(users)

    # システムプロンプト
    print("SYS> こちらはファシリテーションシステムです")
    print("SYS> 話し合いを始めましょう")
    print("SYS> 話し合うのは遠足の日程・場所・遊ぶ内容の3点です")

    # ユーザ入力の処理
    i = 0
    while True:
        text = input("> ")
        '''
        入力として以下のような形式での入力を想定
        "A 私は第一公園が良いと思います"
        '''
        print(text)
        
        uname = text.split()[0]
        utt = text.split()[1]

        # 手入力で対話行為タイプとコンセプトを入力していた箇所を
        # 自動推定するように変更
        da, conceptdic = da_concept.process(utt)        
        print(da, conceptdic)

        # システムとユーザ情報の更新        
        if uname not in users:
            print("知らない人が混じっています")
        else:
            # 対話行為タイプとコンセプトを用いてフレームを更新
            if i == 0:
                participants[uname].update_frame(da, conceptdic, "") 
                sys.update_dialogues(uname, da, conceptdic, participants[uname].frame) # user, da, conceptdic, updated_frame
            else:
                # 一つ前の対話情報を取得
                pre_uname = sys.dialogues[-2]["user"]
                pre_da = sys.dialogues[-2]["da"]
                pre_conceptdic = sys.dialogues[-2]["conceptdic"]

                # システムの更新
                participants[uname].update_frame(da, conceptdic, pre_conceptdic) 
                sys.update_dialogues(uname, da, conceptdic, participants[uname].frame) 
        
        # システムの行動
        sys.update_dialogues(uname, da, conceptdic, participants[uname].frame)

        for user in users:
            print(user, participants[user].frame)
        if i == 2:
            break
        else:
            i += 1
        '''

        # フレームからシステム対話行為を得る   
        sys_da = Facilitator.next_system_da()

        # 遷移先がtell_infoの場合は情報を伝えて終了
        if sys_da == "tell-info":
            print("天気をお伝えします")
            break
        else:
            # 対話行為に紐づいたテンプレートを用いてシステム発話を生成
            sysutt = uttdic[sys_da]
            print("SYS>", sysutt) 
        '''   

    # 終了発話
    print("ご利用ありがとうございました") 