# -*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import sys
import urllib
import urllib2
import webbrowser
import platform
from selenium import webdriver
import BeautifulSoup
import time
from pyvirtualdisplay import Display

LANG = {}

def translate(string, src, dst):
    display = Display(visible=0, size=(800, 800))  
    display.start()

    if platform.system() == 'Darwin':
        path = '/Volumes/UUI/2017-/MyLang/webdriver/osx/chromedriver'
    else:
        path = '/Volumes/UUI/2017-/MyLang/webdriver/linux/chromedriver'
    driver = webdriver.Chrome(executable_path=path)
    res = []
    # print type(string), type(src), type(dst)
    if type(src) != str or type(dst) != str:
        return -1
    encText = string
    # encText = urllib.pathname2url(encText)
    data = "#"+src+"/"+dst+"/"
    url = "https://translate.google.co.kr/?hl=ko"
    new_url = url+data+encText
    # print new_url
    driver.get(new_url)
    time.sleep(1.5)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup.BeautifulSoup(html)
    soup = str(soup.findAll('span', attrs={'id':'result_box'})[0])
    soup = BeautifulSoup.BeautifulSoup(soup)
    soup = soup.findAll('span')
    for sentence in soup:
        res.append(sentence.text)
    return res[0]
