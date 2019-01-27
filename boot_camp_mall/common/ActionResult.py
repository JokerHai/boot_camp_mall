# -*- coding: utf-8 -*-
# 封装统一返回值类型 0成功，1失败
# @Author  : joker
# @Date    : 2019-01-24
from rest_framework.response import Response


class ActionResult(object):
    def __init__(self, errcode, errmsg, entity):
        self.errcode = errcode

        self.errmsg = errmsg

        self.entity = entity

    def get_entity(self):
        return self.entity

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    @staticmethod
    def success(entity=None):
        return Response(ActionResult(0, "ok", entity).__dict__)
    @staticmethod
    def failure(errcode,errmsg):
        return Response(ActionResult(errcode,errmsg,None).__dict__,status=errcode)
