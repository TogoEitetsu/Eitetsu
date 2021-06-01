import csv
import math
import MeCab
import numpy as np
import pandas as pd


def make_padding_mask(ids_tensor, pad_id, device=None):
    mask = torch.where(
        ids_tensor==pad_id,
        torch.ones_like(ids_tensor, device=device),
        torch.zeros_like(ids_tensor, device=device)
    ).type(torch.bool)
    return mask


def make_future_mask(ids_tensor, device=None):
    batch, length = ids_tensor.shape
    arange = torch.arange(length, device=device)
    mask = torch.where(
        arange[None, :] <= arange[:, None],
        torch.zeros((length, length), device=device),
        torch.ones((length, length), device=device)*(-np.inf)
    ).type(torch.float32)
    return mask


def wakachi_tokenize(text_list, tokenizer):
    tokenized_texts = []
    for text in text_list:
        result = [m.surface() for m in tokenizer.tokenize(text, mode)]
        tokenized_texts.append(result)
        
    return tokenized_texts


def csv2list(path, header_delete=True):
    lst = []
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            lst.append(row)
    if header_delete:
        lst.pop(0)
    return lst


def text2words(text):
    tokenized_text = []
    words = m.parse(text).split('\n')
    
    idx = 0
    while True:
        word = words[idx]
        word = word.split('\t')
        suf = word[0]
        if suf == 'EOS':
            break
        others = word[1].split(',')
        pos = others[0]
        tokenized_text.append([suf, pos])
        idx += 1
    return tokenized_text


def tokenizer_mecab(text):
    import MeCab
    m_t = MeCab.Tagger()

    result = []
    node = m_t.parseToNode(text)  # これでスペースで単語が区切られる
    while node:
        result.append(node.surface)
        node = node.next
    return result[1:-1]

def calu_max_length(lst, colidx=5):
    max_length = 0
    for row in lst:
        if len(row[5]) > max_length:
            max_length = len(row[5])
    return max_length


if __name__ == "__main__":
    path = '/Users/togoeitetsu/Documents/k-lab/eitetsu/MPDS/project1/data/Kyutech_Corpus_ver2.0/Conversation/long_utterance_unit/all_data.csv'
    test = '/Users/togoeitetsu/Documents/k-lab/eitetsu/MPDS/project1/data/Kyutech_Corpus_ver2.0/Conversation/long_utterance_unit/20150313_C1.csv'
    colnames = ['#ID', 'start', 'end', 'da', 'utterance']

    text = '勉強したことが大事です。'
    m = MeCab.Tagger()
    print(m.parse(text))