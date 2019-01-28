# -*- coding: utf-8 -*-
#oauth_url 配置
# @Author  : joker
# @Date    : 2019-01-28
from django.conf.urls import url
from oauth import views

urlpatterns = [
    url(
        regex=r'^qq/authorization/$',
        view = views.QQAuthURLView.as_view()
    ),
]
