# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-02-13

from .base import env
# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False

SECRET_KEY = env('SECRET_KEY', default='fOqtAorZrVqWYbuMPOcZnTzw2D5bKeHGpXUwCaNBnvFUmO1njCQZGz05x1BhDG0E')

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