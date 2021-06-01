import sys
sys.path.append('..')
from common.utils import csv2list, tokenizer_mecab, calu_max_length

import re
import numpy as np
import pandas as pd

import torchtext
from torchtext.vocab import Vectors



def preprocessing_text(text):
    # 何を削除するかのリスト
    delete_words = ['\r', '\n', '　', ' ', '', '/L', '/R', '/', 'L', 'R', 'F', '\(', '\)', '？', '\+']
    for delete_word in delete_words:
        text = re.sub(delete_word, '', text)

    # 数字文字の一律「0」化
    text = re.sub(r'[0-9 ０-９]', '0', text)  # 数字
    return text


def tokenizer_with_preprocessing(text):
    text = preprocessing_text(text) # 前処理の正規化
    ret = tokenizer_mecab(text)
    return ret


def save_word2vec():
    from gensim.models import KeyedVectors

    # 一度gensimライブラリで読み込んで、word2vecのformatで保存する
    model = KeyedVectors.load_word2vec_format(
        '../data/entity_vector/entity_vector.model.bin', binary=True)
    # 保存（時間がかかります、10分弱）
    model.save_word2vec_format('../data/japanese_word2vec_vectors.vec')

if __name__ == "__main__":
    DATA_PATH = '/Users/togoeitetsu/Documents/k-lab/eitetsu/MPDS/project1/data/Kyutech_Corpus_ver2.0/Conversation/long_utterance_unit/'
    ALLDATA_PATH = DATA_PATH + 'all_data.csv'
    lst = csv2list(ALLDATA_PATH)
    
    x = []
    y = []
    for row in lst:
        x.append(row[5])
        y.append(row[4])
    
    x = np.array(x)
    y = np.array(y)
    
    max_length = 50
    # max_length = calu_max_length(lst)

    '''

    TEXT = torchtext.data.Field(sequential=True, tokenize=tokenizer_with_preprocessing,
                                use_vocab=True, lower=True, include_lengths=True, batch_first=True, fix_length=max_length)
    LABEL = torchtext.data.Field(sequential=False, use_vocab=False)
    train_ds, val_ds, test_ds = torchtext.data.TabularDataset.splits(
        path='./data/', train='text_train.tsv',
        validation='text_val.tsv', test='text_test.tsv', format='tsv',
        fields=[('Text', TEXT), ('Label', LABEL)])
    '''

    ##### word2vec
    # gensimライブラリで読み込んで、word2vecのformatで保存する
    # save_word2vec()

    japanese_word2vec_vectors = Vectors(name='../data/japanese_word2vec_vectors.vec')

    # 単語ベクトルの中身を確認します
    print("1単語を表現する次元数：", japanese_word2vec_vectors.dim)
    print("単語数：", len(japanese_word2vec_vectors.itos))
    print(japanese_word2vec_vectors['日本'])


    ##### fastText
    '''
    japanese_fasttext_vectors = Vectors(name='../data/vector_neologd/model.vec')
    print("1単語を表現する次元数：", japanese_fasttext_vectors.dim)
    print("単語数：", len(japanese_fasttext_vectors.itos))
    '''