# -*- encoding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
import email.utils
import json

with open('./MyLang/LangPi/Secret', 'r') as f:
    secret = json.loads(f.read())

html = """<!DOCTYPE html>
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
       <div style="padding-top: 20px; padding-left: 15px; padding-bottom: 20px; padding-right: 15px;">아래의 이메일 인증코드를 입력해주세요<br/><br/>이메일 인증코드:<br/>[*6HMTwfSwg]</div>
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
smtp.sendmail('parksjin01@naver.com', ['parksjin01@naver.com'], msg.as_string())
smtp.close()