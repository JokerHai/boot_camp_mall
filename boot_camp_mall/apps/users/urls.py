# -*- coding: utf-8 -*-
#User_urs配置项
# @Author  : joker
# @Date    : 2019-01-22

from django.conf.urls import url

from  . import  views
urlpatterns = [
    url(
        regex=r'^$',
        view=views.home,
        name='home'
    ),
]