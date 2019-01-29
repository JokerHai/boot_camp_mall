# -*- coding: utf-8 -*-
#oauth序列化器
# @Author  : joker
# @Date    : 2019-01-28
import base64
import os

from django_redis import get_redis_connection
from rest_framework import serializers

from common.JwtToken import response_jwt_payload_token
from oauth.models import OAuthQQUser
from oauth.utils import OAuthQQ
from users.models import User


class QQAuthUserSerializer(serializers.ModelSerializer):

    sms_code = serializers.CharField(label='短信验证码',write_only=True)
    access_token = serializers.CharField(label='加密openid',write_only=True)
    token = serializers.CharField(label='jwt_token',read_only=True)
    mobile = serializers.RegexField(regex=r'^1[3-9]\d{9}$',write_only=True)
    class Meta:
        model = User
        fields = ('id','username','mobile','password','sms_code','access_token','token')
        extra_kwargs = {
            'username':{
                'read_only':True #表名该字段序列化输出
            },
            'password':{
                'write_only':True
            }

        }
    #手机号格式，短信验证码是否正确，access_token是否有效

    def validate(self, attrs):
        #access_token是否有效
        access_token = attrs['access_token']
        openid = OAuthQQ.check_save_user_token(access_token)
        if openid is None:
            #解密失败
            raise serializers.ValidationError('无效的access_token')
        attrs['openid'] = openid

        #短信验证码是否正确
        mobile = attrs['mobile']

        #从redis中获取真实的验证码内容
        redis_conn = get_redis_connection('verify_codes')

        real_sms_code = redis_conn.get('sms_%s' % mobile)

        if real_sms_code is None:
            raise serializers.ValidationError('短信验证码已失效')

        #对比验证码内容
        sms_code = attrs['sms_code'] #str

        if real_sms_code.decode() != sms_code:
            raise  serializers.ValidationError('短信验证码错误')

        #如果`mobile`已注册，校验对应的密码是否正确
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            #未注册
            user = None
        else:
            #已注册
            password = attrs['password']
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
        #校验是否已有绑定记录了拦截重复请求绑定接口
        count = OAuthQQUser.objects.filter(openid=openid).count()
        if count >0:
            raise serializers.ValidationError('您已绑定了，请勿重复提交')
        attrs['user'] = user

        return attrs
    def create(self, validated_data):
        #如果`mobile`未注册，先创建一个新用户
        openid = validated_data['openid']
        user = validated_data['user']
        mobile = validated_data['mobile']
        password = validated_data['password']
        if not user:
            #随机生成一个用户名
            username = base64.b64encode(os.urandom(9)).decode()
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        #保存QQ 绑定的数据
        OAuthQQUser.objects.create(user=user,openid=openid)
        token = response_jwt_payload_token(user)
        user.token = token
        return user