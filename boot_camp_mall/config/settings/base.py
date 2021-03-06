# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-01-22
"""
项目基础设置.

"""

import environ

ROOT_DIR = environ.Path(__file__) - 4  # (boot_camp_mall/config/settings/base.py - 3 = boot_camp_mall/)

APPS_DIR = ROOT_DIR.path('boot_camp_mall')

env = environ.Env()

env.read_env(str(ROOT_DIR.path('.env')))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', False)


ROOT_URLCONF = 'boot_camp_mall.config.urls'

WSGI_APPLICATION = 'boot_camp_mall.config.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = env.str('LANGUAGE_CODE')

TIME_ZONE = env.str('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# APPS
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [APPS_DIR+'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
#扩展APPS
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'ckeditor',#富文本编辑器
    'ckeditor_uploader',#富文本编辑器上传模块
    'django_crontab',  # 定时任务
    'django_filters',  # django搜索过滤，
]

#项目配置Apps
LOCAL_APPS = [
    'home.apps.HomeConfig',
    'users.apps.UsersConfig',
    'verifications.apps.VerificationsConfig',
    'oauth.apps.OauthConfig',
    'areas.apps.AreasConfig',
    'goods.apps.GoodsConfig',
    'contents.apps.ContentsConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrderConfig',
    #FastDFS上传测试类
    'pic.apps.PicConfig',
]

INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'