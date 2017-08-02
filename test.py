import urllib2
import urllib
import BeautifulSoup

URL1 = 'http://downsub.com/?url='
URL2 = 'http://downsub.com'
country = {'en':'English', 'ja':'Japan', 'ko':'Korea'}

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
    print html

caption_from_downsub('https://www.youtube.com/watch?v=n3kNlFMXslo')