# -*- coding: utf-8 -*-
#图片验证码效验序列化器
# @Author  : joker
# @Date    : 2019-02-22
from django_redis import get_redis_connection
from rest_framework import serializers


class ImageCodeCheckSerializers(serializers.Serializer):
    """
        图片验证码效验序列化器
    """
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4,min_length=4)

    def validate(self, attrs):
        """
        效验
        """
        image_code_id = attrs['image_code_id']
        text = attrs['text']
        #查询真实图片验证码
        redis_conn = get_redis_connection('verify_codes')

        real_image_code_text = redis_conn.get('img_%s' % image_code_id)

        if not real_image_code_text:

            raise  serializers.ValidationError('图片验证码无效')

        #比较图片验证码

        real_image_code_text = real_image_code_text.decode()

        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError('图片验证码错误')

        #删除图片验证码
        redis_conn.delete('img_%s' % image_code_id)
        #判断是否在60秒内
        model = self.context['view'].kwargs['mobile']

        send_flag = redis_conn.get("send_flag_%s" % model)

        if send_flag:

            raise serializers.ValidationError('请求次数过于频繁')

        return attrs

class CheckSMSCodeSerializers(serializers.Serializer):
    """
    短信验证码序列化器
    """
    sms_code = serializers.CharField(max_length=6,min_length=6)

    def validate(self, data):
        redis_conn = get_redis_connection('verify_codes')

        model = self.context['view'].kwargs['mobile']

        real_mobile_code_text = redis_conn.get('sms_%s' % model)

        if real_mobile_code_text is not  None:

            if real_mobile_code_text.decode()!= data['sms_code']:

                raise  serializers.ValidationError('短信验证码不正确')
        else:
                raise  serializers.ValidationError('数据非法')
        return data






