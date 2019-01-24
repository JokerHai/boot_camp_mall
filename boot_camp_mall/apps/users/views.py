# -*- coding: utf-8 -*-
# Create your views here.
#用户管理
# @Author  : joker
# @Date    : 2019-01-22
from rest_framework.views import APIView

from common.ActionResult import ActionResult
from users.models import User


class UsernameProfileView(APIView):

    """查找用户是否存在"""
    def get(self,request,username):

        """
        获取指定用户的数量
        """
        total_count = User.objects.filter(username=username).count()

        data = {
            'user_name': username,
            'total_count': total_count
        }
        return ActionResult.success(data)