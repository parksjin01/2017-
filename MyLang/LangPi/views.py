# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .Listening.caption_util import *
from .reading import *
import pickle
import cPickle
import binascii
from download_caption import *
from datetime import datetime
import time
import hashlib
import random
import smtplib
import email.utils
from email.mime.text import MIMEText
import base64
import threading
import copy
import os
import json

class Score():
    def __init__(self, score, date):
        self.score = score
        self.date = date

class Message():
    def __init__(self, content, date, new):
        self.content = content
        self.date = date
        self.new = new

class Downloader(threading.Thread):
    def __init__(self, request, url):
        super(Downloader, self).__init__()
        self.request = request
        self.url = url

    def run(self):
        url = self.url
        request = self.request
        hashed_url = ''
        if 'http' not in url:
            url = 'https://www.youtube.com/watch?v=' + url
        try:
            vod = youtube.objects.get(url=url)
            vod.date = datetime.now()
            vod.save()
            message = Message('비디오가 이미 추가되어있습니다.', time.time(), 1)
        except Exception, e:
            vod = youtube()
            titles = title(url)
            for i in range(101):
                try:
                    if i == 100:
                        message = Message('비디오에 맞는 자막을 찾을수 없습니다. 다른 비디오를 찾아주세요.', time.time(), 1)
                        break
                    content, hashed_url = caption_from_downsub(url)
                    break
                except Exception, e:
                    print i, e
                    continue
            if hashed_url != '':
                print 'exited_loop'
                vod.title = titles[0]
                vod.description = titles[1]
                vod.url = url
                vod.hashed_url = hashed_url
                vod.caption = content
                vod.date = datetime.now()
                vod.save()
                message = Message('비디오가 추가되었습니다. 바로 <a href=/video/' + hashed_url + '>여기에서</a>  확인해보세요', time.time(), 1)
        try:
            cur_user = request.COOKIES.get('ec')
        except:
            return render(request, 'login_please.html')
        try:
            user = user_info.objects.get(user_email=base64.b64decode(cur_user))
        except:
            return render(request, 'login_please.html')
        if user.message_box == '':
            message_box = [message]
        else:
            message_box = [message] + cPickle.loads(str(user.message_box))
        print message_box
        user.message_box = cPickle.dumps(message_box)
        user.save()

def email_check(request):
    data = {'is_taken':user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists()}
    data['key'] = ''
    key = ''
    if user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists() == False:
        for i in range(10):
            key += chr(random.randrange(0x21, 0x7f))
        data['key'] = key
        message = 'Your validation key: %s\n' % (key)
        msg = MIMEText(message)
        msg['To'] = email.utils.formataddr(('To User', request.GET.get('email')))
        msg['From'] = email.utils.formataddr(('From Mylang Web', 'parksjin01@naver.com'))
        msg['Subject'] = 'Your temporary ID and Password'
        smtp = smtplib.SMTP_SSL('smtp.naver.com', 465)
        smtp.ehlo()
        smtp.login('parksjin01', 'FXqy9k]Abj')
        smtp.sendmail('parksjin01@naver.com', [request.GET.get('email')], msg.as_string())
        smtp.close()
    return JsonResponse(data)

def id_check(request):
    data = {'is_taken':user_info.objects.filter(user_id__iexact=request.GET.get('username')).exists()}
    return JsonResponse(data)

