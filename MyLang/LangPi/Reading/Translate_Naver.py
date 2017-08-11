import urllib
import urllib2

client_id = "5N9UnYJLTu4LSl3Azjzq"
client_secret = "UGN9ZT7WXg"

def translate(string, src, dst):
    if type(string) != str or type(src) != str or type(dst) != str:
        return -1
    encText = string
    encText = urllib.pathname2url(encText)
    data = "source="+src+"&target="+dst+"&text=" + encText
    url = "https://openapi.naver.com/v1/language/translate"
    request = urllib2.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib2.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        return response_body
    else:
        return -2