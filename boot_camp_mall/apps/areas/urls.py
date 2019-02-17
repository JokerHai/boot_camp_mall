# -*- coding: utf-8 -*-
#areas_url配置项
# @Author  : joker
# @Date    : 2019-02-16
from django.conf.urls import url

from . import views

urlpatterns = [
        # url(
        #     regex=r'^areas/$',
        #     view =views.AreasView.as_view(),
        #     name ='areas'
        # ),
        # url(
        #     regex=r'^areas/(?P<pk>\d+)/$',
        #     view =views.SubAreasView.as_view(),
        #     name ='sub_areas'
        # )

]
# 路由Router
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('areas', views.AreasViewSet, base_name='areas')
urlpatterns += router.urls