def get_voca_score(request):
    try:
        cur_user = request.COOKIES.get('ec')
    except:
        return render(request, 'login_please.html')
    try:
        user = user_info.objects.get(user_email=base64.b64decode(cur_user))
    except:
        return render(request, 'login_please.html')
    voca_scores = pickle.loads(user.vocabulary_level)[:30][::-1]
    data = []
    for idx in range(len(voca_scores)):
        data.append({"close": voca_scores[idx].score, "date": idx+1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)

def get_read_score(request):
    try:
        cur_user = request.COOKIES.get('ec')
    except:
        return render(request, 'login_please.html')
    try:
        user = user_info.objects.get(user_email=base64.b64decode(cur_user))
    except:
        return render(request, 'login_please.html')
    read_scores = pickle.loads(user.readding_level)[:30][::-1]
    data = []
    for idx in range(len(read_scores)):
        data.append({"close": read_scores[idx].score.strip('%'), "date": idx+1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)

def get_listen_score(request):
    try:
        cur_user = request.COOKIES.get('ec')
    except:
        return render(request, 'login_please.html')
    try:
        user = user_info.objects.get(user_email=base64.b64decode(cur_user))
    except:
        return render(request, 'login_please.html')
    listen_scores = pickle.loads(user.listening_level)[:30][::-1]
    data = []
    for idx in range(len(listen_scores)):
        data.append({"close": listen_scores[idx].score, "date": idx+1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)

def test(request):
    return render(request, 'test.html')

def process(request):
    print request.POST.get('like')
    ctx = {'like':request.POST.get('like'), 'dislike':request.POST.get('dislike')}
    return render(request, 'processing_data.html', ctx)

# IMG_URL: 유튜브의 썸네일을 가져오는 URL
# VOD_URL1: 최근 시청한 비디오와 유사한 비디오를 가져오는 URL
# VOD_URL2: 일반적인 유튜브 검색처럼 검색어로 비디오를 가져오는 URL
IMG_URL = '''https://i.ytimg.com/vi/%s/hqdefault.jpg?custom=true&w=336&h=188&stc=true&jpg444=true&jpgq=90&sp=68&sigh=w6tAuAmF905_ShQMYGlSjCnkNgI'''
VOD_URL1 = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=%d&order=relevance&relatedToVideoId=%s&type=video&videoCaption=closedCaption&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s"
VOD_URL2 = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=%s&maxResults=%d&order=relevance&type=video&videoCaption=closedCaption&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s"

# Parameter
# ->video_id: 연관된 유사 비디오를 찾기위한 비디오 id
# ->video_name: 검색하여 비디오를 찾을때 쓸 검색어
# ->max_results: 검색결과의 개수
# Return
# ->(url, 제목, 설명, 썸네일 url)
def youtube_search(video_id=0, video_name='', max_results=5):
    if video_id != 0:
        html = urllib2.urlopen(VOD_URL1 % (max_results, video_id)).read()
    elif video_name != '':
        html = urllib2.urlopen(VOD_URL2 % (video_name, max_results)).read()
    else:
        return -1
    video_id = []
    html = html.split('\n')
    new_html = []
    for sentence in html:
        if "etag" not in sentence:
            new_html.append(sentence)
    html = json.loads('\n'.join(new_html))
    for video in html['items']:
        video_id.append((('/video/add/' + video['id']['videoId'], video['snippet']['title'],
                          video['snippet']['description'],
                          IMG_URL %
                          video['id']['videoId'])))
    return video_id

# Parameter
# ->url: 추가하려는 유튜브의 url
def adder(request, url):
    downloader = Downloader(request, url)
    downloader.start()
    ctx = {'message': '검색하신 동영상에 맞는 자막을 찾아 다운로드받고 있습니다. 다소 시간이 걸리는 관계로 다운로드가 다되면 메시지로 알려드리도록 하겠습니다.'}
    return render(request, 'user_message.html', ctx)

def recommandation(url, num, cur):
    video_id = url.split('?v=')[1]
    video = youtube_search(video_id=video_id, max_results=num+10)
    res = []
    for sentence in video:
        tmp = [sentence[0], sentence[3], sentence[1]]
        if tmp not in cur:
            res.append(tmp)
    if cur == []:
        return res
    else:
        print cur
        return res + cur[:-num]

def home(request):
    message = {}
    try:
        user_email = request.COOKIES.get('ec')
        answers = tmp_answer.objects.filter(cur_user=user_email)
        for answer in answers:
            answer.delete()
    except Exception, e:
        pass
    if request.method == 'POST':
        return redirect('/search/?key=' + request.POST.get('search_key') + '&e=0')
    try:
        h = history.objects.filter(cur_user=request.COOKIES.get('ec'))[0]
        recommand = pickle.loads(h.recommand)
        message['recommand'] = recommand
        message['title'] = 'ML(MyLanguage)'
    finally:
        return render(request, 'home.html', message)

def show(request, name):
    if request.method == 'POST':
        vod = youtube.objects.get(hashed_url=name)
        cur_date = request.COOKIES.get('youan')
        tmp = tmp_answer.objects.get(cur_date=cur_date, cur_user=request.COOKIES.get('ec'))
        answer = tmp.answer
        answer = pickle.loads(binascii.unhexlify(answer))
        user = request.POST.getlist('blank')
        score = check_answer(user, answer)
        print score
        message = {
            'video': '<iframe width="560" height="315" src="https://www.youtube.com/embed/' + vod.url.split('?v=')[
                1] + '"frameborder="0"></iframe>',
        }

        message['score'] = score
        message['title'] = 'ML(MyLang) Listening score'
        user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
        level = []
        if user.listening_level == '':
            user.level = pickle.dumps(level)
        level = pickle.loads(str(user.listening_level))
        try:
            score = Score(score, time.time())
            level = [score] + level
        finally:
            user.listening_level = pickle.dumps(level)
            user.save()
        tmp.delete()
        return render(request, 'dictation.html', message)
    vod = get_object_or_404(youtube, hashed_url=name)
    try:
        cur_user = request.COOKIES.get('ec')
    except:
        return render(request, 'login_please.html')
    try:
        his = history.objects.filter(cur_user=cur_user)[0]
    except:
        his = history()
    vod.date = datetime.now()
    vod.save()
    url = vod.url.split('?v=')[1]
    his.cur = vod.url
    if his.recommand == '' or pickle.loads(his.recommand) == []:
        recommand = recommandation(his.cur, 20, [])
        his.recommand = pickle.dumps(recommand)
    else:
        recommand = pickle.loads(his.recommand)
        recommand = recommandation(his.cur, 5, recommand)
        his.recommand = pickle.dumps(recommand)
    print type(his.recommand)
    user = user_info.objects.get(user_email=base64.b64decode(cur_user))
    his.cur_user = unicode(cur_user)
    try:
        his.save()
    except:
        pass
    caption = vod.caption
    try:
        score = pickle.loads(user.level)
        level = []
        for i in score[:5]:
            level.append(i.score)
        level = sum(map(int, level)) / len(level)
        if level < 70:
            question, answer = analyze(caption, 15)
        elif level < 80:
            question, answer = analyze(caption, 20)
        else:
            question, answer = analyze(caption, 25)
    except:
        question, answer = analyze(caption)
    question = question.replace('\n', '</br>')
    answer = binascii.hexlify(pickle.dumps(answer))
    tmp = tmp_answer()
    tmp.answer = answer
    cur_date = int(time.time())
    tmp.cur_date = cur_date
    tmp.cur_user = cur_user
    tmp.save()
    message = {
        'video': '<h3 class="page-header">Dictation</h3><iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0"></iframe>' % url,
        'form': '<div style="padding-top:30px"><p name=dictation class="dictation">%s</p></div><button type="submit" class="btn btn-primary">Check</button>' % question,
    }

    message['title'] = 'ML(MyLang) Listening'
    # return HttpResponse('\n'.join(message))
    http = render(request, 'dictation.html', message)
    http.set_cookie(key="youan", value=cur_date)
    return http

def show_list(request):
    tube = youtube.objects.order_by('-date').all()
    ctx = {}
    video = []
    for vod in tube:
        cap = vod.caption
        line = 0
        if '\r\n' in cap:
            line = cap.strip().split('\r\n\r\n')[-1].split('\r\n')[0]
        else:
            line = cap.strip().split('\n\n')[-1].split('\n')[0]
        img = IMG_URL % (vod.url.split('?v=')[1])
        tmp_fmt = "'%s'"
        description = vod.description
        if len(description) > 200:
            description = description[:200] + ' ...'
        video.append(('/video/' + vod.hashed_url, vod.title, description, img, tmp_fmt % (img + '!@#' + line)))
    ctx['video'] = video
    ctx['title'] = 'ML(MyLang) Video List'
    return render(request, 'show_list.html', ctx)

def reading(request):
    if request.method == 'POST':
        if len(request.POST.get('foreign')) >= 5000:
            ctx = {'title':'ML(MyLang) Reading', 'error':'1'}
            return render(request, 'reading.html', ctx)
        score = read(request.POST.get('foreign'), request.POST.get('kor'))
        try:
            cur_user = request.COOKIES.get('ec')
        except:
            return render(request, 'login_please.html')
        try:
            user = user_info.objects.get(user_email=base64.b64decode(cur_user))
        except:
            return render(request, 'login_please.html')
        reading = [Score(score, time.time())] + cPickle.loads(str(user.readding_level))
        user.readding_level = cPickle.dumps(reading)
        user.save()
        ctx = {'score': score, 'fore': request.POST.get('foreign'), 'kor': request.POST.get('kor'),
               'test': request.POST.get('test'), 'title':'ML(MyLang) Reading', 'error':'0'}
        return render(request, 'reading.html', ctx)
    ctx = {'title':'ML(MyLang)', 'error':'0'}
    return render(request, 'reading.html', ctx)

def add_video(request):
    ctx = {'title': 'ML(MyLang)Add video'}
    if request.method == 'POST':
        if request.POST.get('url') != u'':
            url = request.POST.get('url')
            adder(request, url)
        elif request.POST.get('keyword') != u'':
            keyword = request.POST.get('keyword')
            video = youtube_search(video_name=keyword, max_results=40)
            ctx['video'] = video
            return render(request, 'add_video.html', ctx)
    else:
        return render(request, 'add_video.html', ctx)

def login(request):
    if request.method == 'POST':
        try:
            user = user_info.objects.get(user_id=request.POST.get('user_id'),
                                         user_pw=hashlib.md5(request.POST.get('user_pw')).hexdigest())
            http = redirect('/')
            http.set_cookie(key="ic", value=hashlib.md5(user.user_id).hexdigest())
            http.set_cookie(key="pc", value=hashlib.md5(user.user_email).hexdigest())
            http.set_cookie(key="ec", value=base64.b64encode(user.user_email))
            return http
        except Exception, e:
            message = {'error': 'Incorrect Id or Password', 'title':'ML(MyLanguage) Login'}
            return render(request, 'login.html', message, message)
    return render(request, 'login.html', {'title':'ML(MyLanguage) Login'})

def register(request):
    if request.method == 'POST':
        try:
            user_info.objects.get(user_email=request.POST.get('user_email'))
            message = {'error': 'Email address is already inuse'}
            return render(request, 'register.html', message)
        except:
            new_user = user_info()
            new_user.user_id = request.POST.get('user_id')
            new_user.user_pw = hashlib.md5(request.POST.get('user_pw')).hexdigest()
            new_user.user_email = request.POST.get('user_email')
            new_user.save()
    return render(request, 'register.html')

def find_id(request):
    if request.method == 'POST':
        key_pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        tmp_id = ''
        tmp_pw = ''
        try:
            user = user_info.objects.get(user_email=request.POST.get('user_email'))
            for i in range(10):
                tmp_id += key_pool[random.randrange(0, len(key_pool))]
                tmp_pw += key_pool[random.randrange(0, len(key_pool))]
            message = 'Your new ID: %s\nYour new Password: %s\n' % (tmp_id, tmp_pw)
            msg = MIMEText(message)
            msg['To'] = email.utils.formataddr(('To User', request.POST.get('user_email')))
            msg['From'] = email.utils.formataddr(('From Mylang Web', 'parksjin01@naver.com'))
            msg['Subject'] = 'Your temporary ID and Password'
            smtp = smtplib.SMTP_SSL('smtp.naver.com', 465)
            smtp.ehlo()
            smtp.login('parksjin01', 'FXqy9k]Abj')
            smtp.sendmail('parksjin01@naver.com', [request.POST.get('user_email')], msg.as_string())
            smtp.close()
            user.user_id = tmp_id
            user.user_pw = hashlib.md5(tmp_pw).hexdigest()
            user.save()
        except Exception, e:
            message = {'error': 'Email address is invalid, You can\'t use g-mail for this service'}
            return render(request, 'find-id.html', message)
    return render(request, 'find-id.html')

def change_id(request):
    if request.method == 'POST':
        next_id = request.POST.get('user_id')
        next_pw = hashlib.md5(request.POST.get('user_pw')).hexdigest()
        cur_email = base64.b64decode(request.COOKIES.get('ec'))
        user = user_info.objects.get(user_email=cur_email)
        user.user_id = next_id
        user.user_pw = next_pw
        user.save()
    return render(request, 'change-id.html')

def search(request):
    key, extend = request.GET.get('key'), request.GET.get('e')
    context = {}
    db = youtube.objects.filter(title__contains=key)
    if len(db) > 0:
        tmp_db = []
        for d in db:
            video_id = d.url.split('?v=')[1]
            tmp_db.append(('/video/' + d.hashed_url, d.title, IMG_URL % video_id))
        context['db'] = tmp_db
    if extend == '1':
        video = youtube_search(video_name=key, max_results=20)
        context['video'] = video
    return render(request, "search.html", context)

def mypage(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    ctx = {'title':'ML(MyLang) mypage'}
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

def mypage_likedislike(request):
    user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
    if request.method == 'POST':
        selected = request.POST.get('select').split(',')
        selected = [int(selected[0]), selected[1]]
        like_dislike = json.loads(user.like_dislike_voca)
        if selected in like_dislike['like']:
            like_dislike['like'].remove(selected)
        elif selected in like_dislike['dislike']:
            like_dislike['dislike'].remove(selected)
        print like_dislike
        user.like_dislike_voca = json.dumps(like_dislike)
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

    ctx['like'] = like
    ctx['dislike'] = dislike
    ctx['error'] = error

    return render(request, 'voca_like_dislike.html', ctx)

def vocabulary(request):
    if request.method == 'POST':
        try:
            user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
        except:
            return render(request, 'login_please.html')
        if request.POST.get('method') == unicode('1'):
            like_dislike = json.loads(user.like_dislike_voca)
            if like_dislike == unicode('0') or like_dislike == str('0') or like_dislike == 0:
                like_dislike = {'like':[], 'dislike':[]}
            like = request.POST.get('like').split(',')
            dislike = request.POST.get('dislike').split(',')

            for word in like:
                if word == '':
                    break
                word_info = voca.objects.get(foreign__contains = 'V'+word+'\n')
                like_dislike['like'].append([word_info.id, word])
                word_info.save()

            for word in dislike:
                if word == '':
                    break
                word_info = voca.objects.get(foreign__contains = 'V'+word+'\n')
                like_dislike['dislike'].append([word_info.id, word])
                word_info.save()

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
        ctx = {'result': result, 'whole': whole}
        ctx['title'] = 'ML(MyLang) Voca result'
        score = Score(int(result), time.time())
        levels = [score] + cPickle.loads(str(user.vocabulary_level))
        user.vocabulary_level = cPickle.dumps(levels)
        user.save()
        tmp.delete()
        return render(request, 'voca.html', ctx)

    with open(str('/Volumes/UUI/2017-/MyLang/LangPi/number.txt'), 'rt') as f:
        num = int(f.read())
    try:
        cur_user = request.COOKIES.get('ec')
    except:
        return render(request, 'login_please.html')
    try:
        user = user_info.objects.get(user_email=base64.b64decode(cur_user))
    except:
        return render(request, 'login_please.html')
    like_dislike = json.loads(user.like_dislike_voca)
    if like_dislike == u'0' or like_dislike == 0:
        like_dislike = {'like':[], 'dislike':[]}
    scores = cPickle.loads(str(user.vocabulary_level))
    levels = []
    if len(scores) != 0:
        for i in scores[:5]:
            levels.append(i.score)
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
        random_number = random.randrange(num)
        random_voca = pickle.loads(voca.objects.get(id=random_number + 3335).foreign)['en']
        if ([random_number, random_voca] not in like_dislike['like']) and ([random_number, random_voca] not in like_dislike['dislike']):
            test.add(random.randrange(num))
    word = []
    answer = []
    for idx in test:
        tmp = []
        tmp.append(pickle.loads(voca.objects.get(id=idx + 3335).foreign)['en'])
        meaning = []
        whole_meaning = pickle.loads(voca.objects.get(id=idx + 3335).korean)
        tmp_meaning = pickle.loads(voca.objects.get(id=idx + 3335).korean)[
            random.randrange(len(pickle.loads(voca.objects.get(id=idx + 3335).korean)))]
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
    tmp = tmp_answer()
    tmp.answer = pickle.dumps(answer)
    cur_date = int(time.time())
    tmp.cur_date = cur_date
    tmp.cur_user = cur_user
    tmp.save()
    ctx = {'test': word}
    ctx['title'] = 'ML(MyLang) Voca'
    http = render(request, 'voca.html', ctx)
    http.set_cookie(key="youan", value=cur_date)
    return http
