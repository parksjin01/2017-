# -*- encoding:utf-8 -*-

from MyLang.LangPi import vocabulary, Ajax, download_caption,Listen, Login, Read, reading, Util, Voca
from MyLang.LangPi.Reading import DOC_comp, Translate_Google_without_API
from MyLang.LangPi.Listening import caption_util
from django.http import HttpRequest

vocabulary.change('안녕하세요', 'de')
vocabulary.change('안녕하세요', 'la')
vocabulary.change('안녕하세요', 'ru')
vocabulary.change('안녕하세요', 'mn')
vocabulary.change('안녕하세요', 'vi')
vocabulary.change('안녕하세요', 'sv')
vocabulary.change('안녕하세요', 'es')
vocabulary.change('안녕하세요', 'ja')
vocabulary.change('안녕하세요', 'zh')
vocabulary.change('안녕하세요', 'it')
vocabulary.change('안녕하세요', 'cs')
vocabulary.change('안녕하세요', 'th')
vocabulary.change('안녕하세요', 'pt')
vocabulary.change('안녕하세요', 'fr')
vocabulary.change('안녕하세요', 'hi')
print 'Stage 1 cleared'

request = HttpRequest.se

# Ajax.
print 'Stage 2 cleared'

download_caption.title('https://www.youtube.com/watch?v=4-O-wWuTvKY')
download_caption.caption_from_downsub('https://www.youtube.com/watch?v=4-O-wWuTvKY')

print 'Stage 3 cleared'

Listen.youtube_search(video_name='ted')

print 'Stage 4 cleared'

reading.read('hello', '안녕하세요')

