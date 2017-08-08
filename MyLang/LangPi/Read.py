from django.shortcuts import render
from .reading import *
import Login
import time
import json

def reading(request):
    if request.method == 'POST':
        if len(request.POST.get('foreign')) >= 5000:
            ctx = {'title':'ML(MyLang) Reading', 'error':'1'}
            return render(request, 'reading.html', ctx)
        score = read(request.POST.get('foreign'), request.POST.get('kor'), request.POST.get('category'))
        if score[0] == u'-':
            score = u'0%'
        user = Login.get_current_user(request)
        if user == -1:
            return render(request, "login_please.html")
        reading = [[score, time.time()]] + json.loads(str(user.readding_level))
        user.readding_level = json.dumps(reading)
        user.save()
        ctx = {'score': score, 'fore': request.POST.get('foreign'), 'kor': request.POST.get('kor'),
               'test': request.POST.get('test'), 'title':'ML(MyLang) Reading', 'error':'0'}
        return render(request, 'reading.html', ctx)
    ctx = {'title':'ML(MyLang)', 'error':'0'}
    if Login.get_current_user(request) != -1:
        ctx['user_id'] = Login.get_current_user(request).user_id
    else:
        return render(request, 'login_please.html')
    return render(request, 'reading.html', ctx)