# -*- coding: utf-8 -*-
#WSGI兼容的Web服务器入口
# @Author  : joker
# @Date    : 2019-01-21

"""
WSGI config for boot_camp_mall project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_wsgi_application()