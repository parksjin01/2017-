# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import Login
import Ajax
# import Listen
# import Read
import Voca
import Util
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .Listening.caption_util import *
from .reading import *
import pickle
import cPickle
import binascii
from download_caption import *
from datetime import datetime
import time
import base64
import threading
import json
import urllib

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
        user = Login.get_current_user(request)
        if user == -1:
            return render(request, "login_please.html")
        if 'http' not in url:
            url = 'https://www.youtube.com/watch?v=' + url
        try:
            user_youtube = json.loads(user.youtube)
            vod = youtube.objects.get(url=url)
            vod.date = datetime.now()
            vod.save()
            if url in user_youtube:
                message = Message('비디오가 이미 추가되어있습니다.', time.time(), 1)
            else:
                user_youtube.append(url)
                user.youtube = json.dumps(user_youtube)
                message = Message('비디오가 추가되었습니다. 바로 <a href=/video/' + vod.hashed_url + '>여기에서</a>  확인해보세요', time.time(), 1)
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
        if user.message_box == '':
            message_box = [message]
        else:
            message_box = [message] + cPickle.loads(str(user.message_box))
        print message_box
        user.message_box = cPickle.dumps(message_box)
        user.save()

def login(request):
    return Login.login(request)

def register(request):
    return Login.register(request)

def find_id(request):
    return Login.find_id(request)

def change_id(request):
    return Login.change_id(request)

def email_check_v2(request):
    return Ajax.email_check_v2(request)

def email_check(request):
    return Ajax.email_check(request)

def id_check(request):
    return Ajax.id_check(request)

def get_voca_score(request):
    return Ajax.get_voca_score(request)

def get_read_score(request):
    return Ajax.get_read_score(request)

def get_listen_score(request):
    return Ajax.get_listening_score(request)

# def test(request):
#     return render(request, 'test.html')
# def process(request):
#     print request.POST.get('like')
#     ctx = {'like':request.POST.get('like'), 'dislike':request.POST.get('dislike')}
#     return render(request, 'processing_data.html', ctx)


IMG_URL = '''https://i.ytimg.com/vi/%s/hqdefault.jpg?custom=true&w=336&h=188&stc=true&jpg444=true&jpgq=90&sp=68&sigh=w6tAuAmF905_ShQMYGlSjCnkNgI'''
VOD_URL1 = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=%d&order=relevance&relatedToVideoId=%s&type=video&videoCaption=closedCaption&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s"
VOD_URL2 = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=%s&maxResults=%d&order=relevance&type=video&videoCaption=closedCaption&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s"


def youtube_search(video_id=0, video_name='', max_results=5):
    video_name = urllib.quote_plus(video_name.encode('utf-8'))
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
    user = Login.get_current_user(request)
    if user == -1:
        return render(request, "login_please.html")
    user_youtube = json.loads(user.youtube)
    if 'https://www.youtube.com/watch?v='+url in user_youtube:
        vod = youtube.objects.get(url='https://www.youtube.com/watch?v=' + url)
        return redirect('/video/'+vod.hashed_url)
    downloader = Downloader(request, url)
    downloader.start()
    ctx = {'message': '검색하신 동영상에 맞는 자막을 찾아 다운로드받고 있습니다. 다소 시간이 걸리는 관계로 다운로드가 다되면 메시지로 알려드리도록 하겠습니다.'}
    user_youtube.append(url)
    print user_youtube
    print url
    user.youtube = json.dumps(user_youtube)
    user.save()
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
        return res[:num]
    else:
        print cur
        return res[:num] + cur[:20-num]

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

def dictation(request, name):
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
    user = Login.get_current_user(request)
    if user == -1:
        return render(request, "login_please.html")
    try:
        his = history.objects.filter(cur_user=base64.b64encode(user.user_email))[0]
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
    his.cur_user = unicode(base64.b64encode(user.user_email))
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
    tmp.cur_user = base64.b64encode(user.user_email)
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

def video_list(request):
    tube = youtube.objects.order_by('-date').all()
    ctx = {}
    video = []
    user = Login.get_current_user(request)
    if user == -1:
        return render(request, "login_please.html")
    user_youtube = json.loads(user.youtube)
    for vod in tube:
        if vod.url not in user_youtube:
            continue
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
        if score[0] == u'-':
            score = u'0%'
        user = Login.get_current_user(request)
        if user == -1:
            return render(request, "login_please.html")
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
            return adder(request, url)
        elif request.POST.get('keyword') != u'':
            keyword = request.POST.get('keyword')
            video = youtube_search(video_name=keyword, max_results=40)
            ctx['video'] = video
            return render(request, 'add_video.html', ctx)
        else:
            return render(request, 'add_video.html', ctx)
    else:
        return render(request, 'add_video.html', ctx)

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
    return Util.mypage(request)

def mypage_listening(request):
    return Util.mypage_listening(request)

def mypage_reading(request):
    return Util.mypage_reading(request)

def mypage_vocabulary(request):
    return Util.mypage_vocabulary(request)

def mypage_message(request):
    return Util.mypage_message(request)

def mypage_likedislike(request):
    return Util.mypage_likedislike(request)

def voca_exam(request):
    return Voca.voca_exam(request)

def add_voca(request):
    return Voca.add_voca(request)