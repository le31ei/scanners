#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2018/4/9 21:27
# @Author: lxflxf
# @File  : celery.py
# @Ver   : 0.1
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scanners.settings')


app = Celery('scanners')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


