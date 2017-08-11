# -*- encoding:utf-8 -*-

from .models import voca, tmp_answer
import pickle
import random
import base64
import Login
from django.shortcuts import render, redirect
import json
import time
import vocabulary

def add_voca(request):
    ctx = {'title': '단어 추가'}
    ctx['user_id'] = Login.get_current_user(request).user_id
    if request.method == 'POST':
        word = []
        final = []
        user = Login.get_current_user(request)
        if user == -1:
            return render(request, "login_please.html")
        number = int(request.POST.get("number"))
        for i in range(1, number+1):
            if [request.POST.get("word"+str(i)), request.POST.get("mean"+str(i))] != [u"", u""]:
                word.append([request.POST.get("word"+str(i)), request.POST.get("mean"+str(i))])
        for w in word:
            try:
                voca.objects.get(foreign__contains="V%s\n" %w[0])
            except Exception, e:
                print e
                final.append(w)
        user_word = json.loads(user.extended_voca)
        user_word += final
        user.extended_voca = json.dumps(user_word)
        user.save()
        return render(request, 'home.html', ctx)
    return render(request, 'add_voca.html', ctx)

def voca_exam(request):
    if request.method == 'POST':
        ctx = {"title":"단어 시험"}
        user = Login.get_current_user(request)
        if user == -1:
            return render(request, "login_please.html")
        ctx['user_id'] = Login.get_current_user(request).user_id
        if request.POST.get('method') == unicode('1'):
            like_dislike = json.loads(user.like_dislike_voca)
            if like_dislike == unicode('0') or like_dislike == str('0') or like_dislike == 0:
                like_dislike = {'like':[], 'dislike':[]}
            like = request.POST.get('like').split(',')
            dislike = request.POST.get('dislike').split(',')

            for word in like:
                try:
                    if word == '':
                        break
                    word_info = voca.objects.get(foreign__contains = 'V'+word+'\n')
                    like_dislike['like'].append([word_info.id, word])
                    word_info.save()
                except Exception, e:
                    print e
                    pass

            for word in dislike:
                try:
                    if word == '':
                        break
                    word_info = voca.objects.get(foreign__contains = 'V'+word+'\n')
                    like_dislike['dislike'].append([word_info.id, word])
                    word_info.save()
                except Exception, e:
                    print e
                    pass

            user.like_dislike_voca = json.dumps(like_dislike)
            user.save()
            return redirect('/')
        cur_date = request.COOKIES.get('youan')
        tmp = tmp_answer.objects.get(cur_date=cur_date, cur_user=request.COOKIES.get('ec'))
        answer = pickle.loads(tmp.answer)
        user_answer = []
        result = 0
        for word in answer:
            user_answer.append(request.POST.get(word[0]))
            if request.POST.get(word[0]) == word[-1]:
                result += 1

        result = result / float(len(answer)) * 100
        whole_test = []
        whole_answer = []
        for word in answer:
            whole_test.append(word[:-1])
            whole_answer.append(word[-1])
        whole = zip(whole_test, whole_answer, user_answer)
        print whole_answer
        ctx = {'result': result, 'whole': whole, 'lang':request.GET.get('category')}
        ctx['title'] = 'ML(MyLang) Voca result'
        score = [int(result), time.time()]
        levels = [score] + json.loads(str(user.vocabulary_level))
        user.vocabulary_level = json.dumps(levels)
        user.save()
        tmp.delete()
        return render(request, 'voca.html', ctx)

    with open(str('/Volumes/UUI/2017-/MyLang/LangPi/number.txt'), 'rt') as f:
        num = int(f.read())
    user = Login.get_current_user(request)
    if user == -1:
        return render(request, "login_please.html")
    user_word = json.loads(user.extended_voca)
    like_dislike = json.loads(user.like_dislike_voca)
    if like_dislike == u'0' or like_dislike == 0:
        like_dislike = {'like':[], 'dislike':[]}
    scores = json.loads(str(user.vocabulary_level))
    levels = []
    if len(scores) != 0:
        for i in scores[:5]:
            levels.append(i[0])
        level = sum(map(int, levels)) / len(levels)
    else:
        level = 70
    if level <= 70:
        example = 3
    elif level <= 80:
        example = 4
    else:
        example = 5
    if level <= 85:
        question = 20
    elif level <= 90:
        question = 30
    else:
        question = 40
    test = set()
    while len(test) < question:
        random_number = random.randrange(num+len(user_word))
        if random_number < num:
            random_voca = pickle.loads(voca.objects.get(id=random_number + 3335).foreign)['en']
            if ([random_number, random_voca] not in like_dislike['like']) and ([random_number, random_voca] not in like_dislike['dislike']):
                test.add(random_number)
        else:
            test.add(random_number)
    word = []
    answer = []
    for idx in test:
        tmp = []
        if idx < num:
            tmp.append(pickle.loads(voca.objects.get(id=idx + 3335).foreign)['en'])
        else:
            tmp.append(user_word[idx-num][0])
        meaning = []
        if idx < num:
            whole_meaning = pickle.loads(voca.objects.get(id=idx + 3335).korean)
            tmp_meaning = pickle.loads(voca.objects.get(id=idx + 3335).korean)[
                random.randrange(len(pickle.loads(voca.objects.get(id=idx + 3335).korean)))]
        else:
            whole_meaning = user_word[idx-num][1]
            tmp_meaning = user_word[idx-num][1]
        meaning.append(tmp_meaning)
        while len(meaning) < example:
            rand = random.randrange(num)
            tmp_meaning = pickle.loads(voca.objects.get(id=rand + 3335).korean)[
                random.randrange(len(pickle.loads(voca.objects.get(id=rand + 3335).korean)))]
            if tmp_meaning not in whole_meaning:
                meaning.append(tmp_meaning)
        tmp_meaning = meaning[0]
        random.shuffle(meaning)
        for mean in meaning:
            tmp.append(mean)
        word.append(tmp[::])
        tmp.append(unicode(meaning.index(tmp_meaning) + 1))
        answer.append(tmp)
    # print answer
    if request.GET.get('category') != 'en':
        answer2 = []
        word = []
        for tmp_word in answer:
            tmp_fore = tmp_word[int(tmp_word[-1])]
            try:
                tmp_fore, tmp_mean = vocabulary.change(tmp_fore, request.GET.get('category'))
            except Exception, e:
                print e
                tmp_fore = tmp_word[0]
                tmp_mean = tmp_word[int(tmp_word[-1])]
            tmp_word[int(tmp_word[-1])] = tmp_mean
            answer2.append([tmp_fore]+tmp_word[1:])
            word.append([tmp_fore]+tmp_word[1:-1])
        answer = answer2[::]
    print answer[0][0], type(answer[0][0])
    tmp = tmp_answer()
    tmp.answer = pickle.dumps(answer)
    print type(tmp.answer)
    cur_date = int(time.time())
    tmp.cur_date = cur_date
    tmp.cur_user = base64.b64encode(user.user_email)
    tmp.save()
    ctx = {'test': word}
    ctx['title'] = 'ML(MyLang) Voca'
    ctx['user_id'] = Login.get_current_user(request).user_id
    ctx['lang'] = request.GET.get('category')
    http = render(request, 'voca.html', ctx)
    http.set_cookie(key="youan", value=cur_date)
    return http