# -*- coding: utf-8 -*-
#系统常量定义
# @Author  : joker
# @Date    : 2019-01-23

#MALL_HOME
MALL_HOME = 'http://www.meiduo.site:8000/'

# 短信验证码有效的时间: s
SMS_CODE_REDIS_EXPIRES = 300


# 发送短信模板ID
SEND_SMS_TEMP_ID = 1

# 短信发送间隔限制: s
SEND_SMS_CODE_INTERVAL = 60

#图片验证码redis有效期，单位秒
IMAGE_CODE_REDIS_EXPIRES = 300

# 邮箱验证链接有效时间: s
VERIFY_EMAIL_TOKEN_EXPIRES = 7200

#verify_url_email

EMAIL_VERIFY_URL = MALL_HOME+'success_verify_email.html?token='