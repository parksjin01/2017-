from django.shortcuts import render
from .reading import *
import Login
import time
import json

def reading(request):
    if request.method == 'POST':
        # 5000 is maximum length for text, Google translator can't translate more than 5000 words
        if len(request.POST.get('foreign')) >= 5000:
            ctx = {'title':'ML(MyLang) Reading', 'error':'1'}
            return render(request, 'reading.html', ctx)
        # read is compare function.
        # parameter: foreign text, korean text and foreign text language code(ex, english is en)
        # return: similarity between foreign text and korean text
        score = read(request.POST.get('foreign'), request.POST.get('kor'), request.POST.get('category'))
        # It sometimes return -15% (because I used log function to get similarity) but similarity can't be negative
        # So change it to 0%
        if score[0] == u'-':
            score = u'0%'
        user = Login.get_current_user(request)
        if user == -1:
            return render(request, "login_please.html")
        # Add reading score. This score can be used for drawing graph
        reading = [[score, time.time()]] + json.loads(str(user.readding_level))
        user.readding_level = json.dumps(reading)
        user.save()
        ctx = {'score': score, 'fore': request.POST.get('foreign'), 'kor': request.POST.get('kor'),
               'test': request.POST.get('test'), 'title':'ML(MyLang) Reading', 'error':'0', 'user_id':Login.get_current_user(request).user_id}
        ctx['number'] = Login.get_current_user(request).new_message
        return render(request, 'reading.html', ctx)
    ctx = {'title':'ML(MyLang)', 'error':'0'}
    if Login.get_current_user(request) != -1:
        ctx['user_id'] = Login.get_current_user(request).user_id
        ctx['number'] = Login.get_current_user(request).new_message
    else:
        return render(request, 'login_please.html')
    return render(request, 'reading.html', ctx)