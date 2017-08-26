# -*- encoding:utf-8 -*-

from .Listening.caption_util import *
import Login
from django.shortcuts import render, redirect, get_object_or_404
from .models import youtube, tmp_answer, history, user_info
from download_caption import *
import threading
import binascii
import time
import pickle
import base64
import datetime
import Util

#듣기 파일 다운
class Downloader(threading.Thread):
    def __init__(self, request, url):
        super(Downloader, self).__init__()
        self.request = request
        self.url = url

    def run(self):
        url = self.url
        request = self.request
        hashed_url = ''
		#로그인이 되어있지 않다면 login_please.html 띄우기
        user = Login.get_current_user(request)
        if user == -1:
            return render(request, "login_please.html")
		#'http'가 url에 없다면
		#'https://www.youtube.com/watch?v='를 추가
        if u'http' not in url:
            url = 'https://www.youtube.com/watch?v=' + url
		#듣기영상추가 요청
        try:
            user_youtube = json.loads(user.youtube)
            vod = youtube.objects.get(url=url)
            vod.date = datetime.datetime.now()
            vod.save()
			#user_youtube에 비디오가 있을경우
            if url in user_youtube:
                message = ['비디오가 이미 추가되어있습니다.', time.time(), 1]
                user.new_message = str(int(user.new_message)+1)
			#user_youtube에 비디오가 없을경우
            else:
                user_youtube.append(url)
                user.youtube = json.dumps(user_youtube)
                message = ['비디오가 추가되었습니다. 바로 <a href=/video/' + vod.hashed_url + '>여기에서</a>  확인해보세요', time.time(), 1]
                user.new_message = str(int(user.new_message) + 1)
        except Exception, e:
            print e
            vod = youtube()
            titles = title(url)
            for i in range(101):
                try:
					#듣기영상추가 후 자막이 없는 비디오일경우
                    if i == 100:
                        message = ['비디오에 맞는 자막을 찾을수 없습니다. 다른 비디오를 찾아주세요.', time.time(), 1]
                        user.new_message = str(int(user.new_message) + 1)
                        break
                    content, hashed_url = caption_from_downsub(url)
                    break
                except Exception, e:
                    print i, e
			#듣기영상추가 후 자막이 있는 비디오일경우
            if hashed_url != '':
                print 'exited_loop'
                vod.title = titles[0]
                vod.description = titles[1]
                vod.url = url
                vod.hashed_url = hashed_url
                vod.caption = content
                vod.date = datetime.datetime.now()
                vod.save()
                user_youtube = json.loads(user.youtube)
                user_youtube.append(url)
                user.youtube = json.dumps(user_youtube)
                user.save()
                message = ['비디오가 추가되었습니다. 바로 <a href=/video/' + hashed_url + '>여기에서</a>  확인해보세요', time.time(), 1]
                user.new_message = str(int(user.new_message) + 1)
        if user.message_box == '':
            message_box = [message]
        else:
            message_box = [message] + json.loads(user.message_box)
        user.message_box = json.dumps(message_box)
        user.save()

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

#youtube검색 함수
def youtube_search(video_id=0, video_name='', max_results=5):
    video_name = urllib.quote_plus(video_name.encode('utf-8'))
	#고유번호가 0이 아닌경우
    if video_id != 0:
        html = urllib2.urlopen(VOD_URL1 % (max_results, video_id)).read()
	#이름이 빈칸이 아닌경우
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

#youtube영상 자막추가 함수
def adder(request, url):
    user = Login.get_current_user(request)
	#로그인이 되어있지 않다면 login_please.html 띄우기
    if user == -1:
        return render(request, "login_please.html")
    user_youtube = json.loads(user.youtube)
	#서버에 요청한비디오가 있는지 비교
    if 'https://www.youtube.com/watch?v='+url in user_youtube:
        vod = youtube.objects.get(url='https://www.youtube.com/watch?v=' + url)
        return redirect('/video/'+vod.hashed_url)
    downloader = Downloader(request, url)
	#자막 다운로드
    downloader.start()
    ctx = {'message': '검색하신 동영상에 맞는 자막을 찾아 다운로드받고 있습니다. 다소 시간이 걸리는 관계로 다운로드가 다되면 메시지로 알려드리도록 하겠습니다.', 'title':'자막 다운로드중'}
    ctx['user_id'] = Login.get_current_user(request).user_id
    user_youtube.append(url)
    user.youtube = json.dumps(user_youtube)
    user.save()
    return render(request, 'user_message.html', ctx)

