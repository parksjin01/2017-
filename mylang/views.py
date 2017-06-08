# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .Listening.caption_util import *
from .reading import *
import pickle
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

#IMG_URL: 유튜브의 썸네일을 가져오는 URL
#VOD_URL1: 최근 시청한 비디오와 유사한 비디오를 가져오는 URL
#VOD_URL2: 일반적인 유튜브 검색처럼 검색어로 비디오를 가져오는 URL
IMG_URL = '''https://i.ytimg.com/vi/%s/hqdefault.jpg?custom=true&w=336&h=188&stc=true&jpg444=true&jpgq=90&sp=68&sigh=w6tAuAmF905_ShQMYGlSjCnkNgI'''
VOD_URL1 = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=%d&order=relevance&relatedToVideoId=%s&type=video&videoCaption=closedCaption&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s"
VOD_URL2 = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=%s&maxResults=%d&order=relevance&type=video&videoCaption=closedCaption&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s"

#Parameter
# ->video_id: 연관된 유사 비디오를 찾기위한 비디오 id
# ->video_name: 검색하여 비디오를 찾을때 쓸 검색어
# ->max_results: 검색결과의 개수
#Return
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

#Parameter
# ->url: 추가하려는 유튜브의 url
def adder(request, url):
    if 'http' not in url:
        url = 'https://www.youtube.com/watch?v=' + url
    try:
        vod = youtube.objects.get(url=url)
	vod.date = datetime.now()
	vod.save()
    except Exception, e:
        vod = youtube()
        titles = title(url)
        while True:
            try:
                content, hashed_url = caption_from_downsub(url)
                break
            except:
                continue
        vod.title = titles[0]
        vod.description = titles[1]
        vod.url = url
        vod.hashed_url = hashed_url
        vod.caption = content
	vod.date = datetime.now()
        vod.save()
    return redirect('/video/')


def recommandation(url, num, cur):
    video_id = url.split('?v=')[1]
    video = youtube_search(video_id=video_id, max_results=num)
    res = []
    fmt = '''<td><a href='%s'"><img src=%s/><span>%s</span></td>'''
    for sentence in video:
        res.append(fmt % (sentence[0], sentence[3], sentence[1]))
    if cur == []:
        return res
    else:
        return res + cur[num:]


def home(request):
    message = {}
    try:
	user_email = request.COOKIES.get('ec')
	answers = tmp_answer.objects.filter(cur_user = user_email)
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
    finally:
        return render(request, 'home.html', message)


def show(request, name):
    if request.method == 'POST':
	vod = youtube.objects.get(hashed_url = name)
        cur_date = request.COOKIES.get('youan')
        tmp = tmp_answer.objects.get(cur_date=cur_date, cur_user=request.COOKIES.get('ec'))
        answer = tmp.answer
        answer = pickle.loads(binascii.unhexlify(answer))
        user = request.POST.getlist('blank')
        score = check_answer(user, answer)
        print score
        message = {
            'video': '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+vod.url.split('?v=')[1]+'"frameborder="0"></iframe>',
        }

        message['score'] = score
	user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
	level = {}
	if user.level == '':
		user.level = pickle.dumps(level)
	else:
		level = pickle.loads(user.level)
	try:
		level['en'] = level['en']*0.65 + score*0.35
	except:
		level['en'] = score*0.8
	finally:
		user.level = pickle.dumps(level)
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
    if his.recommand == '':
        recommand = recommandation(his.cur, 20, [])
        his.recommand = pickle.dumps(recommand)
    else:
        recommand = pickle.loads(his.recommand)
        recommand = recommandation(his.cur, 5, recommand)
        his.recommand = pickle.dumps(recommand)
    print cur_user
    user = user_info.objects.get(user_email=base64.b64decode(cur_user))
    his.cur_user = cur_user
    his.save()
    caption = vod.caption
    try:
        level = pickle.loads(user.level)['en\r']
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
        'video': '<iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0"></iframe>' % url,
        'form': '<div><h1>Dictation</h1><p name=dictation>%s</p></div><button type="submit">Check</button>' % question,
    }

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
	img = IMG_URL %(vod.url.split('?v=')[1])
	tmp_fmt = "'%s'"
	video.append(('/video/'+vod.hashed_url, vod.title, vod.description, img, tmp_fmt %(img+'!@#'+line)))
    ctx['video'] = video
    return render(request, 'show_list.html', ctx)


def reading(request):
    if request.method == 'POST':
        score = read(request.POST.get('foreign'), request.POST.get('kor'))
        ctx = {'score': score, 'fore': request.POST.get('foreign'), 'kor': request.POST.get('kor'),
               'test': request.POST.get('test')}
        return render(request, 'reading.html', ctx)

    return render(request, 'reading.html')


def add_video(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        adder(request, url)
    else:
        return render(request, 'add_video.html')


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
            message = {'error': 'Incorrect Id or Password'}
            return render(request, 'login.html', message)
    return render(request, 'login.html')


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
	ctx = {'level':pickle.loads(user.level)['en\r']}
	return render(request, 'mypage.html', ctx)

def test(request):
	cnt = 0
	with open('words_2.txt', 'rt') as f:
		data = f.read()
	data = unicode(data).split('\n')
	for sentence in data:
		try:
			foreign = {}
			korean = []
			eng, kor = sentence.split('|')
			kor = kor.split(',')
			foreign['en'] = eng
			for word in kor:
				korean.append(' '.join(word.split()))
			tmp_voca = voca()
			tmp_voca.foreign = pickle.dumps(foreign)
			tmp_voca.korean = pickle.dumps(korean)
			tmp_voca.save()
			cnt += 1
			if cnt % 1000 == 0:
				print cnt
		except:
			pass
	return render(request, 'home.html')
