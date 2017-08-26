# -*- encoding: utf-8 -*-

import base64
from .models import user_info, history
from django.shortcuts import render, redirect
import hashlib
import random
import smtplib
from email.mime.text import MIMEText
import email.utils
import json
import time

#이메일로 현재 로그인한 유저판별
def get_current_user(request):
    try:
        cur_user = request.COOKIES.get('ec')
    except Exception, e:
        print e
        return -1
    try:
        user = user_info.objects.get(user_email=base64.b64decode(cur_user))
    except Exception, e:
        print e
        return -1
    return user

#로그인할때 쿠키설정
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
            print e
            message = {'error': 'Incorrect Id or Password', 'title':'ML(MyLanguage) Login'}
            return render(request, 'login.html', message)
    return render(request, 'login.html', {'title':'ML(MyLanguage) Login'})

#회원가입
def register(request):
    ctx = {'title':'회원가입'}
    if request.method == 'POST':
		#이메일 중복확인
        try:
            user_info.objects.get(user_email=request.POST.get('user_email'))
            message = {'에러': '이미 존재하는 이메일입니다.', 'title':'Error'}
            return render(request, 'register.html', message)
			
		#회원가입시 입력한 정보저장
        except Exception, e:
            print e
            create_date = str(int(time.time()))
            new_user = user_info()
            new_user.user_id = request.POST.get('user_id')
            new_user.user_pw = hashlib.md5(request.POST.get('user_pw')).hexdigest()
            new_user.user_email = request.POST.get('user_email')
            new_user.uid = hashlib.md5(new_user.user_id+new_user.user_pw+new_user.user_email+create_date).hexdigest()
            new_user.save()
            return redirect('/login/')
    return render(request, 'register.html', ctx)

#아이디/비밀번호 찾기
def find_id(request):
    ctx = {'title':"아이디/비밀번호 찾기"}
    
	###########################################
	user = get_current_user(request)
	#로그인이 되어있지않은경우 'login_please.html'로 이동
    if user == -1:
        return render(request, 'login_please.html')
    ###########################################
	
	ctx['user_id'] = user.user_id
    ctx['number'] = user.new_message
    if request.method == 'POST':
		#임시 ID/PW의 키풀
        key_pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        tmp_id = ''
        tmp_pw = ''
        try:
            with open('./LangPi/Secret', 'r') as f:
                data = f.read()
            data = json.loads(data)
            user = user_info.objects.get(user_email=request.POST.get('user_email'))
            for _ in range(10):
                tmp_id += key_pool[random.randrange(0, len(key_pool))]
                tmp_pw += key_pool[random.randrange(0, len(key_pool))]
            message = 'Your new ID: %s\nYour new Password: %s\n' % (tmp_id, tmp_pw)
			#임시 ID/PW 발급
            msg = MIMEText(message)
            msg['To'] = email.utils.formataddr(('To User', request.POST.get('user_email')))
            msg['From'] = email.utils.formataddr(('From Mylang Web', 'parksjin01@naver.com'))
            msg['Subject'] = 'Your temporary ID and Password'
            smtp = smtplib.SMTP_SSL('smtp.naver.com', 465)
            smtp.ehlo()
            smtp.login(data['id'], data['pw'])
            smtp.sendmail('parksjin01@naver.com', [request.POST.get('user_email')], msg.as_string())
            smtp.close()
            user.user_id = tmp_id
            user.user_pw = hashlib.md5(tmp_pw).hexdigest()
            user.save()
        except Exception, e:
            print e
        return redirect('/')
    return render(request, 'find-id.html', ctx)

#아이디 변경
def change_id(request):
    ctx = {'title':'아이디 변경'}
    ctx['user_id'] = get_current_user(request).user_id
    ctx['number'] = get_current_user(request).new_message
    if request.method == 'POST':
        next_id = request.POST.get('user_id')
        next_pw = hashlib.md5(request.POST.get('user_pw')).hexdigest()
        cur_email = base64.b64decode(request.COOKIES.get('ec'))
        user = user_info.objects.get(user_email=cur_email)
        user.user_id = next_id
        user.user_pw = next_pw
        user.save()
        return redirect('/')
    return render(request, 'change-id.html', ctx)

#회원탈퇴 함수
def delete(request):
    user = get_current_user(request)
    ctx = {}
    ctx['title'] = "회원탈퇴"
    ctx['user_id'] = user.user_id
	#비밀번호 맞을경우  회원정보 삭제
	#비밀번호 틀렸을경우 삭제페이지로 이동
    if request.method == "POST":
        if user.user_pw == hashlib.md5(request.POST.get('user_pw')).hexdigest():
            ctx['p'] = '2'
            ctx['content'] = '<p class="alert alert-danger" style="font-size: 2.1rem">회원탈퇴가 완료되었습니다.</p>'
            try:
                tmp_history = history.objects.get(cur_user=base64.b64encode(user.user_email))
                tmp_history.delete()
            except:
                print 'No!!!'
            user.delete()
            return render(request, 'mypage_delete.html', ctx)
        else:
            ctx['p'] = '0'
            ctx['content'] = '<p class="alert alert-danger" style="font-size: 2.1rem">비밀번호가 맞지 않아 회원탈퇴가 완료되지 않았습니다.</p>'
            return render(request, 'mypage_delete.html', ctx)
	#회원탈퇴 희망여부 재확인
    if request.GET.get('p') == '0':
        ctx['content'] = """
            <p class="alert alert-danger" style="font-size: 2.1rem">정말 회원탈퇴를 하실 건가요?</p>
            <br/>
            <br/>
            <br/>
            <a href="/" style="color:white; text-decoration:none;"><span class="btn btn-danger col-sm-offset-9 col-sm-1">아니요</span></a>
            <a href="/mypage/delete/?p=1" style="color:white; text-decoration:none;"><span class="btn btn-danger col-sm-offset-1 col-sm-1">네</span></a>
            """
        ctx['p'] = '0'
        return render(request, 'mypage_delete.html', ctx)
	#유저 확인을 위한 비밀번호 재입력
    elif request.GET.get('p') == '1':
        ctx['content1'] = """
                <p class="alert alert-danger" style="font-size: 2.1rem">비밀번호를 다시한번 입력해주세요</p>
                <br/>
                <br/>
                <br/>
                <form method="POST" action="">
                """
        ctx['content2'] = """
                <div class="form-group">
                <label class="col-sm-2 control-label">비밀번호</label>
                <div class="col-sm-3">
                <input type="password" name="user_pw" onkeyup="minimum_length()" id="user_pw" class="form-control" placeholder="Password">
                </div>
                <span id="pw_status"></span>
                </div>
                <button type="submit" class="col-sm-offset-10 col-sm-2 btn btn-danger">탈퇴</button>
                </form>
                """
        ctx['p'] = '1'
        return render(request, 'mypage_delete.html', ctx)
