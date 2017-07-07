# -*- encoding:utf-8 -*-

import konlpy
import nltk

# def pos_conv(value):
#     res = []
#     for i

def Extract_keyword(content):
    twitter = konlpy.tag.Twitter()
    return twitter.morphs(content)

def comp_bleu(a, b):
    return nltk.translate.bleu_score.sentence_bleu(a, b, weights = (0.25, 0.15, 0.1, 0.1))
