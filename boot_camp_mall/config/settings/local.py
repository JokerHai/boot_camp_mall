# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-22
import datetime

import sys

from .base import *  # noqa

from .base import env

import os


# GENERAL
# ------------------------------------------------------------------------------

DEBUG = env.bool('DEBUG', default=True)

SECRET_KEY = env('SECRET_KEY', default='fOqtAorZrVqWYbuMPOcZnTzw2D5bKeHGpXUwCaNBnvFUmO1njCQZGz05x1BhDG0E')

HOME_URL = '/'

# apps注入系统中
#-------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_DIR, 'apps'))

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    'api.bootcamp.site'
]
# CORS跨域请求的白名单
#-------------------------------------------------------------------------------
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1',
    'localhost',
    'www.meiduo.site',
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie
# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': env.str('POSTGRES_HOST'),  # 数据库主机
        'PORT': env.int('POSTGRES_PORT'),  # 数据库端口
        'USER': env.str('POSTGRES_USER'),  # 数据库用户名
        'PASSWORD': env.str('POSTGRES_PASSWORD'),  # 数据库用户密码
        'NAME': env.str('POSTGRES_DB')  # 数据库名字
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    # },
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
            'IGNORE_EXCEPTIONS': True,
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env('SESSION_REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 存储短信验证码的内容
    "verify_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env('SMS_REDIS_URL'),
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
            'filename': os.path.join(ROOT_DIR, "logs/"+datetime.datetime.now().strftime('%Y-%m-%d')+".log"),  # 日志文件的位置
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
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'boot_camp_mall.utils.exceptions.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# django-cors-headers 解决跨域问题
# -----------------------------------------------------------------------------
MIDDLEWARE += ['corsheaders.middleware.CorsMiddleware']

#JWT_AUTH 有效时间
# -----------------------------------------------------------------------------
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

# Your stuff...
# -----------------------------------------------------------------------------

# AUTH_USER_MODEL = '子应用.模型类'
AUTH_USER_MODEL = 'users.User'

#自定义django认证效验
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]

#QQ登录参数
# -----------------------------------------------------------------------------
QQ_CLIENT_ID = env.str('QQ_CLIENT_ID') #开发者应用ID
QQ_CLIENT_SECRET = env.str('QQ_CLIENT_SECRET') #开发者应用appkey
QQ_REDIRECT_URI = env.str('QQ_REDIRECT_URI')#开发者回调地址
QQ_STATE = HOME_URL #登录成功之后要访问的页面

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env.str('EMAIL_HOST')
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = env.str('EMAIL_PORT')

#发送邮件的邮箱
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')

#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

#收件人看到的发件人
EMAIL_FROM = env.str('EMAIL_FROM')

# DRF扩展,地区数据缓存配置
# ------------------------------------------------------------------------------
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

#静态文件处理
#--------------------------------------------------------------------------------
STATIC_ROOT = os.path.join(ROOT_DIR, 'front_end_pc/static')