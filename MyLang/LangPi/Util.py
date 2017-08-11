# -*- encoding:utf -*-

import base64
from django.shortcuts import render, redirect
from .models import user_info, tmp_answer, history, board
import json
import pickle
import time
import copy
import Listen
import Login

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
        except Exception, e:
            print e
            user_word = json.loads(user.extended_voca)
            if selected in user_word:
                user_word.remove(selected)
            user.extended_voca = json.dumps(user_word)
        user.save()
    ctx = {'title': 'ML(MyLang) mypage'}
    ctx['user_id'] = Login.get_current_user(request).user_id
    error = ''
    try:
        like_dislike = json.loads(user.like_dislike_voca)
        assert like_dislike != 0
        assert like_dislike != "0"
        assert like_dislike != unicode("0")

        like = like_dislike['like']
        dislike = like_dislike['dislike']
    except Exception, e:
        print e
        error += "아직 추천단어/비추천단어를 설정하지 않으셨습니다."

    try:
        user_word = json.loads(user.extended_voca)
        assert len(user_word) != 0

    except Exception, e:
        print e
        error += "아직 단어를 추가하지 않으셨습니다."
    ctx['like'] = like
    ctx['dislike'] = dislike
    ctx['word'] = user_word
    ctx['error'] = error

    return render(request, 'voca_like_dislike.html', ctx)

def mypage_message(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    ctx['user_id'] = Login.get_current_user(request).user_id
    if user.message_box != '':
        print user.message_box
        message_boxs = json.loads(user.message_box)
    else:
        message_boxs = []
    message_box = []
    read_message_box = []
    for message in message_boxs:
        message_box.append(
            [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(message[1])), message[0], message[2]])
        tmp = copy.deepcopy(message)
        tmp[2] = 0
        read_message_box.append(tmp)
        del tmp
    user.message_box = json.dumps(read_message_box)
    user.save()

    ctx['message_box'] = message_box
    return render(request, 'message.html', ctx)

def mypage_vocabulary(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    ctx['user_id'] = Login.get_current_user(request).user_id
    error = ''
    voca = []
    try:
        voca_scores = json.loads(user.vocabulary_level)
        assert len(voca_scores) != 0
        for score in voca_scores:
            voca.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score[1])), score[0]])
    except Exception, e:
        print e
        error += 'You haven\'t do voca\n'

    ctx['voca'] = voca
    ctx['error'] = error

    return render(request, 'voca_score.html', ctx)

def mypage_reading(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    ctx['user_id'] = Login.get_current_user(request).user_id
    error = ''
    reading = []
    try:
        reading_scores = json.loads(user.readding_level)
        assert len(reading_scores) != 0
        for score in reading_scores:
            reading.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score[1])), score[0]])
    except Exception, e:
        print e
        error += 'You haven\'t do reading\n'
    ctx['reading'] = reading
    ctx['error'] = error

    return render(request, 'reading_score.html', ctx)

def mypage_listening(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title': 'ML(MyLang) mypage'}
    ctx['user_id'] = Login.get_current_user(request).user_id
    error = ''
    listen = []
    try:
        listen_scores = json.loads(user.listening_level)
        assert len(listen_scores) != 0
        for score in listen_scores:
            listen.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score[1])), score[0]])
    except Exception, e:
        print e
        error += 'You haven\'t do listening\n'
    ctx['listening'] = listen
    ctx['error'] = error
    return render(request, 'listening_score.html', ctx)

def mypage(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    error = ''
    listen = []
    reading = []
    voca = []
    try:
        listen_scores = json.loads(user.listening_level)
        assert len(listen_scores) != 0
        for score in listen_scores[:5]:
            listen.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score[1])), score[0]])
        if len(listen_scores) > 5:
            listen.append(['...', '...'])
    except Exception, e:
        print e
        error += 'You haven\'t do listening\n'
    try:
        reading_scores = json.loads(user.readding_level)
        assert len(reading_scores) != 0
        for score in reading_scores[:5]:
            reading.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score[1])), score[0]])
        if len(reading_scores) > 5:
            reading.append(['...', '...'])
    except Exception, e:
        print e
        error += 'You haven\'t do reading\n'
    try:
        voca_scores = json.loads(user.vocabulary_level)
        assert len(voca_scores) != 0
        for score in voca_scores[:5]:
            voca.append([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(score[1])), score[0]])
        if len(voca_scores) > 5:
            voca.append(['...', '...'])
    except Exception, e:
        print e
        error += 'You haven\'t do voca\n'
    if user.message_box != '':
        print user.message_box, user.user_id
        message_boxs = json.loads(user.message_box)
    else:
        message_boxs = []
    message_box = []
    read_message_box = []
    for message in message_boxs[:5]:
        message_box.append(
            [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(message[1])), message[0], message[2]])
        tmp = copy.deepcopy(message)
        tmp[2] = 0
        read_message_box.append(tmp)
        del tmp
    user.message_box = json.dumps(read_message_box)
    user.save()
    ctx = {'listening': listen, 'reading': reading, 'voca': voca, 'message_box': message_box, 'error': error}
    ctx['title'] = 'ML(MyLang) mypage'
    ctx['user_id'] = Login.get_current_user(request).user_id
    print ctx
    return render(request, 'mypage.html', ctx)

