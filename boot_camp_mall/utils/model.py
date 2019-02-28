# -*- coding: utf-8 -*-
#模型基类
# @Author  : joker
# @Date    : 2019-01-27

from django.db import models

class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表


    def filtration_create_time(self):
        return self.create_time.strftime('%Y年%m月%d日')
    filtration_create_time.short_description = '发布日期'
    filtration_create_time.admin_order_field = 'create_time'

    def filtration_update_time(self):

        return self.update_time.strftion('%Y年%m月%d日')

    filtration_update_time.short_description = '修改日期'
    filtration_update_time.admin_order_field = 'update_time'
