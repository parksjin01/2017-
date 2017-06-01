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

def title(url):
    id = url.split('?v=')[1]
    html = urllib2.urlopen('https://www.googleapis.com/youtube/v3/videos?part=snippet&id=%s&key=AIzaSyBf5cfsWLkaCmGPr4jtmyzeX2W0uSmvO1s' %id)
    html = html.read().split('\n')
    res = {}
    for sentence in html:
        if 'title' in sentence:
            k, v = sentence.strip(' ').split(': ')[0], sentence.strip(' ').split(': ')[1:]
            res[k.strip('"')] = (': '.join(v)).strip('",').strip('"')
        elif 'category' in sentence:
            k, v = sentence.strip(' ').split(': ')[0], sentence.strip(' ').split(': ')[1:]
            res[k.strip('"')] = (': '.join(v)).strip('",').strip('"')
            break

    return res

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
    file_path = '/'.join(__file__.split('/')[:-1])+'/'
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
    soup = BeautifulSoup.BeautifulSoup(tag)
    tag = soup.findAll('a')
    for tmp_tag in tag:
        if tmp_tag['href'][-2:] == 'en':
            driver = g_driver
            url = 'http://downsub.com/'+tmp_tag['href']
            title_s = url.find('title=')+len('title=')
            title_e = url.find('&url=')
            title = url[title_s:title_e]
            driver.get('http://downsub.com/'+tmp_tag['href'])
            time.sleep(5)
            driver.close()
            driver.quit()
            break
    flist = os.listdir(file_path)
    for i in flist:
        if '[DownSub.com]' in i:
            title = i
            break
    with open(file_path+title, 'r') as f:
        data = f.read()
    os.remove(file_path+title)
    return data, str(hashlib.sha256(youtube).hexdigest())

