# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-24
import re
from django_redis import get_redis_connection
from rest_framework import serializers

from boot_camp_mall.common.JwtToken import response_jwt_payload_token
from users.models import User, Address
from boot_camp_mall.utils.tool import perform_phone


class SignupSerializer(serializers.ModelSerializer):
        """
        创建用户序列化器
        """
        password2 = serializers.CharField(label='确认密码',write_only=True) #write_only = 表明该字段仅用于反序列输入

        sms_code = serializers.CharField(label='短信验证码',write_only=True)

        allow = serializers.CharField(label='同意协议',write_only=True)

        token = serializers.CharField(label='JWT Token',read_only=True)

        class Meta:
            model = User

            fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow','token')
            extra_kwargs = {
                'username': {
                    'min_length': 5,
                    'max_length': 20,
                    'error_messages': {
                        'min_length': '仅允许5-20个字符的用户名',
                        'max_length': '仅允许5-20个字符的用户名',
                    }
                },
                'password': {
                    'write_only': True,
                    'min_length': 8,
                    'max_length': 20,
                    'error_messages': {
                        'min_length': '仅允许8-20个字符的密码',
                        'max_length': '仅允许8-20个字符的密码',
                    }
                }
            }
        @classmethod
        def validate_username(cls,value):
            #用户名不能全为数字
            if re.match('^\d+$',value):
                raise serializers.ValidationError('用户名格式不正确')
            return value

        # 是否同意协议，手机号格式，手机号是否存在，两次密码是否一致，短信验证是否正确
        @classmethod
        def validate_mobile(cls,value):
            """验证手机号"""
            if not re.match(r'^1[3-9]\d{9}$', value):
                raise serializers.ValidationError('手机号格式错误')

            # 手机号是否重复
            count = User.objects.filter(mobile=value).count()
            if count > 0:
                raise serializers.ValidationError('手机号已存在')

            return value
        @classmethod
        def validate_allow(cls,value):
            """检验用户是否同意协议"""
            if value != 'true':
                raise serializers.ValidationError('请同意用户协议')
            return value

        def validate(self, data):
            # 判断两次密码
            if data['password'] != data['password2']:
                raise serializers.ValidationError('两次密码不一致')

            # 判断短信验证码
            redis_conn = get_redis_connection('verify_codes')
            mobile = data['mobile']
            real_sms_code = redis_conn.get('sms_%s' % mobile)
            if real_sms_code is None:
                raise serializers.ValidationError('无效的短信验证码')
            if data['sms_code'] != real_sms_code.decode():
                raise serializers.ValidationError('短信验证码错误')

            return data

        def create(self, validated_data):
            """
            创建用户
            """
            # 移除数据库模型类中不存在的属性
            del validated_data['password2']
            del validated_data['sms_code']
            del validated_data['allow']
            # 创建新用户并保存到数据库
            user = User.objects.create_user(**validated_data)

            # 补充生成记录登录状态的token
            token = response_jwt_payload_token(user)
            user.token = token
            return user

class UserDetailSerializer(serializers.ModelSerializer):

    """
        用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id','username','mobile','email','email_active')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['mobile']:
            data['mobile'] = perform_phone(data['mobile'])
        return data

class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','email')
        extra_kwargs = {
            'email':{
                'required':True #是否必传
            }
        }
    def update(self, instance, validated_data):
        #设置登录用户的邮箱
        instance.email = validated_data['email']
        instance.save()

        #生成验证url
        verify_url = instance.generate_verify_email_url()

        #发出发送邮件的任务消息
        from celery_tasks.async_email.tasks import send_verify_email
        send_verify_email.delay(instance.email,verify_url)

        return instance

#收货地址序列化器
class AddressSerializer(serializers.ModelSerializer):
    """
    收货地址序列化器
    """
    province_id = serializers.IntegerField(label='省id')
    city_id = serializers.IntegerField(label='市id')
    district_id = serializers.IntegerField(label='区域id')
    province = serializers.StringRelatedField(label='省', read_only=True)
    city = serializers.StringRelatedField(label='市', read_only=True)
    district = serializers.StringRelatedField(label='区县', read_only=True)
    class Meta:
        model = Address
        exclude = ('user','is_deleted','create_time','update_time')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['mobile']:
            data['mobile'] = perform_phone(data['mobile'])
        return data
    @classmethod
    def validate_mobile(cls,value):
        #手机号格式
        if not re.match(r'^1[3-9]\d{9}$',value):

            raise serializers.ValidationError('手机号格式错误')

        return value

    def create(self, validated_data):

        #获取登录用户对象
        validated_data['user'] = self.context['request'].user

        #调用ModelSerializer中的create方法进行数据保存
        add_address =super().create(validated_data)

        return add_address
#修改标题序列化器
class AddressTitleSerializer(serializers.ModelSerializer):
    """
    地址标题
    """
    class Meta:
        model = Address
        fields = ('title',)