# -*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import time
import os
import BeautifulSoup
import hashlib
from pyvirtualdisplay import Display
import urllib2
import json

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

def caption_from_downsub(youtube):
    display = Display(visible=0, size=(800, 800))
    display.start()
    file_path = '/home/knight/MyLang/mylang'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : file_path}
    chrome_options.add_experimental_option("prefs",prefs)
    # html = ''
    while True:
        driver = webdriver.Chrome(executable_path='../chromedriver', chrome_options=chrome_options)
        driver.get('http://downsub.com/?url='+youtube)
        html = driver.page_source
        if 'div' in html:
            g_driver = driver
            break
        driver.close()
        driver.quit()
    soup = BeautifulSoup.BeautifulSoup(html)
    tag = soup.findAll('div', attrs={'id':'show'})
    tag = str(tag)
    tag = tag.split('<br />')[:-1]
    for tmp_tag in tag:
        if 'English' in tmp_tag:
	    soup = BeautifulSoup.BeautifulSoup(tmp_tag)
	    a = soup.findAll('a')[0]
            driver = g_driver
            driver.get('http://downsub.com/'+a['href'])
            time.sleep(5)
            driver.close()
            driver.quit()
            break
    flist = os.listdir(file_path)
    for i in flist:
        if '[DownSub.com]' in i:
            title = i
            break
    with open(title, 'r') as f:
        data = f.read()
    os.remove(title)
    return data, str(hashlib.sha256(youtube).hexdigest())