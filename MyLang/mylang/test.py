from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import *
import pickle
import binascii
from download_caption import *
from datetime import datetime
import time
import hashlib
import random
import smtplib
import email.utils
from email.mime.text import MIMEText
import base64

tmp_voca = voca()
tmp_voca.foreign = 'hello'
tmp_voca.korean = 'hello'
tmp_voca.save()
