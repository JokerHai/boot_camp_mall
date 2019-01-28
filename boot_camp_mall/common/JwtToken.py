# -*- coding: utf-8 -*-
#统一返回JwtToken
# @Author  : joker
# @Date    : 2019-01-28
from rest_framework_jwt.settings import api_settings

def response_jwt_payload_token(user=None):
    # 生成payload的方法
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    # 生成jwt token的方法
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    # 生成payload
    payload = jwt_payload_handler(user)
    # 生成jwt token
    jwt_token = jwt_encode_handler(payload)

    return jwt_token
