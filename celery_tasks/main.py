# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-23
import os

from celery import Celery

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boot_camp_mall.config.settings.local")
# 创建celery应用
app = Celery('celery_tasks')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks([
            'celery_tasks.async_sms',#手机验证码异步任务
            'celery_tasks.async_email'#邮箱异步任务
        ])