from django.conf import settings
from django.test import Client
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'MyLang.settings'
#
settings.configure()

c = Client()
response = c.get('/')
print response.status_code
response = c.post('/login/', {'user_id':'test', 'user_pw':'testing'})
print response.status_code