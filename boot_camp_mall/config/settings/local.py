# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-22
import logging

from django.utils.log import DEFAULT_LOGGING

from .base import *  # noqa

from .base import env


# GENERAL
# ------------------------------------------------------------------------------

DEBUG = env.bool('DEBUG', default=True)

SECRET_KEY = env('SECRET_KEY', default='fOqtAorZrVqWYbuMPOcZnTzw2D5bKeHGpXUwCaNBnvFUmO1njCQZGz05x1BhDG0E')

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]
# DATABASES
# ------------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': env.str('POSTGRES_HOST'),  # 数据库主机
        'PORT': env.int('POSTGRES_PORT'),  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'root',  # 数据库用户密码
        'NAME': env.str('POSTGRES_DB')  # 数据库名字
    }
}

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SESSION_CACHE_ALIAS = "default"

# Your stuff...
# ------------------------------------------------------------------------------