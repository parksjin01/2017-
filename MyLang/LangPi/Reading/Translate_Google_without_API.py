# -*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests

LANG = {}

def translate(string, src, dst):
    sentence_eng = string
    sentence_eng.replace(u' ', u'+')
    dataset = {'sl': 'en', 'tl': 'ko', 'p': '2'}  # for now, set on English to Korean
    req_url = "http://www.tastemylife.com/gtr.php?sl={0}&tl={1}&p={2}&q=".format(src, dst,
                                                                                 dataset['p'])
    req_url = req_url + sentence_eng
    req = requests.get(req_url)
    req_json = req.json()
    return(req_json['result'])
