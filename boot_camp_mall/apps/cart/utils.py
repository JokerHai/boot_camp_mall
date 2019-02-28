# -*- coding: utf-8 -*-
#添加购物车逻辑
# @Author  : joker
# @Date    : 2019-02-27
from django_redis import get_redis_connection

#添加购物车
from goods.models import SKU


def save_cart(user = None,request = None):

    user = user if user is not None else user

    if user and user.is_authenticated:
        #保存用户的购物车记录
        redis_con = get_redis_connection('cart')

        pipeline = redis_con.pipeline()

        cart_key = 'cart_%s' % user.id

        # 保存购物车中商品及数量

        pipeline.hincrby(cart_key, request['sku_id'], request['count'])

        #保存购物车商品的选中状态

        cart_selected_key = 'cart_selected_%s' % user.id

        if request['selected']:
            pipeline.sadd(cart_selected_key,request['sku_id'])

        pipeline.execute()

        return request
    else:

        pass

#获取购物车信息
def get_cart(user = None):

    user = user if user is not None else user

    if user:
        # 2.1 如果用户已登录，从redis中获取用户的购物车记录
        redis_conn = get_redis_connection('cart')

        cart_key = 'cart_%s' % user.id
        redis_cart = redis_conn.hgetall(cart_key)

        cart_selected_key = 'cart_selected_%s' % user.id
        redis_cart_selected = redis_conn.smembers(cart_selected_key)

        cart_dict = {}
        for sku_id, count in redis_cart.items():
            cart_dict[int(sku_id)] = {
                'count': int(count),
                'selected': sku_id in redis_cart_selected
            }

        # 3. 根据购物车记录获取对应商品的信息
        sku_result = SKU.objects.filter(id__in=cart_dict.keys())
        for sku in sku_result:
            sku.count = cart_dict[sku.id]['count']
            sku.selected = cart_dict[sku.id]['selected']

        return sku_result