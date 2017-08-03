# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class youtube(models.Model):
	url=models.URLField()
	hashed_url=models.CharField(max_length=255, null=True)
	caption=models.TextField()
	title=models.CharField(max_length=255, default="Nop!")
	date=models.DateTimeField(auto_now=True)
	description = models.TextField(default='')

class history(models.Model):
	cur = models.URLField(default='')
	recommand = models.TextField(default='')
	cur_user = models.TextField(default='')

class tmp_answer(models.Model):
	answer = models.TextField(default='')
	cur_date = models.IntegerField(default=0)
	cur_user = models.TextField(default='')

class user_info(models.Model):
	user_id = models.TextField(default='')
	user_pw = models.TextField(default='')
	user_email = models.TextField(default='')
	listening_level = models.TextField(default='''[]''')
	vocabulary_level = models.TextField(default='''[]''')
	readding_level = models.TextField(default='''[]''')
	message_box = models.TextField(default='''[]''')
	like_dislike_voca = models.TextField(default = '{"like":[], "dislike":[]}')
	extended_voca = models.TextField(default='[]')
	youtube = models.TextField(default='[]')

class voca(models.Model):
	foreign = models.TextField(default='')
	korean = models.TextField(default='')
	like = models.IntegerField(default=0)
	dislike = models.IntegerField(default=0)

class board(models.Model):
	title = models.TextField()
	text = models.TextField()
	author = models.CharField(max_length=256)
	date = models.TextField()
	comment = models.TextField()
	category = models.TextField()
