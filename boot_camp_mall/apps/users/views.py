# -*- coding: utf-8 -*-
# Create your views here.
#用户管理
# @Author  : joker
# @Date    : 2019-01-22
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from common.ActionResult import ActionResult
from users.serializers import SignupSerializer , UserDetailSerializer, EmailSerializer
from users.models import User


#url(r'^signup/$')
#注册
class SignupView(CreateAPIView):

    serializer_class = SignupSerializer

# url(r'^username/(?P<username>\w{5,20})/count/$'),
#效验用户名是否存在
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
#效验手机号是否存在
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

#url(r'^user/$')
#获取用户详情
class UserDetailView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

#url(r^email$)
class EmailView(UpdateAPIView):

    """
        保存用户邮箱
    """
    permission_classes = [IsAuthenticated]  # 验证用户登录

    serializer_class = EmailSerializer

    def get_object(self,*args, **kwargs):

        """
        重写get_object方法,获取当前用户对象
        update()中需要get_object获
        :param args:
        :param kwargs:
        :return:
        """
        return self.request.user