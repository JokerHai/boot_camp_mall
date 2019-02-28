# -*- coding: utf-8 -*-
#购物车url配置项
# @Author  : joker
# @Date    : 2019-02-27
from django.conf.urls import url
from cart import views


urlpatterns = [
    url(
        regex=r'^cart/$',
        view= views.CartView.as_view(),
        name='cart'
    )
]

