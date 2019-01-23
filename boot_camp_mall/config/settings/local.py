# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-22
import logging

from django.utils.log import DEFAULT_LOGGING

from .base import *  # noqa

from .base import env

import os


# GENERAL
# ------------------------------------------------------------------------------

DEBUG = env.bool('DEBUG', default=True)

SECRET_KEY = env('SECRET_KEY', default='fOqtAorZrVqWYbuMPOcZnTzw2D5bKeHGpXUwCaNBnvFUmO1njCQZGz05x1BhDG0E')

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    'api.bootcamp.site'
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
default = env('SESSION_REDIS_URL')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('DEFAULT_REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env('SESSION_REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SESSION_CACHE_ALIAS = "session"



# Sentry
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(ROOT_DIR), "logs"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# rest_framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'meiduo_mall.utils.exceptions.exception_handler',
}

# AUTH_USER_MODEL = '子应用.模型类'
AUTH_USER_MODEL = 'users.User'

# Your stuff...
# ------------------------------------------------------------------------------