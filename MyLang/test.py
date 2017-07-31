import urllib2

a = urllib2.urlopen('https://translate.google.co.kr/#en/ko/byebye').read()
print a