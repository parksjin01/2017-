# -*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import time
import os
import BeautifulSoup
import urllib
import hashlib
import Caption_util

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
    file_list = os.listdir('/Users/Knight/Desktop/2017 오픈소스 대회/Caption')
    if hashlib.sha256(youtube).hexdigest() in file_list:
        return '/Users/Knight/Desktop/2017 오픈소스 대회/Caption/'+hashlib.sha256(youtube).hexdigest()
    g_driver = ''
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "/Users/Knight/Desktop/2017 오픈소스 대회/Caption"}
    chrome_options.add_experimental_option("prefs",prefs)
    # html = ''
    while True:
        driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
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
    title = url_decode(title).decode('utf-8')
    print title
    flist = os.listdir('/Users/Knight/Desktop/2017 오픈소스 대회/Caption/')
    for i in flist:
        if '[DownSub.com]' in i:
            title = i
            break
    os.rename('/Users/Knight/Desktop/2017 오픈소스 대회/Caption/'+title, str('/Users/Knight/Desktop/2017 오픈소스 대회/Caption/'+hashlib.sha256(youtube).hexdigest()))
    return '/Users/Knight/Desktop/2017 오픈소스 대회/Caption/'+hashlib.sha256(youtube).hexdigest()

def caption_from_youtube(youtube):
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"download.default_directory" : "/Users/Knight/Desktop/2017 오픈소스 대회/Caption"}
    # chrome_options.add_experimental_option("prefs",prefs)
    #webdriver.support.ui.WebDriverWait()
    #driver = webdriver.Chrome('./chromedriver')
    #driver.get('https://www.youtube.com/watch?v=rUGP0d93OPA')
    #driver.execute_script("document.getElementsByClassName('yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup pause-resume-autoplay yt-uix-menu-trigger yt-uix-tooltip')[0].click()")
    #driver.execute_script("document.getElementsByClassName('yt-ui-menu-item has-icon yt-uix-menu-close-on-select action-panel-trigger action-panel-trigger-transcript')[0].click()")
    #print driver.page_source
    "Under developing"


print Caption_util.analyze(caption_from_downsub('https://youtu.be/Jmjlmn0jHbw'))[1]
# f = caption_from_downsub('https://www.youtube.com/watch?v=ah9FzeLAtbo')
# print f
# with open(f, 'r') as f:
#     print f.read()

