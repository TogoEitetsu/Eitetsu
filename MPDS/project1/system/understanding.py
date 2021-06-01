import MeCab
import numpy as np

DATA_DIR = '../data/'
CKPT_DIR = '../checkpoints/'
keymodel = CKPT_DIR + 'resources/taggers/example-ner/final-model.pt'

class Understander:
    '''
    発話理解部
    '''
    def __init__(self):
        self.act_estimation = ActEstimator()
        self.keyword_extractor = KeywordExtractor()



class DaEstimator:
    '''
    発話行為推定
    '''
    def __init__(self):
        self.tokenizer = MeCab.Tagger()
    
    def predict(self):
        pass


class WordExtractor:
    '''
    キーワード抽出
    '''
    def __init__(self):
        pass

    def extract(self):
        pass

if __name__ == "__main__":
    m = MeCab.Tagger()
    print(m.parse("コーヒー牛乳とラーメン"))