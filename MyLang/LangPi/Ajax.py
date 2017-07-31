from .models import user_info
import random
import smtplib
from email.mime.text import MIMEText
import email.utils
from django.http import JsonResponse
import Login
import pickle
from django.shortcuts import render

def email_check_v2(request):
    data = {'is_taken': user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists()}
    key = ''
    for i in range(10):
        key += chr(random.randrange(0x21, 0x7f))
    data['key'] = key
    if user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists() == True:
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

def email_check(request):
    data = {'is_taken': user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists()}
    key = ''
    for i in range(10):
        key += chr(random.randrange(0x21, 0x7f))
    data['key'] = key
    if user_info.objects.filter(user_email__iexact=request.GET.get('email')).exists() == False:
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
    data = {'is_taken': user_info.objects.filter(user_id__iexact=request.GET.get('username')).exists()}
    return JsonResponse(data)

def get_voca_score(request):
    user = Login.get_current_user(request)
    if user == -1:
        return render(request, "login_please.html")
    voca_scores = pickle.loads(user.vocabulary_level)[:30][::-1]
    data = []
    for idx in range(len(voca_scores)):
        data.append({"close": voca_scores[idx].score, "date": idx + 1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)

def get_read_score(request):
    user = Login.get_current_user(request)
    if user == -1:
        return render(request, "login_please.html")
    read_scores = pickle.loads(user.readding_level)[:30][::-1]
    data = []
    for idx in range(len(read_scores)):
        data.append({"close": read_scores[idx].score.strip('%'), "date": idx + 1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)

def get_listening_score(request):
    user = Login.get_current_user(request)
    if user == -1:
        return render(request, "login_please.html")
    listen_scores = pickle.loads(user.listening_level)[:30][::-1]
    data = []
    for idx in range(len(listen_scores)):
        data.append({"close": listen_scores[idx].score, "date": idx + 1})
    # data = data[::-1]
    return JsonResponse(data, safe=False)