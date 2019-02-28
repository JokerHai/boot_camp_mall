# -*- coding: utf-8 -*-
#后台配置项基类
# @Author  : joker
# @Date    : 2019-02-26
from django.contrib import admin
from boot_camp_mall.common import constants
class BaseAdmin(admin.ModelAdmin):
    #默认每页显示条数
    list_per_page = constants.ADMIN_LIST_PER_PAGE

