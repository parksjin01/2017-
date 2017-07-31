# -*- encoding:utf -*-
import datetime
import cPickle
import threading
import Login
import json
import time
from .Listening.caption_util import *
from .models import youtube
from django.shortcuts import render


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