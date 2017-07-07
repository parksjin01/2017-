# -*- encoding:utf-8 -*-
import nltk
import numpy as np

def parsing(caption):
    res = []
    switch = 0
    if '\r\n\r\n' in caption:
    	caption = caption.split('\r\n\r\n')
    else:
	caption = caption.split('\n\n')
    for sentence in caption:
        tmp = ''
        for each in sentence.split('\n')[2:]:
            for char in each:
                if char == '<' or char == '[' or char == '(':
                    switch += 1
                elif (char == '>' or char == ']' or char == ')') and switch > 0:
                    switch -= 1
                if switch == 0 and char != '>' and char != ']' and char != ')':
                    tmp += char
        if tmp:
            res.append(tmp)
    return '\n` '.join(res)

def analyze(caption, perc = 10):
    if perc > 100:
        print '[-]Percentage can\'t above 100%'
    caption = parsing(caption)
    res = {'CC':[], 'CD':[], 'DT':[], 'EX':[], 'FW':[], 'IN':[], 'JJ':[], 'JJR':[], 'JJS':[], 'LS':[], 'MD':[], 'NN':[], 'NNP':[], 'NNPS':[], 'NNS':[], 'PDT':[], 'POS':[], 'PRP':[], 'RB':[], 'RBR':[], 'RBS':[], 'RP':[], 'SYM':[], 'TO':[], 'UH':[], 'VB':[], 'VBD':[], 'VBG':[], 'VBN':[], 'VBP':[], 'VBZ':[], 'WDT':[], 'WP':[], 'WP$':[], 'WRB':[]}
    question_idx = []
    question = ''
    answer = [] 
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
        if i in question_idx:
	    tmp = '<input type=text name=blank placeholder=%s size=%d></input>' %(('_'*len(token[i])), len(token[i]))
            if i<len(token)-1 and (token[i+1] == ',' or token[i+1] == '.'):
                question += tmp
                answer.append(token[i])
            elif i < len(token)-1 and 2 <= len(token[i+1]) and len(token[i+1]) < 5 and (token[i+1][0] == "'" or (token[i+1][1] == "'" and token[i+1][0] == 'n')):
                question += tmp
                answer.append(token[i])
            else:
                question += tmp+' '
                answer.append(token[i])
        else:
            if i < len(token)-1 and (token[i+1] == ',' or token[i+1] == '.'):
                question += token[i]
            elif i < len(token)-1 and 2 <= len(token[i+1]) and len(token[i+1]) < 5 and (token[i+1][0] == "'" or (token[i+1][1] == "'" and token[i+1][0] == 'n')):
                question += token[i]
            else:
                question += token[i]+' '

    return question.replace('` ', '\n'), answer

def check_answer(user, answer):
    cnt_problem = len(answer)
    correct = 0
    for idx in range(len(user)):
	print user[idx]== answer[idx]
        if user[idx].lower() == answer[idx].lower():
            print 1
            correct += 1
    return float(correct)/cnt_problem*100
