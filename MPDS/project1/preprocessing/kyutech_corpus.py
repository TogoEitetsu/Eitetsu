import os
import glob
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class KyutechCorpus:
    def __init__(self, endpoint):
        self.path = endpoint
        self.data = None # dataframe型

    def load_data(self, is_shaffle=False):
        pass
    
    def get_csv(self):
        self.data = pd.read_csv(self.path)
    
    def shuffle(self):
        pass


class Classifier:
    def __init__(self, data):
        self.data = data

if __name__ == "__main__":
    endpoint = '/Users/togoeitetsu/Documents/k-lab/eitetsu/MPDS/project1/data/Kyutech_Corpus_ver2.0/Conversation/long_utterance_unit/all_data.csv'
    corpus = KyutechCorpus(endpoint)
    corpus.get_csv()
    data = corpus.data # データ取得
    data = data.values # pdをnumpy配列に

    # いらないdaの削除
    da_list, counts = np.unique(data[:, 4], return_counts=True)
    use_da_list = [] # 使うdaを収納
    for da, count in zip(da_list, counts):
        if count  > 3: # ここの基準はどうするか検討の余地あり
            use_da_list.append(da)

    use_data = []
    for row in data:
        if row[4] in use_da_list:
            use_data.append(row)
    use_data = np.array(use_data)

    train, test = train_test_split(use_data, test_size=0.2) # 訓練データとテストデータに分割
    x_train, t_train = train[:, 5], train[:, 4]
    x_test, t_test = test[:, 5], test[:, 4]

    print(x_train.shape, t_train.shape)
    print(x_test.shape, t_test.shape)

    delete_words = ['/R', '/L', 'F']