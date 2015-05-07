# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, url

from foodnet.membership import views


urlpatterns = [
    url(r'profile/$', views.profile, name="profile"),
    url(r'login/$', views.log_in, name="log_in"),
    url(r'logout/$', views.log_out, name="log_out"),
]
