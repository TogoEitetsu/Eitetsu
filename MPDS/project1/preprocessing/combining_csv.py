import glob
import numpy as np
import pandas as pd

if __name__ == "__main__":
    data_dir = '/Users/togoeitetsu/Documents/k-lab/eitetsu/MPDS/project1/data/Kyutech_Corpus_ver2.0/Conversation/long_utterance_unit'
    endpoints = glob.glob(data_dir + '/*')

    data = pd.read_csv(endpoints[0])
    for i in range(1, len(endpoints)):
        endpoint = endpoints[i]
        add = pd.read_csv(endpoint)
        data = pd.merge(data, add, how='outer')
    
    data.to_csv('/Users/togoeitetsu/Documents/k-lab/eitetsu/MPDS/project1/data/Kyutech_Corpus_ver2.0/Conversation/long_utterance_unit/all_data.csv')