# -*- encoding:utf-8 -*-

from selenium import webdriver
import time
import BeautifulSoup

def translate(string, src='en', dst='ko'):
    res = []
    string = string.split('.')
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "/Users/Knight/Desktop/2017 오픈소스 대회/Caption"}
    chrome_options.add_experimental_option("prefs",prefs)
    for i in string:
        driver = webdriver.Chrome('/'.join(__file__.split('/')[:-3])+'/chromedriver')
        driver.get('http://translate.naver.com/#/'+src+'/'+dst+'/'+i.strip())
        driver.execute_script("document.getElementsByClassName('btn_translate')[0].click()")
        time.sleep(0.3)
        soup = BeautifulSoup.BeautifulSoup(driver.page_source)
        tmp = soup.find('div', attrs={'id':'transResultContentNoFuriDiv'})
        res.append(tmp.text)
        driver.quit()
    return res
