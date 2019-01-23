# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-23

from celery import Celery


# 创建celery应用

app = Celery('celery_tasks')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks(['celery_tasks.sms'])