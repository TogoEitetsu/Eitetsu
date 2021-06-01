import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


if __name__ == "__main__":
    DATA_PATH = '/Users/togoeitetsu/Documents/k-lab/eitetsu/MPDS/project1/data/Kyutech_Corpus_ver2.0/Conversation/long_utterance_unit/all_data.csv'
    df = pd.read_csv(DATA_PATH)
    colnames = list(df.columns)
    data = df.values # numpyに

    np_train, np_test = train_test_split(data, train_size=0.6, random_state=21)
    print(np_train.shape)
    print(np_test.shape)