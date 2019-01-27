# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-24
import re

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }
#自定义Django认证后端类
class UsernameMobileAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        """
        username :用户名或手机号
        password :密码
        """
        #根据用户名或者手机号查询用户信息
        try:
             user = User.objects.get(Q(username=username) | Q(mobile=username))
        except User.DoesNotExist:
            return  None
        #如果用户存在，在效验密码
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
             return user