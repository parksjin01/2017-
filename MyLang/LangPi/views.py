# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import Login
import Ajax
import Listen
import Read
import Voca
import Util

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

def youtube_search(video_id=0, video_name='', max_results=5):
    return Listen.youtube_search(video_id, video_name, max_results)

# Parameter
# ->url: 추가하려는 유튜브의 url
def adder(request, url):
    return Listen.adder(request, url)

def recommandation(url, num, cur):
    return Util.recommandation(url, num, cur)

def home(request):
    return Util.home(request)

def bullet_board(request):
    return Util.bullet_board(request)

def show_memo(request):
    return Util.show_memo(request)

def edit(request):
    return Util.edit(request)

def write(request):
    return Util.write(request)

def dictation(request, name):
    return Listen.dictation(request, name)

def video_list(request):
    return Listen.video_list(request)

def add_video(request):
    return Listen.add_video(request)

def reading(request):
    return Read.reading(request)

def search(request):
    return Listen.search(request)

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

def mypage_board(request):
    return Util.mypage_board(request)

def voca_exam(request):
    return Voca.voca_exam(request)

def add_voca(request):
    return Voca.add_voca(request)

def delete(request):
    return Login.delete(request)