#듣기 빈칸만들기 함수
def dictation(request, name):
    if request.method == 'POST':
        vod = youtube.objects.get(hashed_url=name)
        cur_date = request.COOKIES.get('youan')
        tmp = tmp_answer.objects.get(cur_date=cur_date, cur_user=request.COOKIES.get('ec'))
        answer = tmp.answer
        question = tmp.question
        answer = pickle.loads(binascii.unhexlify(answer))
        user = request.POST.getlist('blank')
        score = check_answer(user, answer)
        idx = 0
		#
        for correct in answer:
			#정오답 표시
            if correct == user[idx]:
                tmp_idx = question.index('<input type=text name=blank></input>')
                question = question[:tmp_idx]+('<span style="border-bottom: solid; border-bottom-color: deepblue;">%s</span>' %user[idx])+question[tmp_idx+36:]
            else:
                tmp_idx = question.index('<input type=text name=blank></input>')
                question = question[:tmp_idx] + (
                '<span style="border-bottom: solid; border-bottom-color: deeppink;">%s</span>' % user[idx]) + question[tmp_idx+36:]
            idx += 1
        message = {
            'video': '<iframe width="560" height="315" src="https://www.youtube.com/embed/' + vod.url.split('?v=')[
                1] + '"frameborder="0"></iframe>', 'title':'듣기 평가', 'result': question
        }

        message['score'] = score
        message['user_id'] = Login.get_current_user(request).user_id
        message['number'] = Login.get_current_user(request).new_message
        user = user_info.objects.get(user_email=base64.b64decode(request.COOKIES.get('ec')))
		#점수기록
        level = []
        if user.listening_level == '':
            user.level = json.dumps(level)
        level = json.loads(str(user.listening_level))
        try:
            score = [score, time.time()]
            level = [score] + level
        finally:
            user.listening_level = json.dumps(level)
            user.save()
        tmp.delete()
        return render(request, 'dictation.html', message)
	#영상이 없을경우 에러
    vod = get_object_or_404(youtube, hashed_url=name)
    user = Login.get_current_user(request)
	#로그인이 되어있지 않다면 login_please.html 띄우기
    if user == -1:
        return render(request, "login_please.html")
    try:
        his = history.objects.filter(cur_user=base64.b64encode(user.user_email))[0]
    except Exception, e:
        print e
        his = history()
    vod.date = datetime.datetime.now()
    vod.save()
    url = vod.url.split('?v=')[1]
    his.cur = vod.url
	#처음에 영상을 봤을경우 20개추천
    if his.recommand == '' or pickle.loads(his.recommand) == []:
        recommand = Util.recommandation(his.cur, 20, [])
        his.recommand = pickle.dumps(recommand)
	#이미 추천영상이 있는경우 5개
    else:
        recommand = pickle.loads(his.recommand)
        recommand = Util.recommandation(his.cur, 5, recommand)
        his.recommand = pickle.dumps(recommand)
    print type(his.recommand)
    his.cur_user = unicode(base64.b64encode(user.user_email))
    try:
        his.save()
    except Exception, e:
        print e
    caption = vod.caption
    try:
        score = pickle.loads(user.level)
        level = []
		#최근 5개점수 불러오기
		#평균 점수별 문제 갯수 차등화
        for i in score[:5]:
            level.append(i.score)
        level = sum(map(int, level)) / len(level)
        if level < 70:
            question, answer = analyze(caption, 15)
        elif level < 80:
            question, answer = analyze(caption, 20)
        else:
            question, answer = analyze(caption, 25)
    except Exception, e:
        print e
        question, answer = analyze(caption)
    question = question.replace('\n', '</br>')
    answer = binascii.hexlify(pickle.dumps(answer))
    tmp = tmp_answer()
    tmp.answer = answer
    tmp.question = question
    cur_date = int(time.time())
    tmp.cur_date = cur_date
    tmp.cur_user = base64.b64encode(user.user_email)
    tmp.save()
    message = {
        'video': '<h3 class="page-header">Dictation</h3><iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0"></iframe>' % url,
        'form': '<div style="padding-top:30px"><p name=dictation class="dictation">%s</p></div><button type="submit" class="btn btn-primary">Check</button>' % question,
    }

    message['title'] = 'ML(MyLang) Listening'
    message['user_id'] = Login.get_current_user(request).user_id
    message['number'] = Login.get_current_user(request).new_message
    # return HttpResponse('\n'.join(message))
    http = render(request, 'dictation.html', message)
    http.set_cookie(key="youan", value=cur_date)
    return http

