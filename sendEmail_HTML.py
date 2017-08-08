# -*- encoding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
import email.utils
import json

with open('./MyLang/LangPi/Secret', 'r') as f:
    secret = json.loads(f.read())

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
    <script src="https://code.jquery.com/jquery-3.1.0.min.js"></script>
    <title>Test Page</title>
</head>
<body>
<header class="navbar-fixed-top" style="background-color: white; height: 10%; width:100%">
<div class="container-fluid" style="background-color: white">
    <div class="col-sm-12" id="menu">
        <a href="/" class="col-sm-9" style="text-decoration: none;"><h1>ML   <small>MyLang</small></h1></a>
    </div>
</div>
</header>
<div class="container col-sm-12" role="main" style="position: absolute;top: 20%">
    <div class="container" style="text-align: center">
    당신의 아이디는 무엇입니까?
    </div>
    <footer style=" width:100% background-color: lightgrey; height: 15%">
    <div class="col-sm-offset-2">
        <h2 class="col-sm-2"><a href="https://github.com/parksjin01" style="color: black; text-decoration:none;">Damotorie</a></h2>
        <div class="col-sm-10">
            <h5><a href="#" class="col-sm-12">Copyright</a></h5>
            <span class="text-center">이 페이지는 <b>***</b>개발팀에 의해 만들어진 교육용 홈페이지입니다.<br>다른 어떤 목적으로도 사용하실수 없습니다.</span>
        </div>
    </div>
</footer>
</div>
</body>
</html>
"""

msg = MIMEText(html, 'html')
msg['To'] = email.utils.formataddr(('To User', 'parksjin01@gmail.com'))
msg['From'] = email.utils.formataddr(('From Mylang Web', 'parksjin01@naver.com'))
msg['Subject'] = 'Your temporary ID and Password'
smtp = smtplib.SMTP_SSL('smtp.naver.com', 465)
smtp.ehlo()
smtp.login(secret['id'], secret['pw'])
smtp.sendmail('parksjin01@naver.com', ['parksjin01@gmail.com'], msg.as_string())
smtp.close()