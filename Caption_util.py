# -*- encoding:utf-8 -*-
import nltk
import numpy as np

def parsing(caption):
    res = ''
    switch = False
    for i in caption:
        if switch:
            if i == '>':
                switch=False
        else:
            if i == '<':
                switch=True
            else:
                res += i

    content = res.split('\n\n')
    res = ''
    for sentence in content:
        tmp = sentence.split('\n')[2:]
        for line in tmp:
            if line[0] != '(' and line[0] != '[':
                res += line+'\n`\n'
        res += '\n\n'

    return res

def analyze(caption, perc = 10):
    if perc > 100:
        print '[-]Percentage can\'t above 100%'
    with open(caption, 'r') as f:
        data = f.read()
    caption = parsing(data)
    # res = {'Noun':[], 'Verb':[], 'Adjective':[], 'Determiner':[], 'Adverb':[], 'Conjunction':[], 'Exclamation':[], 'Josa':[], 'PreEomi':[], 'Eomi':[], 'Suffix':[], 'Punctuation':[], 'Foreign':[], 'Alpha':[], 'Number':[], 'Unknown':[], 'KoreanParticle'}
    res = {'CC':[], 'CD':[], 'DT':[], 'EX':[], 'FW':[], 'IN':[], 'JJ':[], 'JJR':[], 'JJS':[], 'LS':[], 'MD':[], 'NN':[], 'NNP':[], 'NNPS':[], 'NNS':[], 'PDT':[], 'POS':[], 'PRP':[], 'RB':[], 'RBR':[], 'RBS':[], 'RP':[], 'SYM':[], 'TO':[], 'UH':[], 'VB':[], 'VBD':[], 'VBG':[], 'VBN':[], 'VBP':[], 'VBZ':[], 'WDT':[], 'WP':[], 'WP$':[], 'WRB':[]}
    question_idx = []
    question = ''
    token = nltk.word_tokenize(caption)
    pos = nltk.pos_tag(token)
    for i in range(len(token)):
        tmp = pos[i]
        try:
            res[tmp[1]].append(i)
        except:
            pass
    cnt = int(len(token)*(perc/100.0))
    for pos_key in res.keys():
        tmp_len = int(cnt * float(len(res[pos_key]))/len(token))
        if tmp_len > 0:
            question_idx += list(np.random.choice(res[pos_key], tmp_len))

    for i in range(len(token)):
        if token[i] == '.':
            question += token[i] + '\n'
        elif i in question_idx:
            tmp = '_'*len(token[i])
            if token[i+1] == ',' or token[i+1] == '.':
                question += tmp
            else:
                question += tmp+' '
        else:
            if i < len(token)-1 and (token[i+1] == ',' or token[i+1] == '.'):
                question += token[i]
            else:
                question += token[i]+' '

    return pos, question.replace('` ', '\n')