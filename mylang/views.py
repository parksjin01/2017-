# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .Listening.caption_util import *
from .reading import *
import pickle
import binascii
from download_caption import *
from datetime import datetime
import time
# Create your views here.

def adder(request, url):
	if 'http' not in url:
		url = 'https://www.youtube.com/watch?v='+url
	print url
	try:
                tube = youtube.objects.get(url=url)
        except Exception, e:
		print e
                tube = youtube()
                titles = title(url)
                while True:
                    try:
                         content, hashed_url = caption_from_downsub(url)
                         break
                    except:
                         continue
                tube.title = titles[str('title')]
                tube.category = titles[str('categoryId')]
                tube.url = url
                tube.hashed_url = hashed_url
                tube.caption = content
                tube.save()	
	return redirect('/video/')
def recommandation(url, num, cur):
    video_id = url.split('?v=')[1]
    html = urllib2.urlopen('https://www.googleapis.com/youtube/v3/search?part=id&maxResults=%d&order=relevance&relatedToVideoId=%s&type=video&videoCaption=closedCaption&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s' %(num, video_id))
    html = html.read().split('\n')
    res = []
    fmt = '''<td><a href='video/add/%s'"><img src=%s/><span>%s</span></td>'''
    for sentence in html:
        if 'videoId' in sentence:
            related_video = sentence.split(': ')[1][:-1].strip('"')
            related_video = 'https://www.youtube.com/watch?v='+related_video
            titles = title(related_video)[str('title')]
            img = 'https://i.ytimg.com/vi/%s/hqdefault.jpg?custom=true&w=336&h=188&stc=true&jpg444=true&jpgq=90&sp=68&sigh=w6tAuAmF905_ShQMYGlSjCnkNgI' %(related_video.split('?v=')[1]) 
            res.append(fmt %(related_video.split('?v=')[1], img, titles))
    if cur == []:
        return res
    else:
        return res + cur[num:]

def home(request):
	message = {}
	if request.method == 'POST':
		print 1
		print request
	try:
	    h = history.objects.all()[0]
	    recommand = pickle.loads(h.recommand)
	    message['recommand'] = recommand	
	finally:
	    return render(request, 'home.html', message)

def show(request, name):
	if request.method == 'POST':
		cur_date = request.COOKIES.get('youan')
		tmp = tmp_answer.objects.get(cur_date=cur_date)
		answer = tmp.answer
		answer = pickle.loads(binascii.unhexlify(answer))
		print answer
		user=request.POST.getlist('blank')
		print user
		score=check_answer(user, answer)
		print score
		message = {
	'video':'<iframe width="560" height="315" src="https://www.youtube.com/embed/vNOllWX-2aE" frameborder="0"></iframe>',
	}

		message['score']=score
		tmp.delete()
		return render(request, 'dictation.html', message)
	tube=get_object_or_404(youtube, hashed_url=name)
	try:
	    his = history.objects.all()[0]
	except:
	    his = history()
	tube.date = datetime.now()
	tube.save()
	url = tube.url.split('?v=')[1]
	his.cur = tube.url
	if his.recommand == '':
		recommand = recommandation(his.cur, 20, [])
		his.recommand = pickle.dumps(recommand)
	else:
		recommand = pickle.loads(his.recommand)
		recommand = recommandation(his.cur, 5, recommand)
		his.recommand = pickle.dumps(recommand)
	his.save()
	caption = tube.caption
	question, answer = analyze(caption)
	question = question.replace('\n', '</br>')
	answer = binascii.hexlify(pickle.dumps(answer))
	tmp = tmp_answer()
	tmp.answer = answer
	cur_date = int(time.time())
	tmp.cur_date = cur_date
	tmp.save()
	message = {
'video':'<iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0"></iframe>' %url,
'form':'<div><h1>Dictation</h1><p name=dictation>%s</p></div><button type="submit">Check</button>' %question,
}

	#return HttpResponse('\n'.join(message))
	http = render(request, 'dictation.html', message)
	http.set_cookie(key="youan", value=cur_date)
	return http

def show_list(request):
	tube = youtube.objects.order_by('-date').all()
	message = ['<a href="/video/add"><input type=button value="Add"></input></a>']
	fmt = '''
<div>
<a align=left href="%s"><div align=left><img width=300 height=150 src=https://i.ytimg.com/vi/%s/hqdefault.jpg?custom=true&w=336&h=188&stc=true&jpg444=true&jpgq=90&sp=68&sigh=w6tAuAmF905_ShQMYGlSjCnkNgI/> <h2 align=left>%s</h2></div></a>
</br>
</br>
</div>
'''
	for idx in tube:
		message.append(fmt %(idx.hashed_url, idx.url.split('?v=')[1], idx.title))
	return HttpResponse('\n'.join(message))		

def reading(request):
	if request.method == 'POST':
		score = read(request.POST.get('foreign'), request.POST.get('kor'))
		ctx = {'score':score, 'fore':request.POST.get('foreign'), 'kor':request.POST.get('kor'), 'test':request.POST.get('test')}
		return render(request, 'reading.html', ctx)
		
	return render(request, 'reading.html')

def add_video(request):
	if request.method == 'POST':
	    url = request.POST.get('url')
	    adder(request, url)
	else:
	    return render(request, 'add_video.html')

def login(request):
	return render(request, 'login.html')

def register(request):
	return render(request, 'register.html')


