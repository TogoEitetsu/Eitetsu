import os
import random
import numpy as np
import pandas as pd

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from flair.datasets import ColumnCorpus
from flair.embeddings import StackedEmbeddings, FlairEmbeddings
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer


DATA_DIR = '/Users/togoeitetsu/Documents/k-lab/MPDS/project1/data'


SEED = 21
def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        
seed_everything(SEED)


columns = {0: 'text', 1: 'ner'}
data_folder = '.'
corpus = ColumnCorpus(data_folder, columns,
                      train_file = DATA_DIR + 'ja.wikipedia.conll')


tag_type = 'ner'
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

print(tag_dictionary.idx2item)


embedding_types = [
    FlairEmbeddings('ja-forward'),
    FlairEmbeddings('ja-backward'),
]

embeddings = StackedEmbeddings(embeddings=embedding_types)


tagger = SequenceTagger(hidden_size=256,
                        embeddings=embeddings,
                        tag_dictionary=tag_dictionary,
                        tag_type=tag_type,
                        use_crf=True)

trainer = ModelTrainer(tagger, corpus)
trainer.train('resources/taggers/example-ner',
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs=150)


model = SequenceTagger.load('resources/taggers/example-ner/final-model.pt')

sentence = Sentence('私 は 田中 と 東京 駅 へ 行っ た')
model.predict(sentence)

print(sentence.to_tagged_string())