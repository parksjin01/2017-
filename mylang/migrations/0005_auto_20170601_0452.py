# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylang', '0004_tmp_answer_cur_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(default='')),
                ('user_pw', models.TextField(default='')),
                ('user_email', models.TextField(default='')),
            ],
        ),
        migrations.AlterField(
            model_name='tmp_answer',
            name='cur_date',
            field=models.TextField(default=''),
        ),
    ]