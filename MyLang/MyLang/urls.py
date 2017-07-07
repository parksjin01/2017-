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
from mylang.views import *
urlpatterns = [
    url('^$', home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login, name='login'),
    url(r'^find-id/', find_id, name='find_id'),
    url(r'^change-id/', change_id, name='change_id'),
    url(r'^register/',register, name='register'),
    url(r'^search/', search, name='search'),
    url(r'^video/add/$', add_video, name='add_video'),
    url(r'^video/add/(?P<url>[0-9a-zA-Z_\-+=]+)/$', adder, name='adder'),
    url(r'^video/(?P<name>[0-9a-zA-Z]+)/$', show, name='show'),
    url(r'^video/$', show_list, name='show_list'),
    url(r'^read/$', reading, name='reading'),
    url(r'^mypage/$', mypage, name='mypage'),
    url(r'^vocabulary/$', vocabulary, name='vocabulary'),
]
