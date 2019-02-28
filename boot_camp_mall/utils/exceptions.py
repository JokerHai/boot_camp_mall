# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-22
import logging

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError
from redis.exceptions import RedisError

# 获取在配置文件中定义的logger，用来记录日志


logger = logging.getLogger('django')

def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, type(exc)))

            response = Response({
                 'errmsg': '服务器内部错误,请联系管理员'
            },status=status.HTTP_507_INSUFFICIENT_STORAGE)
        # response.data['status_code'] = response.status_code
    return response
