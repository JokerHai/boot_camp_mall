# -*- coding: utf-8 -*-
#全局分页配置类
# @Author  : joker
# @Date    : 2019-02-26
from rest_framework.pagination import PageNumberPagination
from boot_camp_mall.common import constants

class StandardResultPagination(PageNumberPagination):
     #默认每页显示条数
     page_size = constants.FRONT_LIST_PER_PAGE
     #获取分页数据时，传递`页容量`参数名称
     page_size_query_param = 'page_size'
     # 最大`页容量`
     max_page_size = constants.Front_LIST_PER_MAX_PAGE
