#-*-coding:utf-8-*-
import os
import sys

os.environ['DJANGO_SETTINGS_MOULE']='expertRecommendation.settings'
app_path='/home/xiaohe/expertRecommendation/expertRecommendation/'
sys.path.append(app_path)
os.chdir(app_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","expertRecommendation.settings")
import django.core.handlers.wsgi
application=django.core.handlers.wsgi.WSGIHandler()

