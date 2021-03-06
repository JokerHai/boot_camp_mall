# -*- coding: utf-8 -*-
#项目的URL配置文件
# @Author  : joker
# @Date    : 2019-01-21

"""boot_camp_mall URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URL_conf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'',include('home.urls',namespace='home')),
    url(r'',include('users.urls',namespace='users')),
    url(r'',include('verifications.urls',namespace='verifications')),
    url(r'oauth/',include('oauth.urls',namespace='qq_oauth')),
    url(r'',include('areas.urls',namespace='areas')),
    url(r'',include('goods.urls',namespace='goods')),
    url(r'',include('cart.urls',namespace='cart')),
    url(r'',include('orders.urls',namespace='order')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

]