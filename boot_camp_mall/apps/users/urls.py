# -*- coding: utf-8 -*-
#User_urs配置项
# @Author  : joker
# @Date    : 2019-01-22

from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from  . import  views
urlpatterns = [
    url(
        regex=r'^signup/$',
        view =views.SignupView.as_view(),
        name ='signUp'
    ),
    url(
        regex=r'^authorizations/$',
        view = obtain_jwt_token
    ),
    url(
        regex=r'^username/(?P<username>\w{5,20})/count/$',
        view =views.UsernameProfileView.as_view(),
        name ='user_profile'
    ),
    url(
        regex=r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',
        view =views.MobileProfileView.as_view(),
        name ='mobile_profile'
    )
]