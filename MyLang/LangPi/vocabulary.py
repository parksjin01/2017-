# -*- encoding: utf-8 -*-

import urllib2
import json
import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def c2de(word):
    request = urllib2.Request('http://dedic.naver.com/search.nhn?range=all&q=%s' %word)
    html = urllib2.urlopen(request).read()
    word = BeautifulSoup.BeautifulSoup(html).findAll('span', attrs={'class':'gma'})[0].text
    return word

def c2la(word):
    request = urllib2.Request('http://ladic.naver.com/api/la/search.nhn?&query=%s&dictName=alldict&lh=true' %word)
    result = json.loads(urllib2.urlopen(request).read())['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2ru(word):
    request = urllib2.Request('http://rudic.naver.com/api/ru/search.nhn?&query=%s&dictName=alldict&lh=true' % word)
    request.add_header('user-agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    if result['exactMatcheEntryUrl'] == "false":
        url = result['searchResult']['searchEntryList']['items'][0]['entryId']
    else:
        url = result['exactMatcheEntryUrl'].split('/')[-1]
    url = "http://rudic.naver.com/api/ru/entry.nhn?entryId=%s&meanType=default&groupConjugation=false" % url
    request = urllib2.Request(url)
    request.add_header('user-agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2mn(word):
    request = urllib2.Request('http://mndic.naver.com/api/mn/search.nhn?&query=%s&dictName=alldict&lh=true' % word)
    request.add_header('user-agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    if result['exactMatcheEntryUrl'] == "false":
        url = result['searchResult']['searchEntryList']['items'][0]['entryId']
    else:
        url = result['exactMatcheEntryUrl'].split('/')[-1]
    url = "http://mndic.naver.com/api/mn/entry.nhn?entryId=%s&meanType=default&groupConjugation=false" % url
    request = urllib2.Request(url)
    request.add_header('user-agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2vi(word):
    request = urllib2.Request('http://vndic.naver.com/api/vn/search.nhn?&query=%s&dictName=alldict&lh=true' %word)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    if result['exactMatcheEntryUrl'] == "false":
        url = result['searchResult']['searchEntryList']['items'][0]['entryId']
    else:
        url = result['exactMatcheEntryUrl'].split('/')[-1]
    url = "http://vndic.naver.com/api/vn/entry.nhn?entryId=%s&meanType=default&groupConjugation=false" %url
    request = urllib2.Request(url)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2sv(word):
    request = urllib2.Request('http://svdic.naver.com/api/sv/search.nhn?&query=%s&dictName=alldict&lh=true' %word)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    if result['exactMatcheEntryUrl'] == "false":
        url = result['searchResult']['searchEntryList']['items'][0]['entryId']
    else:
        url = result['exactMatcheEntryUrl'].split('/')[-1]
    url = "http://svdic.naver.com/api/sv/entry.nhn?entryId=%s&meanType=default&groupConjugation=false" %url
    request = urllib2.Request(url)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2es(word):
    request = urllib2.Request('http://spdic.naver.com/krEntry.nhn?entryNO=1014026&query=%s' % word)
    html = urllib2.urlopen(request).read()
    word = BeautifulSoup.BeautifulSoup(html).findAll('span', attrs={'class': 'autolink'})[0].text
    return word

def c2ja(word):
    request = urllib2.Request('http://jpdic.naver.com/search.nhn?dic_where=jpdic&query=%s' %word)
    html = urllib2.urlopen(request).read()
    tag = BeautifulSoup.BeautifulSoup(html).findAll('ruby')[0]
    return tag.text

def c2zh(word):
    request = urllib2.Request('http://cndic.naver.com/search/all?q=%s' %word)
    html = urllib2.urlopen(request).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    div_tag = soup.findAll('div', attrs={'class':'word_result '})[0]
    soup = BeautifulSoup.BeautifulSoup(str(div_tag))
    span_tag = soup.findAll('span', attrs={'class':'sc'})[1]
    result = span_tag.text
    return result.split('。')[0]

def c2it(word):
    request = urllib2.Request('http://itdic.naver.com/api/it/search.nhn?&query=%s&dictName=alldict&lh=true' %word)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    if result['exactMatcheEntryUrl'] == "false":
        url = result['searchResult']['searchEntryList']['items'][0]['entryId']
    else:
        url = result['exactMatcheEntryUrl'].split('/')[-1]
    url = "http://itdic.naver.com/api/it/entry.nhn?entryId=%s&meanType=default&groupConjugation=false" %url
    request = urllib2.Request(url)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2cs(word):
    request = urllib2.Request('http://csdic.naver.com/api/cs/search.nhn?&query=%s&dictName=alldict&lh=true' %word)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2th(word):
    request = urllib2.Request('http://thdic.naver.com/api/th/search.nhn?&query=%s&dictName=alldict&lh=true' %word)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    if result['exactMatcheEntryUrl'] == "false":
        url = result['searchResult']['searchEntryList']['items'][0]['entryId']
    else:
        url = result['exactMatcheEntryUrl'].split('/')[-1]
    url = "http://thdic.naver.com/api/th/entry.nhn?entryId=%s&meanType=default&groupConjugation=false" %url
    request = urllib2.Request(url)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2pt(word):
    request = urllib2.Request('http://ptdic.naver.com/api/pt/search.nhn?&query=%s&dictName=alldict&lh=true' %word)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    if result['exactMatcheEntryUrl'] == "false":
        url = result['searchResult']['searchEntryList']['items'][0]['entryId']
    else:
        url = result['exactMatcheEntryUrl'].split('/')[-1]
    url = "http://ptdic.naver.com/api/pt/entry.nhn?entryId=%s&meanType=default&groupConjugation=false" %url
    request = urllib2.Request(url)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def c2fr(word):
    request = urllib2.Request('http://frdic.naver.com/search.nhn?q=%s' %word)
    html = urllib2.urlopen(request).read()
    word = BeautifulSoup.BeautifulSoup(html).findAll('span', attrs={'class':'fra'})[0].text
    return word

def c2hi(word):
    request = urllib2.Request('http://hidic.naver.com/api/hi/search.nhn?&query=%s&dictName=alldict&lh=true' %word)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    if result['exactMatcheEntryUrl'] == "false":
        url = result['searchResult']['searchEntryList']['items'][0]['entryId']
    else:
        url = result['exactMatcheEntryUrl'].split('/')[-1]
    url = "http://hidic.naver.com/api/hi/entry.nhn?entryId=%s&meanType=default&groupConjugation=false" %url
    request = urllib2.Request(url)
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    result = json.loads(urllib2.urlopen(request).read())
    result = result['searchResult']['searchMeanList']['items'][0]
    return result['entry']

def change(word, lang):
    if lang == 'de':
        return c2de(word)
    elif lang == 'la':
        return c2la(word)
    elif lang == 'ru':
        return c2ru(word)
    elif lang == 'mn':
        return c2mn(word)
    elif lang == 'vi':
        return c2vi(word)
    elif lang == 'sv':
        return c2sv(word)
    elif lang == 'es':
        return c2es(word)
    elif lang == 'ja':
        return c2ja(word)
    elif lang == 'zh':
        return c2zh(word)
    elif lang == 'it':
        return c2it(word)
    elif lang == 'cs':
        return c2cs(word)
    elif lang == 'th':
        return c2th(word)
    elif lang == 'pt':
        return c2pt(word)
    elif lang == 'fr':
        return c2fr(word)
    elif lang == 'hi':
        return c2hi(word)