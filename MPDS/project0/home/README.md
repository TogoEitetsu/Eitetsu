# 複数人対話システム
## To Do
- examples_excursion.txt の内容を増やす
    - 「私は〜」
- 意味理解で機械学習を使う
- 基盤化についての学習


## 対話内容


## 手法
```スロットフィリング```

### スロット内容
- 日付 date
    - 今日
    - 明日
    - 明後日
    - 明明後日
- 場所 place
    - 第1公園 ~ 第10公園
    - 校庭
    - 保育園
- 内容 type
    - 鬼ごっこ
    - かくれんぼ
    - ボール遊び
    - サッカー
    - キックベース
    - ドッチボール
    - 縄跳び
    - 缶蹴り

### システムの行動
- consensus
    - 競合した意見を合わせる
- confirm
    - 内容の確認

### ユーザの発話意図　想定
- 主張: advocate
- 賛成: agree
- 反対: disagree

## モデルの更新方法
- svc.model の更新
    1. examples_excursion.txt の内容を書き換える
    2. generate_da_samples.py の実行
    3. train_da_model.py の実行
- crf.model の更新
    1. examples_excursion.txt の内容を書き換える
    2. generate_concept_samples.py の実行
    3. train_concept_model.py の実行

## 参考書籍
書籍「python で作る対話システム」