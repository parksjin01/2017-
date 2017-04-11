import Translate_Google_without_API
import Translate_Naver
import BeautifulSoup
import urllib2

def Translate(string, src, dst, select):
    if select == "Google":
        result = Translate_Google_without_API.translate(string, src, dst)
    elif select == "Naver":
        result = Translate_Naver.translate(string, src, dst)
    return result

def Translate_from_URL(url, src, dst, select = "Google"):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    res = []
    if 'cnn' in url:
        div = soup.findAll('div', attrs={'id':'storytext'})
        # print div
        soup = BeautifulSoup.BeautifulSoup(str(div))
        div = soup.findAll('p')
        for txt in div:
            res.append(txt.text)
    print Translate(str('\n'.join(res)), src, dst, select)
