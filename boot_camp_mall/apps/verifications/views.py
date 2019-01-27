import random

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from common import constants

#r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$'
from common.ActionResult import ActionResult


class SMSCodeView(APIView):
    def get(self, request, mobile):

        """
            获取短信验证码
        """
        redis_conn = get_redis_connection('verify_codes')

        send_flag = redis_conn.get("send_flag_%s" % mobile)

        if send_flag:
            return Response({"message": "请求次数过于频繁"}, status=status.HTTP_400_BAD_REQUEST)
        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)

        # 创建redis管道对象
        pl = redis_conn.pipeline()

        print("短信验证码:%s" % sms_code)

        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, constants.SEND_SMS_TEMP_ID)
        # 一次执行redis管道的所有命令
        pl.execute()

        expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        # 发出发送短信任务消息
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code, expires)

        return ActionResult.success()
