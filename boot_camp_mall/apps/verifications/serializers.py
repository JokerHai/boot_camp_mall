# -*- coding: utf-8 -*-
#图片验证码效验序列化器
# @Author  : joker
# @Date    : 2019-02-22

from rest_framework import serializers

#图片验证码序列化器
class ImageCodeCheckSerializer(serializers.Serializer):
    """
        图片验证码效验序列化器
    """
    image_code_id = serializers.UUIDField

    text = serializers.CharField(max_length=4,min_length=4)


    def validate(self, attrs):



        return attrs



