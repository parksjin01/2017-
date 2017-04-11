# -*- encoding:utf-8 -*-
# !/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from gensim.models import Word2Vec
import pprint

def make_corpus(txt):
    corpus = []
    for i in txt:
        corpus.append([i])
    return corpus

# with open('parsed_data.txt', 'r') as f:
#     corpus = make_corpus(map(unicode, f.read().split('\n')))
# print corpus[:20]
#
# create_corpus = corpus[:len(corpus)/2]
# print u'즐겁' in corpus
# train_corpus = corpus[len(corpus)/2:]

# model = Word2Vec(size=128, window=5, min_count=5, workers=4)
# model.build_vocab(corpus,keep_raw_vocab=False)
# model.train(corpus)
# model.save('w2v')
model = Word2Vec.load('w2v')
pprint.pprint(model.most_similar(u'너'))
tmp = model.most_similar(u'12',topn=100)
# a = model.vocab.keys()
# for i in a[:20]:
#     print i
for i in tmp:
    print i[0], i[1]