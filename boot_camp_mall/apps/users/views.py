# -*- coding: utf-8 -*-
# Create your views here.
#用户管理
# @Author  : joker
# @Date    : 2019-01-22
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from common.ActionResult import ActionResult
from users import serializers
from users.models import User



class UserView(CreateAPIView):

    serializer_class = serializers.CreateUserSerializer

# url(r'^username/(?P<username>\w{5,20})/count/$'),
class UsernameProfileView(APIView):

    """查找用户是否存在"""
    def get(self,request,username):

        """
        获取指定用户的数量
        """
        total_count = User.objects.filter(username=username).count()

        data = {
            'user_name': username,
            'count': total_count
        }
        return ActionResult.success(data)

#url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$')
class MobileProfileView(APIView):
    """
        手机号数量
    """

    def get(self,request,mobile):
        """
        获取指定手机的数量
        :param request:
        :param mobile:
        :return:
        """
        total_count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile':mobile,
            'count':total_count
        }
        return ActionResult.success(data)