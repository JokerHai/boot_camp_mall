# -*- coding: utf-8 -*-
#商品序列化器
# @Author  : joker
# @Date    : 2019-02-26
from rest_framework import serializers

from goods.models import SKU


class SKUSerializer(serializers.ModelSerializer):
    """
        SKU商品序列化器类
    """
    class Meta:
        model = SKU
        fields = ('id','name','price','default_image_url','comments','is_hot')
