# -*- coding: utf-8 -*-
#url 配置项
# @Author  : joker
# @Date    : 2019-02-27

from django.conf.urls import url

from orders import views

urlpatterns = [

    url(
        regex=r'^orders/settlement/$',
        view= views.OrderSettlementView.as_view(),
        name='settlement'
    ),
    url(
        regex=r'^save_orders/$',
        view= views.SaveOrderView.as_view(),
        name='save_order'
    )
]