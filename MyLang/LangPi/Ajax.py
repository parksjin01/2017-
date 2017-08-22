# -*- encoding:utf-8 -*-

from .models import user_info
import random
import smtplib
from email.mime.text import MIMEText
import email.utils
from django.http import JsonResponse
import Login
from django.shortcuts import render
import json
import string

# html = """
#             %s
# """

#이메일 
def email_check_v2(request):
    data = {'is_taken': user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists()}
    key_poll = string.ascii_letters + '0123456789'
    key = ''
    for _ in range(10):
        key += key_poll[random.randrange(len(key_poll))]
    data['key'] = key
    with open('./LangPi/Secret', 'r') as f:
        secret = f.read()
    secret = json.loads(secret)
    if user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists() == True:
        message = '''<!DOCTYPE html>
<html lang="en" style="height: 100%; width: 100%">
<head>
    <meta charset="UTF-8">
    <title>Test</title>
</head>
<body style="height: 100%; width: 100%;">
<div style="background-color: #1976d2; height: 10%; width: 100%; display: table">
    <div style="display: table-cell; vertical-align: middle">
        <a href="" style="color:#fff;display:inline-block;font-size:2.1rem;padding:0; text-decoration: none">MyLang</a>
    </div>
</div>
<div style="border:thin black solid;">
        <div style="padding-top: 20px; padding-left: 15px; padding-bottom: 20px; padding-right: 15px;">아래의 이메일 인증코드를 입력해주세요<br/><br/>이메일 인증코드:<br/>['''+key+''']</div>
</div>
</body>
</html>'''
        msg = MIMEText(message, 'html')
        msg['To'] = email.utils.formataddr(('To User', request.GET.get('email')))
        msg['From'] = email.utils.formataddr(('From Mylang Web', 'parksjin01@naver.com'))
        msg['Subject'] = 'ML(MyLang) 임시 비밀번호 발급용 이메일 인증코드입니다.'
        smtp = smtplib.SMTP_SSL('smtp.naver.com', 465)
        smtp.ehlo()
        smtp.login(secret['id'], secret['pw'])
        smtp.sendmail('parksjin01@naver.com', [request.GET.get('email')], msg.as_string())
        smtp.close()
    return JsonResponse(data)

#이메일 인증코드발송 함수
def email_check(request):
    data = {'is_taken': user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists()}
	#인증코드 발송시 대소문자영어와 숫자만 사용
    key_poll = string.ascii_letters + '0123456789'
    key = ''
	#인증코드는 10자리
    for _ in range(10):
        key += key_poll[random.randrange(len(key_poll))]
    data['key'] = key
	#운영자 메일 아이디와 비밀번호
    with open('./LangPi/Secret', 'r') as f:
        secret = f.read()
    secret = json.loads(secret)
	#이메일인증시 이미 존재하는 이메일인지 확인
    if user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists() == False:
        message = '''<!DOCTYPE html>
<html lang="en" style="height: 100%; width: 100%">
<head>
    <meta charset="UTF-8">
    <title>Test</title>
</head>
<body style="height: 100%; width: 100%;">
<div style="background-color: #1976d2; height: 10%; width: 100%; display: table">
    <div style="display: table-cell; vertical-align: middle">
        <a href="" style="color:#fff;display:inline-block;font-size:2.1rem;padding:0; text-decoration: none">MyLang</a>
    </div>
</div>
<div style="border:thin black solid;">
        <div style="padding-top: 20px; padding-left: 15px; padding-bottom: 20px; padding-right: 15px;">아래의 이메일 인증코드를 입력해주세요<br/><br/>이메일 인증코드:<br/>['''+key+''']</div>
</div>
</body>
</html>'''
        msg = MIMEText(message, 'html')
        msg['To'] = email.utils.formataddr(('To User', request.GET.get('email')))
        msg['From'] = email.utils.formataddr(('From Mylang Web', 'parksjin01@naver.com'))
        msg['Subject'] = 'ML(MyLang) 이메일 인증코드입니다.'
        smtp = smtplib.SMTP_SSL('smtp.naver.com', 465)
        smtp.ehlo()
        smtp.login(secret['id'], secret['pw'])
        smtp.sendmail('parksjin01@naver.com', [request.GET.get('email')], msg.as_string())
        smtp.close()
    return JsonResponse(data)

#아이디 중복확인
def id_check(request):
    data = {'is_taken': user_info.objects.filter(user_id__iexact=request.GET.get('username')).exists()}
    return JsonResponse(data)

#단어점수 불러오기
def get_voca_score(request):
    user = Login.get_current_user(request)
	#로그인이 되어있지 않다면 login_please.html 띄우기
    if user == -1:
        return render(request, "login_please.html")
	#단어시험 최근 30개를 역순으로 출력
    voca_scores = json.loads(user.vocabulary_level)[:30][::-1]
    data = []
	#각 시험의 점수 출력
    for idx, value in enumerate(voca_scores):
        data.append({"close": value[0], "date": idx+1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)

#읽기점수 불러오기
def get_read_score(request):
    user = Login.get_current_user(request)
	#로그인이 되어있지 않다면 login_please.html 띄우기
    if user == -1:
        return render(request, "login_please.html")
	#읽기시험 최근 30개를 역순으로 출력
    read_scores = json.loads(user.readding_level)[:30][::-1]
    data = []
    # for idx in range(len(read_scores)):
    #     data.append({"close": read_scores[idx][0].strip('%'), "date": idx + 1})
	#각 시험의 점수 출력
    for idx, value in enumerate(read_scores):
        data.append({"close": value[0].strip('%'), "date": idx+1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)

#듣기점수 불러오기
def get_listening_score(request):
    user = Login.get_current_user(request)
	#로그인이 되어있지 않다면 login_please.html 띄우기
    if user == -1:
        return render(request, "login_please.html")
	#읽기시험 최근 30개를 역순으로 출력
    listen_scores = json.loads(user.listening_level)[:30][::-1]
    data = []
    # for idx in range(len(listen_scores)):
    #     data.append({"close": listen_scores[idx][0], "date": idx + 1})
	#각 시험의 점수 출력
    for idx, value in enumerate(listen_scores):
        data.append({"close": value[0], "date": idx+1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)
