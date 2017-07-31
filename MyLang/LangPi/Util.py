# -*- encoding:utf -*-

import base64
from django.shortcuts import render
from .models import user_info
import json
import pickle
import time
import cPickle
import copy

def mypage_likedislike(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    if request.method == 'POST':
        selected = request.POST.get('select').split(',')
        try:
            selected = [int(selected[0]), selected[1]]
            like_dislike = json.loads(user.like_dislike_voca)
            if selected in like_dislike['like']:
                like_dislike['like'].remove(selected)
            elif selected in like_dislike['dislike']:
                like_dislike['dislike'].remove(selected)
            user.like_dislike_voca = json.dumps(like_dislike)
        except:
            user_word = json.loads(user.extended_voca)
            if selected in user_word:
                user_word.remove(selected)
            user.extended_voca = json.dumps(user_word)
        user.save()
    ctx = {'title': 'ML(MyLang) mypage'}
    error = ''
    voca = []
    try:
        like_dislike = json.loads(user.like_dislike_voca)
        assert like_dislike != 0
        assert like_dislike != "0"
        assert like_dislike != unicode("0")

        like = like_dislike['like']
        dislike = like_dislike['dislike']
    except:
        error += "아직 추천단어/비추천단어를 설정하지 않으셨습니다."

    try:
        user_word = json.loads(user.extended_voca)
        assert len(user_word) != 0

    except:
        error += "아직 단어를 추가하지 않으셨습니다."
    ctx['like'] = like
    ctx['dislike'] = dislike
    ctx['word'] = user_word
    ctx['error'] = error

    return render(request, 'voca_like_dislike.html', ctx)

def mypage_message(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    if user.message_box != '':
        message_boxs = pickle.loads(user.message_box)
    else:
        message_boxs = []
    message_box = []
    read_message_box = []
    for message in message_boxs:
        message_box.append(
            [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(message.date)), message.content, message.new])
        tmp = copy.deepcopy(message)
        tmp.new = 0
        read_message_box.append(tmp)
        del tmp
    user.message_box = cPickle.dumps(read_message_box)
    user.save()

    ctx['message_box'] = message_box
    return render(request, 'message.html', ctx)

def mypage_vocabulary(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    error = ''
    voca = []
    try:
        voca_scores = pickle.loads(user.vocabulary_level)
        assert len(voca_scores) != 0
        for score in voca_scores:
            voca.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score.date)), score.score])
    except:
        error += 'You haven\'t do voca\n'

    ctx['voca'] = voca
    ctx['error'] = error

    return render(request, 'voca_score.html', ctx)

def mypage_reading(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    error = ''
    reading = []
    try:
        reading_scores = pickle.loads(user.readding_level)
        assert len(reading_scores) != 0
        for score in reading_scores:
            reading.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score.date)), score.score])
    except:
        error += 'You haven\'t do reading\n'
    ctx['reading'] = reading
    ctx['error'] = error

    return render(request, 'reading_score.html', ctx)

def mypage_listening(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    error = ''
    listen = []
    try:
        listen_scores = pickle.loads(user.listening_level)
        assert len(listen_scores) != 0
        for score in listen_scores:
            listen.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score.date)), score.score])
    except:
        error += 'You haven\'t do listening\n'
    ctx['listening'] = listen
    ctx['error'] = error
    return render(request, 'listening_score.html', ctx)

def mypage(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    error = ''
    listen = []
    reading = []
    voca = []
    try:
        listen_scores = pickle.loads(user.listening_level)
        assert len(listen_scores) != 0
        for score in listen_scores[:5]:
            listen.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score.date)), score.score])
        if len(listen_scores) > 5:
            listen.append(['...', '...'])
    except:
        error += 'You haven\'t do listening\n'
    try:
        reading_scores = pickle.loads(user.readding_level)
        assert len(reading_scores) != 0
        for score in reading_scores[:5]:
            reading.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score.date)), score.score])
        if len(reading_scores) > 5:
            reading.append(['...', '...'])
    except:
        error += 'You haven\'t do reading\n'
    try:
        voca_scores = pickle.loads(user.vocabulary_level)
        assert len(voca_scores) != 0
        for score in voca_scores[:5]:
            voca.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score.date)), score.score])
        if len(voca_scores) > 5:
            voca.append(['...', '...'])
    except:
        error += 'You haven\'t do voca\n'
    if user.message_box != '':
        message_boxs = pickle.loads(user.message_box)
    else:
        message_boxs = []
    message_box = []
    read_message_box = []
    for message in message_boxs[:5]:
        message_box.append(
            [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(message.date)), message.content, message.new])
        tmp = copy.deepcopy(message)
        tmp.new = 0
        read_message_box.append(tmp)
        del tmp
    user.message_box = cPickle.dumps(read_message_box)
    user.save()
    ctx = {'listening': listen, 'reading': reading, 'voca': voca, 'message_box': message_box, 'error': error}
    ctx['title'] = 'ML(MyLang) mypage'
    return render(request, 'mypage.html', ctx)