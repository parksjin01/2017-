# -*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import BeautifulSoup
import hashlib
import urllib2
import urllib
import json

URL1 = 'http://downsub.com/?url='
URL2 = 'http://downsub.com'
country = {'en':'English', 'ja':'Japan', 'ko':'Korea'}

def title(url):
    id = url.split('?v=')[1]
    html = urllib2.urlopen('https://www.googleapis.com/youtube/v3/videos?part=snippet&id=%s&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s' %id).read()
    html = html.split('\n')
    new_html = []
    for sentence in html:
        if "etag" not in sentence:
            new_html.append(sentence)
    html = json.loads('\n'.join(new_html))
    return [html['items'][0]['snippet']['title'], html['items'][0]['snippet']['description']]


def url_decode(url):
    i = 0
    res = ''
    while i < len(url):
        if url[i] == '%':
            res += '-'
            i += 3
        elif url[i] == '+':
            res += ' '
            i += 1
        else:
            res += url[i]
            i += 1
    return res

# print caption_from_downsub('https://www.youtube.com/watch?v=zHZ6bNvzzJ4')

def caption_from_downsub(youtube, lang='en'):
    if len(lang) == 2:
        lang = country[lang]
    request = urllib2.Request(URL1+urllib.quote_plus(youtube))
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    html = urllib2.urlopen(request).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    tags = str(soup.findAll('div', attrs={'id':'show'})[0])
    tags = tags.split('<br />')
    href = ''
    for line in tags:
        if lang in line:
            soup = BeautifulSoup.BeautifulSoup(line)
            a = soup.findAll('a')[0]
            href = a['href']
            break
    print href
    request = urllib2.Request(URL2+href)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    html = urllib2.urlopen(request).read()
    return html, str(hashlib.sha256(youtube).hexdigest())