#듣기창 화면
def video_list(request):
    tube = youtube.objects.order_by('-date').all()
    ctx = {}
    video = []
    user = Login.get_current_user(request)
	#로그인이 되어있지 않다면 login_please.html 띄우기
    if user == -1:
        return render(request, "login_please.html")
    user_youtube = json.loads(user.youtube)
    for vod in tube:
		#user_youtube 동영상 url이 없을경우
        if vod.url not in user_youtube:
            continue
        cap = vod.caption
        line = 0
		#운영체제별 개행문자
        if '\r\n' in cap:
            line = cap.strip().split('\r\n\r\n')[-1].split('\r\n')[0]
        else:
            line = cap.strip().split('\n\n')[-1].split('\n')[0]
        img = IMG_URL % (vod.url.split('?v=')[1])
        tmp_fmt = "'%s'"
        description = vod.description
        if len(description) > 200:
            description = description[:200] + ' ...'
		#비디오 추가
        video.append(('/video/' + vod.hashed_url, vod.title, description, img, tmp_fmt % (img + '!@#' + line)))
    ctx['video'] = video
    ctx['title'] = 'ML(MyLang) Video List'
    ctx['user_id'] = Login.get_current_user(request).user_id
    ctx['number'] = Login.get_current_user(request).new_message
    return render(request, 'show_list.html', ctx)

# 유튜브에서 동영상 추가
def add_video(request):
    ctx = {'title': 'ML(MyLang)Add video'}
    if request.method == 'POST':
		#로그인 유무 확인
        if Login.get_current_user(request) != -1:
            ctx['user_id'] = Login.get_current_user(request).user_id
		#url로 검색요청
        if request.POST.get('url') != u'':
            url = request.POST.get('url')
            return adder(request, url)
		#키워드로 검색요청
        elif request.POST.get('keyword') != u'':
            keyword = request.POST.get('keyword')
            video = youtube_search(video_name=keyword, max_results=40)
            ctx['video'] = video
            return render(request, 'add_video.html', ctx)
        else:
            return render(request, 'add_video.html', ctx)
    else:
        if Login.get_current_user(request) != -1:
            ctx['user_id'] = Login.get_current_user(request).user_id
        return render(request, 'add_video.html', ctx)

# 유튜브에서 동영상 검색
def search(request):
    key, extend = request.GET.get('key'), request.GET.get('e')
    context = {}
	# 서버에 헤당 검색어를 포함한 동영상있는지 확인한다.
    db = youtube.objects.filter(title__contains=key)
    if Login.get_current_user(request) != -1:
        context['user_id'] = Login.get_current_user(request).user_id
    else:
        return render(request, 'login_please.html')
    user_youtube = json.loads(Login.get_current_user(request).youtube)
    if len(db) > 0:
        tmp_db = []
        for d in db:
            video_id = d.url.split('?v=')[1]
			# If user has same Youtube URL in user database, make link attached to dictation. 
			# If not make link attached to video caption download 
            if d.url in user_youtube:
                tmp_db.append(('/video/' + d.hashed_url, d.title, IMG_URL % video_id))
            else:
                tmp_db.append(('/video/add/'+video_id, d.title, IMG_URL %video_id))
        context['db'] = tmp_db
	# There are two options.
	# First extend is '0' which means don't search video with Youtube API
	# Second extend is '1' which means search video with Youtube API. You can get more results.
    if extend == '1':
        video = youtube_search(video_name=key, max_results=20)
        context['video'] = video
    return render(request, "search.html", context)
