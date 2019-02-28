# -*- coding: utf-8 -*-
#路由配置
# @Author  : joker
# @Date    : 2019-02-26
from django.conf.urls import url

from  goods import views

urlpatterns = [
    url(
        regex=r'^categories/(?P<category_id>\d+)/skus/$',
        view= views.SKUListView.as_view(),
        name='sku_list'
    ),
]
