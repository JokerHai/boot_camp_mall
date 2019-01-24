# -*- coding: utf-8 -*-
#项目首页
# @Author  : joker
# @Date    : 2019-01-24

from  django.conf.urls import url


from . import  views

urlpatterns = [
    url(
        regex=r'^$',
        view =views.home,
        name ='home'
    )
]
