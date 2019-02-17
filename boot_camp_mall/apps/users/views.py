# -*- coding: utf-8 -*-
# Create your views here.
# 用户管理
# @Author  : joker
# @Date    : 2019-01-22
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from boot_camp_mall.common import constants
from boot_camp_mall.common.ActionResult import ActionResult
from users.serializers import SignupSerializer, UserDetailSerializer, EmailSerializer, AddressSerializer, \
    AddressTitleSerializer
from users.models import User


# url(r'^signup/$')
# 注册
class SignupView(CreateAPIView):
    serializer_class = SignupSerializer


# url(r'^username/(?P<username>\w{5,20})/count/$'),
# 效验用户名是否存在
class UsernameProfileView(APIView):
    """查找用户是否存在"""

    def get(self, request, username):
        """
        获取指定用户的数量
        """
        total_count = User.objects.filter(username=username).count()

        data = {
            'user_name': username,
            'count': total_count
        }
        return ActionResult.success(data)


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$')
# 效验手机号是否存在
class MobileProfileView(APIView):
    """
        手机号数量
    """

    def get(self, request, mobile):
        """
        获取指定手机的数量
        :param request:
        :param mobile:
        :return:
        """
        total_count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': total_count
        }
        return ActionResult.success(data)


# url(r'^user/$')
# 获取用户详情
class UserDetailView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# url(r^email$)
class EmailView(UpdateAPIView):
    """
        保存用户邮箱
    """
    permission_classes = [IsAuthenticated]  # 验证用户登录

    serializer_class = EmailSerializer

    def get_object(self, *args, **kwargs):
        """
        重写get_object方法,获取当前用户对象
        update()中需要get_object获
        :param args:
        :param kwargs:
        :return:
        """
        return self.request.user


# url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
class VerifyEmailView(APIView):
    """
    邮箱验证
    """
    def put(self, request):
        # 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message': '链接信息无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({'message': 'OK'})

#url(r'^addresses/$')
class AddressViewSet(CreateModelMixin,UpdateModelMixin,GenericViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)
    #Post /addresses/
    def create(self,request,*args,**kwargs):

        # 0. 判断用户的地址数量是否超过数量上限
        count = request.user.addresses.filter(is_deleted=False).count()

        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message': '地址数量超过上限'}, status=status.HTTP_400_BAD_REQUEST)
        # #获取参数并进行效验，
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        #
        # #创建并保存新增数据(create)
        #
        # serializer.save()
        #
        # #返回相应
        # return Response(serializer.data,status=status.HTTP_201_CREATED)
        return super().create(request,*args,**kwargs)
    def list(self,request):

        #1.获取登录用户所有地址数据

        addresses = self.get_queryset()

        #2.将地址数据序列化返回
        serializer = self.get_serializer(addresses, many=True)

        return Response({
            'user_id':request.user.id,
            'default_address_id':request.user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data
        })

    # delete /addresses/<pk>/
    def destroy(self,request,pk):
        """
            处理删除
        :return:
        """
        address = self.get_object()

        #进行逻辑删除
        address.is_deleted = True

        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    #PUT /addresses/pk/status
    @action(methods=['put'],detail=True)
    def status(self,request,pk):
        """
        设为默认地址
        """
        address = self.get_object()

        request.user.default_address = address

        request.user.save()

        return Response({'message':'OK'},status=status.HTTP_200_OK)
    # put /addresses/pk/title/
    # 需要请求体参数 title
    @action(methods=['put'], detail=True)
    def title(self, request, pk):
        """
        修改标题
        """
        address = self.get_object()
        serializer = AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)