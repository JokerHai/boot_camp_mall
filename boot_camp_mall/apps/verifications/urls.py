# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-22
from django.conf.urls import url

from . import views
urlpatterns = [
    url(
        regex=r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',
        view=views.SMSCodeView.as_view(),
        name='verify_sms_codes'
    ),
    url(
        regex=r'^image_codes/(?P<image_code_id>[\w-]+)/$',
        view=views.ImageCodeView.as_view(),
        name='verify_image_codes'
    )
]