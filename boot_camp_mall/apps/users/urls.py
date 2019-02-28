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
    ),
    url(
        regex=r'^user/$',
        view =views.UserDetailView.as_view(),
        name ='user_detail'
    ),
    url(
        regex=r'^email/$',
        view =views.EmailView.as_view(),
        name='send_email'
    ),
    url(
        regex=r'^emails/verification/$',
        view =views.VerifyEmailView.as_view(),
        name ='verify_email'
    ),
    url(
        regex=r'^password_reset/$',
        view =views.ResetPasswordView.as_view(),
        name ='reset_password'
    ),
    url(
        regex=r'^orders/$',
        view=views.MyOrderView.as_view(),
        name='my_orders'
    )
]
# 路由Router
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('addresses', views.AddressViewSet, base_name='addresses')
urlpatterns += router.urls