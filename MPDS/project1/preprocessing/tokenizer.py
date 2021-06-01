import MeCab
from janome.tokenizer import Tokenizer


def tokenizer_janome(text):
    return [tok for tok in j_t.tokenize(text, wakati=True)]


def tokenizer_mecab(text):
    text = m_t.parse(text)  # これでスペースで単語が区切られる
    ret = text.strip().split()  # スペース部分で区切ったリストに変換
    return ret


if __name__ == "__main__":
    j_t = Tokenizer()
    text = '勉強したことが大事です。'
    print(j_t.tokenize(text, wakati=True))
    # m_t = MeCab.Tagger('-Owakati -d /usr/lib/mecab/dic/mecab-ipadic-neologd')