def home(request):
    message = {}
    message['title'] = 'ML(MyLanguage)'
    try:
        user_email = request.COOKIES.get('ec')
        answers = tmp_answer.objects.filter(cur_user=user_email)
        message['user_id'] = Login.get_current_user(request).user_id
        for answer in answers:
            answer.delete()
    except Exception, e:
        print e
    if request.method == 'POST':
        return redirect('/search/?key=' + request.POST.get('search_key') + '&e=0')
    try:
        h = history.objects.filter(cur_user=request.COOKIES.get('ec'))[0]
        recommand = pickle.loads(h.recommand)
        message['recommand'] = recommand
    except Exception, e:
        print e
    return render(request, 'home.html', message)

def recommandation(url, num, cur):
    video_id = url.split('?v=')[1]
    video = Listen.youtube_search(video_id=video_id, max_results=num+10)
    res = []
    for sentence in video:
        tmp = [sentence[0], sentence[3], sentence[1]]
        if tmp not in cur:
            res.append(tmp)
    if cur == []:
        return res[:num]
    else:
        print cur
        return res[:num] + cur[:20-num]

def write(request):
    ctx = {'title': '글쓰기', 'authority':'0'}
    if Login.get_current_user(request) == -1:
        return render(request, 'login_please.html')
    ctx['user_id'] = Login.get_current_user(request).user_id
    ctx['category'] = request.GET.get('c')
    if request.method == "POST":
        user = Login.get_current_user(request)
        memo = board()
        memo.title = request.POST.get('title')
        memo.text = request.POST.get('content')
        memo.author = user.user_id
        memo.date = str(time.time())
        memo.category = request.POST.get('category')
        if memo.category == 'notice' and (memo.author != "parksjin01" and memo.author != "damotorie"):
            ctx['authority'] = '1'
            return render(request, 'write.html', ctx)
        memo.save()
        return redirect('/')
    return render(request, 'write.html', ctx)

def bullet_board(request):
    href = "/board/show?date=%s&id=%s"
    write_href = "/board/write?c=%s"
    ctx = {'title': '게시판'}
    if Login.get_current_user(request) != -1:
        ctx['user_id'] = Login.get_current_user(request).user_id
    ctx['category'] = request.GET.get('c')
    memo = board.objects.filter(category__exact=ctx['category'])
    message = []
    for tmp in memo:
        message.append([tmp.title, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(tmp.date))), tmp.author,
                        href % (tmp.date, tmp.author)])
    ctx['memo'] = message
    ctx['write'] = write_href %ctx['category']
    return render(request, 'board.html', ctx)

def show_memo(request):
    ctx = {'title': '게시판'}
    if Login.get_current_user(request) != -1:
        ctx['user_id'] = Login.get_current_user(request).user_id
    href = "/board/edit?date=%s&id=%s"
    date = request.GET.get('date')
    uid = request.GET.get('id')
    memo = board.objects.get(date=date, author=uid)
    if request.method == "POST":
        user = Login.get_current_user(request)
        if memo.author == user.user_id:
            memo.delete()
            return redirect('/')
    ctx['Title'] = memo.title
    ctx['Content'] = memo.text
    ctx['Date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(date)))
    ctx['Author'] = memo.author
    if memo.author == Login.get_current_user(request).user_id:
        ctx['authority'] = '0'
        ctx['href'] = href % (date, uid)
    else:
        ctx['authority'] = '1'
    return render(request, 'show_memo.html', ctx)

def edit(request):
    ctx = {'title': '게시판'}
    ctx['authority'] = '0'
    if Login.get_current_user(request) == -1:
        return render(request, 'login_please.html')
    user = Login.get_current_user(request)
    ctx['user_id'] = Login.get_current_user(request).user_id
    date = request.GET.get('date')
    uid = request.GET.get('id')
    memo = board.objects.get(date=date, author=uid)
    if memo.author != user.user_id:
        ctx['authority'] = '1'
    if request.method == "POST":
        user = Login.get_current_user(request)
        memo.title = request.POST.get('title')
        memo.text = request.POST.get('content')
        memo.author = user.user_id
        memo.date = str(time.time())
        memo.category = request.POST.get('category')
        if memo.category == 'notice' and (memo.author != "parksjin01" and memo.author != "damotorie"):
            ctx['authority'] = '1'
            return render(request, 'write.html', ctx)
        memo.save()
        return redirect('/')
    ctx['Title'] = memo.title
    ctx['Content'] = memo.text
    ctx['category'] = memo.category
    return render(request, 'edit_memo.html', ctx)

def mypage_board(request):
    user = Login.get_current_user(request)
    if Login.get_current_user(request) == -1:
        return render(request, 'login_please.html')
    href = "/board/show?date=%s&id=%s"
    ctx = {'title': '게시판'}
    ctx['user_id'] = Login.get_current_user(request).user_id
    memo = board.objects.filter(author__exact=user.user_id)
    message = []
    for tmp in memo:
        message.append([tmp.title, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(tmp.date))), tmp.category,
                        href % (tmp.date, tmp.author)])
    ctx['memo'] = message
    return render(request, 'mypage_board.html', ctx)