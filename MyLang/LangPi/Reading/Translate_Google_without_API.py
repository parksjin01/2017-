# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import urllib
import time
import json

__all__ = ["get_tk"]

import sys
from datetime import datetime


_ENCODING = "UTF-8"


# Helper functions
def _mb_strlen(string):
    """Get the length of the encoded string."""
    return len(string.decode(_ENCODING))


def _mb_substr(string, start, length):
    """Get substring from the encoded string."""
    return string.decode(_ENCODING)[start: start + length]

##################################################


def _shr32(x, bits):
    if bits <= 0:
        return x

    if bits >= 32:
        return 0

    x_bin = bin(x)[2:]
    x_bin_length = len(x_bin)

    if x_bin_length > 32:
        x_bin = x_bin[x_bin_length - 32: x_bin_length]

    if x_bin_length < 32:
        x_bin = x_bin.zfill(32)

    return int(x_bin[:32 - bits].zfill(32), 2)


def _char_code_at(string, index):
    return ord(_mb_substr(string, index, 1))


#OLD Function
def _generateB():
    start = datetime(1970, 1, 1)
    now = datetime.now()

    diff = now - start

    return int(diff.total_seconds() / 3600)


def _TKK():
    """Replacement for _generateB function."""
    return [406604, 1836941114]


def _RL(a, b):
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]

        if d >= 'a':
            d = _char_code_at(d, 0) - 87
        else:
            d = int(d)

        if b[c + 1] == '+':
            d = _shr32(a, d)
        else:
            d = a << d

        if b[c] == '+':
            a = a + d & (pow(2, 32) - 1)
        else:
            a = a ^ d

    return a


def _TL(a):
    #b = _generateB()
    tkk = _TKK()
    b = tkk[0]

    d = []

    for f in range(0, _mb_strlen(a)):
        g = _char_code_at(a, f)

        if g < 128:
            d.append(g)
        else:
            if g < 2048:
                d.append(g >> 6 | 192)
            else:
                if ((g & 0xfc00) == 0xd800 and
                        f + 1 < _mb_strlen(a) and
                        (_char_code_at(a, f + 1) & 0xfc00) == 0xdc00):

                    f += 1
                    g = 0x10000 + ((g & 0x3ff) << 10) + (_char_code_at(a, f) & 0x3ff)

                    d.append(g >> 18 | 240)
                    d.append(g >> 12 & 63 | 128)
                else:
                    d.append(g >> 12 | 224)
                    d.append(g >> 6 & 63 | 128)

            d.append(g & 63 | 128)

    a = b

    for e in range(0, len(d)):
        a += d[e]
        a = _RL(a, "+-a^+6")

    a = _RL(a, "+-3^+b+-f")

    a = a ^ tkk[1]

    if a < 0:
        a = (a & (pow(2, 31) - 1)) + pow(2, 31)

    a %= pow(10, 6)

    return "%d.%d" % (a, a ^ b)


def get_tk(word):
    """Returns the tk parameter for the given word."""
    if isinstance(word, unicode):
        word = word.encode(_ENCODING)

    return _TL(word)

def translate(string, src, dst):
    tk = get_tk(string)

    request = urllib2.Request("https://translate.google.co.kr/translate_a/single?client=t&sl=%s&tl=%s&hl=ko&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk=%s&q=%s" %(src, dst, tk, urllib.quote_plus(string.encode('utf-8'))))
    request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')

    result = json.loads(urllib2.urlopen(request).read())[0][0][0]
    time.sleep(3)
    return result
