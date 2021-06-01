# 単語情報から素性を作成
def word2features(sent, i):
    word = sent[i][0] # word = '気温'
    postag = sent[i][1] # postag = '名詞'
    features = {
        'bias': 1.0,
        'word': word,
        'postag': postag
    }
    if i > 0: # 0じゃなかったら
        word_left = sent[i-1][0]
        postag_left = sent[i-1][1]
        features.update({
            '-1:word': word_left,
            '-1:postag': postag_left
        })
        # dic.update で前の辞書に追加するイメージ
    else:
        features['BOS'] = True

    if i < len(sent)-1: # 一番最後じゃなかったら
        word_right = sent[i+1][0]
        postag_right = sent[i+1][1]
        features.update({
            '+1:word': word_right,
            '+1:postag': postag_right
        })
    else:
        features['EOS'] = True
    return features # n番目は {'-1:word': 'は', '-1:word': '助詞', 'bias': 1.0, 'word': 'あり', 'postag': 'o', '+1:word': 'ませ', '+1:postag': '助動詞'}

# 単語情報を素性に変換
def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]
    # ex) sent = [['気温', '名詞', 'B-type'], ['で', '助詞', 'O'], ['は', '助詞', 'O'], ['あり', '動詞', 'O'], ['ませ', '助動詞', 'O'], ['ん', '助動詞', 'O']]

# 文情報をラベルに変換
def sent2labels(sent):
    return [label for word, postag, label in sent]