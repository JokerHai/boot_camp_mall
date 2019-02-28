# -*- coding: utf-8 -*-
#购物车序列化器
# @Author  : joker
# @Date    : 2019-02-27
from rest_framework import serializers

from goods.models import SKU

#购物车序列化器
class CartSerializer(serializers.Serializer):

    """
        购物车序列化器
    """
    sku_id = serializers.IntegerField(label='sku_id',min_value=1)

    count = serializers.IntegerField(label='购买数量',min_value=1)

    selected = serializers.BooleanField(label='是否勾选',default=True)


    def validate(self, data):

        try:
            sku_result = SKU.objects.get(id = data['sku_id'])
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        #效验库存
        if data['count'] >sku_result.stock:

            raise serializers.ValidationError('商品库存不存在')


        return data


#购物车商品数据序列化器
class CartSKUSerializer(serializers.ModelSerializer):
    """
        购物车商品数据序列化器
    """

    count = serializers.IntegerField(label='数量')
    selected = serializers.BooleanField(label='是否勾选')

    class Meta:
        model = SKU
        fields = ('id', 'count', 'name', 'default_image_url', 'price', 'selected')


