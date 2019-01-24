# -*- coding: utf-8 -*-
#User_urs配置项
# @Author  : joker
# @Date    : 2019-01-22

from django.conf.urls import url

from  . import  views
urlpatterns = [
    url(
        regex=r'^username/(?P<username>\w{5,20})/count/$',
        view=views.UsernameProfileView.as_view(),
        name='user_profile'
    ),
]