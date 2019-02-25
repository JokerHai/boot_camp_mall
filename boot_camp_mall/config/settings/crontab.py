# -*- coding: utf-8 -*-
#定时任务配置文件
# @Author  : joker
# @Date    : 2019-02-25
import os

import datetime

from .base import *
# 解决crontab中文问题
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'


# 定时任务
CRONJOBS = [
    # 每5分钟执行一次生成主页静态文件
    ('*/1 * * * *', 'home.crons.generate_static_index_html', '>> '+os.path.join(ROOT_DIR,"logs/crontab/"+datetime.datetime.now().strftime('%Y-%m-%d')+".log"))
]
