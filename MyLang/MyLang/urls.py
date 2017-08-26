"""MyLang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from LangPi.views import *

urlpatterns = [
    url('^$', home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login, name='login'),
    url(r'^find-id/$', find_id, name='find_id'),
    url(r'^change-id/', change_id, name='change_id'),
    url(r'^register/$',register, name='register'),
    url(r'^search/', search, name='search'),
    url(r'^video/add/$', add_video, name='add_video'),
    url(r'^video/add/(?P<url>[0-9a-zA-Z_\-+=]+)/$', adder, name='adder'),
    url(r'^video/(?P<name>[0-9a-zA-Z]+)/$', dictation, name='show'),
    url(r'^video/$', video_list, name='show_list'),
    url(r'^read/$', reading, name='reading'),
    url(r'^mypage/$', mypage, name='mypage'),
    url(r'^vocabulary/$', voca_exam, name='vocabulary'),
    # url(r'test/$', test, name='test'),
    # url(r'process/$', process, name='process'),
    url(r'^mypage/listening/$', mypage_listening, name='mypage_listening'),
    url(r'^mypage/reading/$', mypage_reading, name='mypage_reading'),
    url(r'^mypage/vocabulary/$', mypage_vocabulary, name='mypage_vocabulary'),
    url(r'mypage/likedislike/$', mypage_likedislike, name='mypage_likedislike'),
    url(r'^mypage/message/$', mypage_message, name='mypage_message'),
    url(r'^mypage/board/$', mypage_board, name='mypage_board'),
    url(r'mypage/delete/', delete, name='mypage_delete'),
    url(r'get_voca_score/$', get_voca_score, name='get_voca_score'),
    url(r'get_read_score/$', get_read_score, name='get_read_score'),
    url(r'get_listen_score/$', get_listen_score, name='get_listen_score'),
    url(r'register/ajax/validate_username/', id_check, name="id_check"),
    url(r'register/ajax/validate_mail/', email_check, name="email_check"),
    url(r'find-id/ajax/validate_mail/', email_check_v2, name="email_check_v2"),
    url(r'add/vocabulary/', add_voca, name="add_voca"),
    url(r'board/edit', edit, name='edit'),
    url(r'board/show', show_memo, name='show_menu'),
    url(r'board/write', write, name='write'),
    url(r'board/', bullet_board, name='board'),
    url(r'add/comment', add_memo_comment),
    url(r'memo/delete', delete_reply),
    url(r'memo/alert', alert_reply),
    url(r'memo/recommand', memo_recommand),
    url(r'memo/reply/recommand', memo_reply_recommand),
]
