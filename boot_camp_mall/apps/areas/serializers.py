# -*- coding: utf-8 -*-
#area序列化器
# @Author  : joker
# @Date    : 2019-02-16
from rest_framework import serializers

from areas.models import Area


class AreasSerializers(serializers.ModelSerializer):

    class Meta:

        model = Area

        fields = ('id','name')

class SubAreaSerializers(serializers.ModelSerializer):
    """
    地区序列化器类
    """
    subs = AreasSerializers(label='下级地区',many=True)

    class Meta:
        model = Area

        fields = ('id','name','subs')
