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
	category = models.CharField(max_length=10, default="1")

class history(models.Model):
	cur = models.URLField(default='')
	recommand = models.TextField(default='')

class tmp_answer(models.Model):
	answer = models.TextField(default='')
	cur_date = models.TextField(default='')

class user_info(models.Model):
	user_id = models.TextField(default='')
	user_pw = models.TextField(default='')
	user_email = models.TextField(default='')
