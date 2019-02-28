# -*- coding: utf-8 -*-

# @Author  : joker
# @Date    : 2019-02-20

def perform_phone(value):
    # 取出中间四位
    list_phone = value[3:7]
    # 加密
    new_phone = value.replace(list_phone, '****')

    return new_phone


def substring(value):
    if len(str(value)) > 20:
        return '{}....'.format(str(value)[0:30])
    else:
        return str(value)
